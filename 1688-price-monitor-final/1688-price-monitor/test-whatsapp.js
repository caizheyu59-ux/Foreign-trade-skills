#!/usr/bin/env node
/**
 * 测试 WhatsApp 通知
 * 用法：node test-whatsapp.js +8613800138000
 */

const { execSync } = require('child_process');

const phoneNumber = process.argv[2];

if (!phoneNumber) {
    console.log(`
📱 WhatsApp 测试工具

用法：node test-whatsapp.js <手机号码>

示例：
  node test-whatsapp.js +8613800138000

注意：手机号码需要带国家码（如 +86 表示中国）
`);
    process.exit(1);
}

const testMessage = `
🍔 1688 价格监控测试

✅ 连接成功！

这是测试消息，如果你收到这条消息，说明 WhatsApp 通知已配置成功。

下一步：
1. 编辑 config/monitored-products.json 添加监控商品
2. 运行 node price-alert.js 开始监控
3. 价格变化将自动推送到此 WhatsApp

---
1688 Price Monitor v1.0
`.trim();

console.log(`\n📱 发送测试消息到：${phoneNumber}`);
console.log('📤 消息内容：');
console.log(testMessage);
console.log('\n发送中...\n');

try {
    // 使用 openclaw message 发送
    const escapedMessage = testMessage.replace(/"/g, '\\"').replace(/\n/g, '\\n');
    const cmd = `openclaw message send --target "${phoneNumber}" --message "${escapedMessage}"`;
    
    execSync(cmd, {
        encoding: 'utf-8',
        stdio: 'inherit'
    });
    
    console.log('\n✅ 测试消息已发送！请检查 WhatsApp。\n');
    process.exit(0);
} catch (e) {
    console.error('\n❌ 发送失败：', e.message);
    console.error('\n可能原因：');
    console.error('1. WhatsApp 未连接 - 运行 openclaw message status 检查状态');
    console.error('2. 手机号码格式错误 - 确保带国家码（如 +8613800138000）');
    console.error('3. 网络连接问题\n');
    process.exit(1);
}
