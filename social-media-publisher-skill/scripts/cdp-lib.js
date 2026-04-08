/**
 * CDP 工具库 - 提供通用的 CDP 连接和操作功能
 * 使用 web-access CDP Proxy (端口 3456)
 */

import http from 'http';

const CDP_PROXY_URL = 'http://localhost:3456';

/**
 * HTTP 请求辅助函数
 */
function httpRequest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, CDP_PROXY_URL);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(30000);
    
    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

/**
 * 列出所有 tab
 */
export async function getTargets() {
  return await httpRequest('GET', '/targets');
}

/**
 * 创建新 tab
 */
export async function createTarget(url) {
  return await httpRequest('GET', `/new?url=${encodeURIComponent(url)}`);
}

/**
 * 执行 JavaScript
 */
export async function evalJS(targetId, expression) {
  const result = await httpRequest('POST', `/eval?target=${targetId}`, expression);
  if (result.error) {
    throw new Error(`JS 执行失败：${result.error}`);
  }
  return result.value;
}

/**
 * 点击元素
 */
export async function clickElement(targetId, selector) {
  return await httpRequest('POST', `/click?target=${targetId}`, selector);
}

/**
 * 上传文件到 input[type=file]
 */
export async function setFiles(targetId, selector, files) {
  const body = { selector, files };
  return await httpRequest('POST', `/setFiles?target=${targetId}`, body);
}

/**
 * 截图
 */
export async function screenshot(targetId, filePath = 'screenshot.png') {
  return await httpRequest('GET', `/screenshot?target=${targetId}&file=${filePath}`);
}

/**
 * 关闭 tab
 */
export async function closeTarget(targetId) {
  return await httpRequest('GET', `/close?target=${targetId}`);
}

/**
 * 等待页面加载
 */
export async function waitForLoad(targetId, timeoutMs = 15000) {
  const startTime = Date.now();
  
  while (Date.now() - startTime < timeoutMs) {
    try {
      const readyState = await evalJS(targetId, 'document.readyState');
      if (readyState === 'complete') {
        await new Promise(r => setTimeout(r, 1000)); // 额外等待 1 秒
        return true;
      }
    } catch (e) {
      // 忽略错误，继续等待
    }
    await new Promise(r => setTimeout(r, 500));
  }
  
  throw new Error(`页面加载超时 (${timeoutMs}ms)`);
}

/**
 * 查找按钮
 */
export async function findButtons(targetId, keywords = ['发布', '保存', '下一步']) {
  const buttons = await evalJS(targetId, `(() => {
    const results = [];
    const allButtons = document.querySelectorAll('button, span[role="button"], div[role="button"]');
    allButtons.forEach(btn => {
      const text = (btn.innerText || btn.textContent || '').trim();
      if (text && keywords.some(kw => text.includes(kw))) {
        const rect = btn.getBoundingClientRect();
        results.push({
          text: text,
          visible: rect.width > 0 && rect.height > 0,
          top: rect.top,
          left: rect.left
        });
      }
    });
    return results;
  })()`);
  
  return buttons || [];
}

/**
 * 带重试的操作
 */
export async function withRetry(operation, maxRetries = 2, delayMs = 1000) {
  let lastError;
  
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;
      console.log(`操作失败，重试 ${i + 1}/${maxRetries}: ${error.message}`);
      if (i < maxRetries) {
        await new Promise(r => setTimeout(r, delayMs));
      }
    }
  }
  
  throw lastError;
}
