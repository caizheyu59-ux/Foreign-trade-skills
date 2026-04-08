/**
 * 测试连接脚本
 * 验证所有依赖是否正常
 */

import http from 'http';

function httpRequest(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    }).on('error', reject);
  });
}

async function testConnection() {
  console.log('ℹ️  测试 CDP 连接...\n');
  
  // 测试 1: CDP Proxy
  try {
    const targets = await httpRequest('http://localhost:3456/targets');
    console.log('✅ CDP Proxy 连接成功');
    console.log(`   当前 tab 数：${Array.isArray(targets) ? targets.length : 0}`);
  } catch (error) {
    console.log('❌ CDP Proxy 连接失败');
    console.log(`   错误：${error.message}`);
    console.log('\n解决：启动 web-access CDP Proxy');
    console.log('  node ~/.openclaw/skills/web-access/scripts/cdp-proxy.mjs\n');
    process.exit(1);
  }
  
  // 测试 2: Chrome 远程调试
  try {
    const targets = await httpRequest('http://localhost:3456/targets');
    if (Array.isArray(targets)) {
      console.log('✅ Chrome 远程调试正常');
    } else {
      throw new Error('返回格式错误');
    }
  } catch (error) {
    console.log('❌ Chrome 远程调试失败');
    console.log(`   错误：${error.message}`);
    console.log('\n解决：');
    console.log('  1. 打开 chrome://inspect/#remote-debugging');
    console.log('  2. 勾选 "Allow remote debugging"');
    console.log('  3. 重启 Chrome\n');
    process.exit(1);
  }
  
  console.log('\n✅ 所有依赖正常\n');
  console.log('可以开始使用技能了！');
  console.log('\n使用示例：');
  console.log('  node upload-xhs.js "C:\\video.mp4" "C:\\content.txt"\n');
}

testConnection();
