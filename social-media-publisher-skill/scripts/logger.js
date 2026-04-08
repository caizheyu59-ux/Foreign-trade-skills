/**
 * 日志工具
 * 提供详细的日志输出和文件记录
 */

import fs from 'fs';
import path from 'path';

// 日志级别
const LOG_LEVELS = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3
};

// 日志图标
const LOG_ICONS = {
  debug: '🔍',
  info: 'ℹ️',
  success: '✅',
  warn: '⚠️',
  error: '❌'
};

class Logger {
  constructor(options = {}) {
    this.level = options.level || 'info';
    this.logFile = options.logFile || null;
    this.saveToFile = options.saveToFile || false;
    
    // 创建日志目录
    if (this.saveToFile && this.logFile) {
      const dir = path.dirname(this.logFile);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    }
  }
  
  /**
   * 格式化时间戳
   */
  formatTimestamp() {
    return new Date().toISOString().split('T')[1].split('.')[0];
  }
  
  /**
   * 写入日志文件
   */
  writeToFile(message) {
    if (this.saveToFile && this.logFile) {
      fs.appendFileSync(this.logFile, `${new Date().toISOString()} ${message}\n`);
    }
  }
  
  /**
   * 日志输出
   */
  log(level, message, data = null) {
    const levelValue = LOG_LEVELS[level];
    const currentLevelValue = LOG_LEVELS[this.level];
    
    // 检查日志级别
    if (levelValue < currentLevelValue) {
      return;
    }
    
    const timestamp = this.formatTimestamp();
    const icon = LOG_ICONS[level] || LOG_ICONS.info;
    
    // 格式化消息
    let logMessage = `${icon} [${timestamp}] ${message}`;
    if (data) {
      logMessage += `\n   ${JSON.stringify(data, null, 2)}`;
    }
    
    // 输出到控制台
    console.log(logMessage);
    
    // 写入文件
    this.writeToFile(logMessage);
  }
  
  /**
   * 调试日志
   */
  debug(message, data) {
    this.log('debug', message, data);
  }
  
  /**
   * 信息日志
   */
  info(message, data) {
    this.log('info', message, data);
  }
  
  /**
   * 成功日志
   */
  success(message, data) {
    this.log('success', message, data);
  }
  
  /**
   * 警告日志
   */
  warn(message, data) {
    this.log('warn', message, data);
  }
  
  /**
   * 错误日志
   */
  error(message, data) {
    this.log('error', message, data);
  }
  
  /**
   * 开始步骤
   */
  stepStart(stepName, stepNumber, totalSteps) {
    this.info(`步骤 ${stepNumber}/${totalSteps}: ${stepName}`);
  }
  
  /**
   * 完成步骤
   */
  stepComplete(stepName, duration = null) {
    let message = `完成：${stepName}`;
    if (duration) {
      message += ` (${duration}ms)`;
    }
    this.success(message);
  }
  
  /**
   * 失败步骤
   */
  stepFailed(stepName, error, retryCount = 0) {
    let message = `失败：${stepName}`;
    if (retryCount > 0) {
      message += ` (重试 ${retryCount} 次)`;
    }
    this.error(message, { error: error.message });
  }
  
  /**
   * 进度日志
   */
  progress(current, total, message = '') {
    const percentage = Math.round((current / total) * 100);
    const bar = this.progressBar(percentage);
    this.info(`${bar} ${percentage}% ${message}`);
  }
  
  /**
   * 进度条
   */
  progressBar(percentage, width = 20) {
    const filled = Math.round((percentage / 100) * width);
    const empty = width - filled;
    return '[' + '█'.repeat(filled) + '░'.repeat(empty) + ']';
  }
  
  /**
   * 分隔线
   */
  divider(char = '─', length = 50) {
    console.log(char.repeat(length));
  }
  
  /**
   * 总结
   */
  summary(stats) {
    this.divider();
    this.info('📊 执行总结');
    this.divider('─', 30);
    
    for (const [key, value] of Object.entries(stats)) {
      this.info(`  ${key}: ${value}`);
    }
    
    this.divider();
  }
}

/**
 * 创建日志实例
 */
export function createLogger(options = {}) {
  return new Logger(options);
}

/**
 * 全局日志实例
 */
export const logger = createLogger();

/**
 * 性能计时
 */
export class PerformanceTimer {
  constructor(logger, name) {
    this.logger = logger;
    this.name = name;
    this.startTime = Date.now();
  }
  
  /**
   * 结束计时
   */
  end() {
    const duration = Date.now() - this.startTime;
    this.logger.debug(`${this.name} 耗时：${duration}ms`);
    return duration;
  }
}

/**
 * 计时装饰器
 */
export async function timed(logger, name, fn) {
  const timer = new PerformanceTimer(logger, name);
  try {
    const result = await fn();
    timer.end();
    return result;
  } catch (error) {
    timer.end();
    throw error;
  }
}
