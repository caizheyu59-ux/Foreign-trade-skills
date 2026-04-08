/**
 * 配置文件
 * 用户可以自定义上传设置
 */

export const defaultConfig = {
  // ==================== 通用设置 ====================
  general: {
    // 日志级别：'debug' | 'info' | 'warn' | 'error'
    logLevel: 'info',
    
    // 是否保存进度文件
    saveProgress: true,
    
    // 进度文件路径
    progressFile: '.upload-state.json',
    
    // 超时设置（毫秒）
    timeouts: {
      pageLoad: 30000,      // 页面加载
      fileUpload: 60000,    // 文件上传
      operation: 10000      // 单个操作
    }
  },
  
  // ==================== 重试设置 ====================
  retry: {
    // 最大重试次数
    maxRetries: 2,
    
    // 重试间隔（毫秒）
    delayMs: 1000,
    
    // 是否递增延迟（每次重试增加延迟）
    exponentialBackoff: false
  },
  
  // ==================== 平台特定设置 ====================
  platforms: {
    // 小红书
    xiaohongshu: {
      // 自动保存草稿
      autoSave: true,
      
      // 保存前等待时间（毫秒）
      saveDelay: 2000,
      
      // 标签数量限制
      maxTags: 10,
      
      // 标题长度限制
      titleMaxLength: 20
    },
    
    // B 站
    bilibili: {
      // 默认分区 ID
      defaultCategory: null,
      
      // 默认标签
      defaultTags: [],
      
      // 是否开启弹幕
      enableDanmaku: true
    },
    
    // YouTube
    youtube: {
      // 可见性：'private' | 'unlisted' | 'public'
      visibility: 'private',
      
      // 受众设置：'not_made_for_kids' | 'made_for_kids'
      audience: 'not_made_for_kids',
      
      // 是否允许评论
      allowComments: true,
      
      // 是否允许评分
      allowRatings: true
    },
    
    // 抖音
    douyin: {
      // 自动选择封面
      autoSelectCover: false,
      
      // 封面索引（0 = 第一个）
      coverIndex: 0,
      
      // 是否同步到头条
      syncToToutiao: false,
      
      // 标签数量限制
      maxTags: 5
    }
  },
  
  // ==================== 内容设置 ====================
  content: {
    // 自动截断超长描述
    truncateDescription: true,
    
    // 描述最大长度（0 = 不限制）
    maxDescriptionLength: 1000,
    
    // 标签前缀（自动添加）
    tagPrefix: '',
    
    // 标签后缀（自动添加）
    tagSuffix: ''
  },
  
  // ==================== 文件设置 ====================
  files: {
    // 临时目录
    tempDir: '.temp',
    
    // 截图保存
    saveScreenshots: true,
    
    // 截图目录
    screenshotDir: 'screenshots',
    
    // 日志文件
    logFile: 'upload.log'
  }
};

/**
 * 用户配置（可以覆盖默认配置）
 * 复制并修改此对象到 user-config.js
 */
export const userConfig = {
  // 示例：修改日志级别
  // general: {
  //   logLevel: 'debug'
  // },
  
  // 示例：修改 YouTube 默认可见性
  // platforms: {
  //   youtube: {
  //     visibility: 'unlisted'
  //   }
  // }
};

/**
 * 合并配置
 */
function mergeConfig(defaults, user) {
  const result = { ...defaults };
  
  for (const key in user) {
    if (user[key] instanceof Object && defaults[key] instanceof Object) {
      result[key] = mergeConfig(defaults[key], user[key]);
    } else {
      result[key] = user[key];
    }
  }
  
  return result;
}

/**
 * 获取最终配置
 */
export function getConfig() {
  return mergeConfig(defaultConfig, userConfig);
}

/**
 * 验证配置
 */
export function validateConfig(config) {
  const errors = [];
  
  // 验证日志级别
  const validLevels = ['debug', 'info', 'warn', 'error'];
  if (!validLevels.includes(config.general.logLevel)) {
    errors.push(`Invalid log level: ${config.general.logLevel}`);
  }
  
  // 验证 YouTube 可见性
  const validVisibility = ['private', 'unlisted', 'public'];
  if (!validVisibility.includes(config.platforms.youtube.visibility)) {
    errors.push(`Invalid YouTube visibility: ${config.platforms.youtube.visibility}`);
  }
  
  // 验证重试次数
  if (config.retry.maxRetries < 0 || config.retry.maxRetries > 5) {
    errors.push(`Invalid retry count: ${config.retry.maxRetries}`);
  }
  
  if (errors.length > 0) {
    throw new Error(`配置验证失败：\n${errors.join('\n')}`);
  }
  
  return true;
}
