/**
 * 小红书视频上传脚本
 * 
 * 使用方法：
 * node upload-xhs.js <video_path> <content_path>
 * 
 * 示例：
 * node upload-xhs.js "C:\video.mp4" "C:\content.txt"
 */

import fs from 'fs';
import { createTarget, evalJS, setFiles, clickElement, screenshot, waitForLoad, findButtons, withRetry } from './cdp-lib.js';
import { createLogger } from './logger.js';
import { getConfig } from './config.js';
import { getSelector } from './selectors.js';

// 初始化日志
const config = getConfig();
const log = createLogger({
  level: config.general.logLevel,
  saveToFile: config.files.saveScreenshots,
  logFile: config.files.logFile
});

// 配置
const UPLOAD_URL = 'https://creator.xiaohongshu.com/publish/publish';
const CHECKPOINT_FILE = config.general.progressFile;

// 保存进度
function saveProgress(step, data = {}) {
  if (!config.general.saveProgress) return;
  
  fs.writeFileSync(CHECKPOINT_FILE, JSON.stringify({
    step,
    timestamp: Date.now(),
    ...data
  }, null, 2));
  log.debug(`进度已保存：${step}`);
}

// 读取进度
function loadProgress() {
  try {
    if (fs.existsSync(CHECKPOINT_FILE)) {
      return JSON.parse(fs.readFileSync(CHECKPOINT_FILE, 'utf-8'));
    }
  } catch (e) {
    log.debug('读取进度失败', e);
  }
  return null;
}

// 清除进度
function clearProgress() {
  if (fs.existsSync(CHECKPOINT_FILE)) {
    fs.unlinkSync(CHECKPOINT_FILE);
    log.debug('进度文件已清除');
  }
}

// 解析内容文件
function parseContentFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  
  const titleMatch = content.match(/短标题\s*\n([\s\S]*?)(?=\d+\.|$)/i);
  const descMatch = content.match(/第一人称摘要[\s\S]*?\n\n([\s\S]*?)(?=标签：|$)/i);
  const tagsMatch = content.match(/标签：(.+)/i);
  
  return {
    title: titleMatch?.[1]?.trim() || '',
    description: descMatch?.[1]?.trim() || '',
    tags: tagsMatch?.[1]?.trim()?.split(/\s+/).filter(t => t.startsWith('#')) || []
  };
}

// 主流程
async function uploadVideo(videoPath, contentPath) {
  log.divider('═', 60);
  log.info(' 小红书视频上传流程');
  log.divider('═', 60);
  
  // 检查文件
  if (!fs.existsSync(videoPath)) {
    log.error(`视频文件不存在：${videoPath}`);
    throw new Error(`视频文件不存在：${videoPath}`);
  }
  if (!fs.existsSync(contentPath)) {
    log.error(`内容文件不存在：${contentPath}`);
    throw new Error(`内容文件不存在：${contentPath}`);
  }
  
  // 解析内容
  const content = parseContentFile(contentPath);
  log.stepStart('准备内容', 0, 5);
  log.info(`标题：${content.title}`);
  log.info(`描述：${content.description.substring(0, 50)}...`);
  log.info(`标签：${content.tags.length} 个`);
  log.stepComplete('准备内容');
  
  // 检查进度
  const progress = loadProgress();
  let targetId = null;
  let startStep = 'open';
  
  if (progress) {
    log(`发现未完成的进度：${progress.step}`, 'warning');
    startStep = progress.step;
    // TODO: 恢复 targetId（需要更复杂的会话管理）
  }
  
  // 步骤 1: 打开页面
  if (startStep === 'open' || startStep === 'upload') {
    log('步骤 1/5: 打开上传页面...');
    const result = await createTarget(UPLOAD_URL);
    targetId = result.targetId;
    log(`页面已打开：${targetId}`);
    
    await waitForLoad(targetId);
    saveProgress('open', { targetId });
  }
  
  // 步骤 2: 上传视频
  if (startStep === 'open' || startStep === 'upload') {
    log('步骤 2/5: 上传视频文件...');
    await withRetry(async () => {
      await setFiles(targetId, 'input[type="file"]', [videoPath]);
      await evalJS(targetId, `(() => {
        const input = document.querySelector('input[type="file"]');
        if (input) input.dispatchEvent(new Event('change', { bubbles: true }));
      })()`);
    });
    
    log('视频上传成功，等待处理...');
    await new Promise(r => setTimeout(r, 10000)); // 等待 10 秒
    saveProgress('upload', { targetId });
  }
  
  // 步骤 3: 填写标题
  if (startStep === 'upload' || startStep === 'title') {
    log('步骤 3/5: 填写标题...');
    await withRetry(async () => {
      const result = await evalJS(targetId, `(() => {
        const input = document.querySelector('input[placeholder*="标题"]');
        if (!input) return { error: '未找到标题框' };
        input.value = '${content.title.replace(/'/g, "\\'")}';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        return { success: true };
      })()`);
      
      if (result.error) throw new Error(result.error);
    });
    
    log('标题填写成功');
    saveProgress('title', { targetId });
  }
  
  // 步骤 4: 填写描述
  if (startStep === 'title' || startStep === 'description') {
    log('步骤 4/5: 填写描述...');
    await withRetry(async () => {
      const result = await evalJS(targetId, `(() => {
        const editor = document.querySelector('div[contenteditable="true"]');
        if (!editor) return { error: '未找到编辑器' };
        editor.focus();
        document.execCommand('insertText', false, '${content.description.substring(0, 500).replace(/'/g, "\\'")}');
        return { success: true };
      })()`);
      
      if (result.error) throw new Error(result.error);
    });
    
    log('描述填写成功');
    saveProgress('description', { targetId });
  }
  
  // 步骤 5: 添加标签
  if (startStep === 'description' || startStep === 'tags') {
    log('步骤 5/5: 添加标签...');
    
    for (const tag of content.tags.slice(0, 5)) {
      await withRetry(async () => {
        await evalJS(targetId, `(() => {
          const editor = document.querySelector('div[contenteditable="true"]');
          if (!editor) return { error: '未找到编辑器' };
          editor.focus();
          document.execCommand('insertText', false, ' ${tag}');
          return { success: true };
        })()`);
      });
      
      log(`  添加标签：${tag}`);
      await new Promise(r => setTimeout(r, 500));
    }
    
    saveProgress('tags', { targetId });
  }
  
  // 截图确认
  log('截图确认...');
  await screenshot(targetId, 'xhs-result.png');
  log('截图已保存：xhs-result.png');
  
  // 查找按钮
  const buttons = await findButtons(targetId);
  log(`找到按钮：${buttons.map(b => b.text).join(', ')}`);
  
  // 完成
  log('上传流程完成！', 'success');
  log('请在浏览器中检查内容，然后手动点击发布按钮');
  clearProgress();
  
  return { targetId, success: true };
}

// 命令行入口
const args = process.argv.slice(2);

if (args.length < 2) {
  console.log('使用方法：');
  console.log('  node upload-xhs.js <video_path> <content_path>');
  console.log('');
  console.log('示例：');
  console.log('  node upload-xhs.js "C:\\video.mp4" "C:\\content.txt"');
  process.exit(1);
}

const [videoPath, contentPath] = args;

uploadVideo(videoPath, contentPath)
  .then(() => {
    process.exit(0);
  })
  .catch((error) => {
    log(`错误：${error.message}`, 'error');
    saveProgress('error', { error: error.message });
    process.exit(1);
  });
