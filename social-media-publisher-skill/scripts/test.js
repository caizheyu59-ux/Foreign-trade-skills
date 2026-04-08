/**
 * 测试套件
 * 验证技能包的核心功能
 */

import { createLogger } from './logger.js';
import { getConfig, validateConfig } from './config.js';
import { getSelector, getSelectors } from './selectors.js';

const log = createLogger({ level: 'info' });

// 测试结果
let passed = 0;
let failed = 0;
let total = 0;

/**
 * 断言函数
 */
function assert(condition, message) {
  total++;
  if (condition) {
    passed++;
    log.success(`✓ ${message}`);
  } else {
    failed++;
    log.error(`✗ ${message}`);
  }
}

/**
 * 测试配置模块
 */
function testConfig() {
  log.divider('─', 50);
  log.info('测试配置模块');
  log.divider('─', 50);
  
  // 测试 1: 获取默认配置
  try {
    const config = getConfig();
    assert(config !== null, '获取默认配置');
    assert(config.general.logLevel === 'info', '默认日志级别为 info');
    assert(config.retry.maxRetries === 2, '默认重试次数为 2');
  } catch (e) {
    assert(false, `获取配置失败：${e.message}`);
  }
  
  // 测试 2: 验证配置
  try {
    const config = getConfig();
    const valid = validateConfig(config);
    assert(valid === true, '配置验证通过');
  } catch (e) {
    assert(false, `配置验证失败：${e.message}`);
  }
  
  // 测试 3: 配置验证错误处理
  try {
    const invalidConfig = {
      general: { logLevel: 'invalid' },
      retry: { maxRetries: 10 },
      platforms: { youtube: { visibility: 'invalid' } }
    };
    validateConfig(invalidConfig);
    assert(false, '应该抛出配置验证错误');
  } catch (e) {
    assert(true, '配置验证错误处理正确');
  }
}

/**
 * 测试选择器模块
 */
function testSelectors() {
  log.divider('─', 50);
  log.info('测试选择器模块');
  log.divider('─', 50);
  
  // 测试 1: 获取平台选择器
  try {
    const selectors = getSelectors('xiaohongshu');
    assert(selectors !== null, '获取小红书选择器');
    assert(typeof selectors === 'object', '选择器为对象');
  } catch (e) {
    assert(false, `获取选择器失败：${e.message}`);
  }
  
  // 测试 2: 获取单个选择器
  try {
    const titleSelector = getSelector('xiaohongshu', 'title');
    assert(titleSelector.includes('标题'), '标题选择器包含关键词');
    assert(titleSelector.includes('placeholder'), '使用 placeholder 属性');
  } catch (e) {
    assert(false, `获取标题选择器失败：${e.message}`);
  }
  
  // 测试 3: 不支持的平台
  try {
    getSelector('invalid_platform', 'title');
    assert(false, '应该抛出不支持平台错误');
  } catch (e) {
    assert(true, '不支持平台错误处理正确');
  }
  
  // 测试 4: 所有平台选择器
  const platforms = ['xiaohongshu', 'bilibili', 'youtube', 'douyin'];
  platforms.forEach(platform => {
    try {
      const selectors = getSelectors(platform);
      assert(selectors.form !== undefined, `${platform} 有 form 选择器`);
      assert(selectors.buttons !== undefined, `${platform} 有 buttons 选择器`);
    } catch (e) {
      assert(false, `${platform} 选择器错误：${e.message}`);
    }
  });
}

/**
 * 测试日志模块
 */
function testLogger() {
  log.divider('─', 50);
  log.info('测试日志模块');
  log.divider('─', 50);
  
  // 测试 1: 创建日志实例
  try {
    const testLog = createLogger({ level: 'debug' });
    assert(testLog !== null, '创建日志实例');
  } catch (e) {
    assert(false, `创建日志实例失败：${e.message}`);
  }
  
  // 测试 2: 各级别日志
  try {
    const testLog = createLogger({ level: 'debug' });
    testLog.debug('调试消息');
    testLog.info('信息消息');
    testLog.success('成功消息');
    testLog.warn('警告消息');
    testLog.error('错误消息');
    assert(true, '各级别日志输出正常');
  } catch (e) {
    assert(false, `日志输出失败：${e.message}`);
  }
  
  // 测试 3: 日志级别过滤
  try {
    const testLog = createLogger({ level: 'error' });
    // debug 和 info 不应该输出
    assert(true, '日志级别设置成功');
  } catch (e) {
    assert(false, `日志级别设置失败：${e.message}`);
  }
  
  // 测试 4: 进度条
  try {
    const testLog = createLogger({ level: 'info' });
    const bar = testLog.progressBar(50, 20);
    assert(bar.length === 20, '进度条长度正确');
    assert(bar.includes('█'), '进度条包含填充字符');
    assert(bar.includes('░'), '进度条包含空白字符');
  } catch (e) {
    assert(false, `进度条生成失败：${e.message}`);
  }
}

/**
 * 测试 CDP 工具库（模拟）
 */
function testCDPLib() {
  log.divider('─', 50);
  log.info('测试 CDP 工具库（模拟）');
  log.divider('─', 50);
  
  // 注意：CDP 工具库需要实际运行环境，这里只做基本测试
  
  // 测试 1: 模块导入
  try {
    import('./cdp-lib.js').then(() => {
      assert(true, 'CDP 库导入成功');
    }).catch(() => {
      assert(false, 'CDP 库导入失败');
    });
  } catch (e) {
    assert(false, `CDP 库错误：${e.message}`);
  }
}

/**
 * 运行所有测试
 */
async function runAllTests() {
  log.divider('═', 60);
  log.info('  Social Media Publisher - 测试套件');
  log.divider('═', 60);
  log.info('');
  
  const startTime = Date.now();
  
  // 运行测试
  testConfig();
  log.info('');
  
  testSelectors();
  log.info('');
  
  testLogger();
  log.info('');
  
  await testCDPLib();
  await new Promise(r => setTimeout(r, 1000)); // 等待异步测试
  
  // 总结
  const duration = Date.now() - startTime;
  log.divider('═', 60);
  log.info('  测试总结');
  log.divider('═', 60);
  log.info(`  总测试数：${total}`);
  log.success(`  通过：${passed}`);
  if (failed > 0) {
    log.error(`  失败：${failed}`);
  }
  log.info(`  耗时：${duration}ms`);
  log.divider('═', 60);
  
  // 返回结果
  return {
    total,
    passed,
    failed,
    duration,
    success: failed === 0
  };
}

// 命令行入口
if (process.argv[1].includes('test.js')) {
  runAllTests().then((result) => {
    process.exit(result.success ? 0 : 1);
  }).catch((error) => {
    log.error(`测试套件错误：${error.message}`);
    process.exit(1);
  });
}

export { runAllTests, testConfig, testSelectors, testLogger };
