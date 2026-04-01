#!/usr/bin/env node
const WebSocket = require('ws');

const targetId = process.argv[2];
const wsUrl = `ws://127.0.0.1:18800/devtools/page/${targetId}`;

const ws = new WebSocket(wsUrl);

ws.on('open', () => {
    console.log('🔗 连接到 WhatsApp Web');
    
    ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.enable'
    }));
    
    // 简单测试：获取页面标题
    ws.send(JSON.stringify({
        id: 2,
        method: 'Runtime.evaluate',
        params: {
            expression: 'document.title'
        }
    }));
});

ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.id === 2 && msg.result?.result?.value) {
        console.log('✅ WhatsApp Web 页面标题:', msg.result.result.value);
        console.log('\n📱 请在浏览器中手动发送测试消息：');
        console.log('1. 搜索号码：+86XXXXXXXXXXX');
        console.log('2. 发送消息：1688 价格监控测试');
        console.log('\n完成后我会继续配置自动监控。\n');
        ws.close();
    }
});

ws.on('error', (err) => {
    console.error('❌', err.message);
    process.exit(1);
});
