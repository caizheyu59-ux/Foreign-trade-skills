/**
 * 平台选择器配置
 * 使用稳定的属性选择器，避免使用动态 class 和 CSS 路径
 */

export const platformSelectors = {
  // ==================== 小红书 ====================
  xiaohongshu: {
    // 页面结构
    tabs: {
      video: '[role="tab"]:has-text("上传视频")',
      image: '[role="tab"]:has-text("上传图文")',
      article: '[role="tab"]:has-text("写长文")'
    },
    
    // 表单元素 - 使用 placeholder 属性（稳定）
    form: {
      file: 'input[type="file"]',  // 文件上传
      title: 'input[placeholder*="标题"]',  // 标题（不依赖具体文字）
      description: 'div[contenteditable="true"]',  // 描述编辑器
      tags: 'input[placeholder*="话题"], input[placeholder*="标签"]'  // 标签
    },
    
    // 按钮 - 使用文字匹配
    buttons: {
      save: '[class*="暂存"]',  // 暂存离开
      publish: '[class*="发布"], button[type="submit"]',  // 发布
      confirm: '[class*="确认"]'  // 确认按钮
    }
  },
  
  // ==================== B 站 ====================
  bilibili: {
    // 表单元素
    form: {
      file: 'input[type="file"]',
      title: 'input[placeholder="请输入稿件标题"]',
      description: '.ql-editor',  // Quill 编辑器（稳定 class）
      tags: 'input[placeholder*="标签"]',
      category: '.select-zone, [class*="分区"]'
    },
    
    // 按钮
    buttons: {
      submit: 'button[type="submit"], [class*="提交"]',
      save: '[class*="保存草稿"]'
    }
  },
  
  // ==================== YouTube ====================
  youtube: {
    // 表单元素
    form: {
      file: 'input[type="file"]',
      title: '#textbox:first-of-type',  // 第一个 textbox
      description: '#textbox:nth-of-type(2)',  // 第二个 textbox
      audience: '[name*="MADE_FOR_KIDS"]'  // 受众选择
    },
    
    // 按钮
    buttons: {
      next: '[next-button], [class*="next"]',
      publish: '#publish-button, [class*="publish"]'
    }
  },
  
  // ==================== 抖音 ====================
  douyin: {
    // 表单元素
    form: {
      file: 'input[type="file"]',
      title: 'input[placeholder*="标题"]',  // 不依赖完整文字
      description: 'div[contenteditable="true"]',
      cover: '[class*="封面"]'
    },
    
    // 按钮
    buttons: {
      publish: 'button:has-text("发布"), button:has-text("高清发布")',
      save: '[class*="暂存"]'
    }
  }
};

/**
 * 获取平台选择器
 * @param {string} platform - 平台名称
 * @param {string} category - 类别（form/buttons/tabs）
 * @returns {object} 选择器对象
 */
export function getSelectors(platform, category = 'form') {
  const platformConfig = platformSelectors[platform];
  if (!platformConfig) {
    throw new Error(`不支持的平台：${platform}`);
  }
  
  return platformConfig[category] || {};
}

/**
 * 获取单个选择器
 * @param {string} platform - 平台名称
 * @param {string} key - 选择器键名
 * @returns {string} CSS 选择器
 */
export function getSelector(platform, key) {
  const selectors = getSelectors(platform);
  const selector = selectors[key];
  
  if (!selector) {
    throw new Error(`未找到选择器：${platform}.${key}`);
  }
  
  return selector;
}

/**
 * 选择器版本管理
 * 当平台 UI 更新时，可以切换版本
 */
export const selectorVersions = {
  xiaohongshu: {
    v1: {
      // 旧版本选择器（保留作为备份）
      title: 'input[placeholder*="填写标题"]'
    },
    v2: {
      // 当前版本选择器
      title: 'input[placeholder*="标题"]'
    },
    current: 'v2'  // 当前使用的版本
  }
};

/**
 * 获取指定版本的选择器
 */
export function getVersionedSelector(platform, key, version = null) {
  const versionConfig = selectorVersions[platform];
  if (!versionConfig) {
    return getSelector(platform, key);
  }
  
  const targetVersion = version || versionConfig.current;
  return versionConfig[targetVersion]?.[key] || getSelector(platform, key);
}
