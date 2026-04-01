#!/usr/bin/env node
/**
 * 通过 WhatsApp Web CDP 发送消息
 * 用法：node send-whatsapp-cdp.js +86XXXXXXXXXXX "消息内容"
 */

const WebSocket = require('ws');
const { execSync } = require('child_process');

const phoneNumber = process.argv[2] || '+86XXXXXXXXXXX';
const message = process.argv[3] || '🍔 1688 价格监控测试消息';

// 获取 WhatsApp Web 的 targetId
function getWhatsAppTargetId() {
    try {
        const result = execSync('curl -s http://127.0.0.1:18800/json/list', { encoding: 'utf-8' });
        const tabs = JSON.parse(result);
        const waTab = tabs.find(t => t.url.includes('web.whatsapp.com'));
        return waTab ? waTab.id : null;
    } catch (e) {
        console.error('❌ 无法获取 WhatsApp Web 标签页');
        return null;
    }
}

async function sendMessageViaWhatsApp(targetId, phone, msg) {
    return new Promise((resolve) => {
        const wsUrl = `ws://127.0.0.1:18800/devtools/page/${targetId}`;
        const ws = new WebSocket(wsUrl);
        
        ws.on('open', () => {
            console.log('🔗 连接到 WhatsApp Web');
            
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.enable'
            }));
            
            // 执行 JavaScript 发送消息
            ws.send(JSON.stringify({
                id: 2,
                method: 'Runtime.evaluate',
                params: {
                    expression: `(async () => {
                        try {
                            // 检查是否在聊天列表页面
                            const searchBox = document.querySelector('[contenteditable="true"][data-tab="3"]');
                            if (!searchBox) {
                                return { success: false, error: '未找到搜索框' };
                            }
                            
                            // 搜索联系人
                            searchBox.focus();
                            searchBox.innerText = '${phone}';
                            searchBox.dispatchEvent(new Event('input', { bubbles: true }));
                            
                            // 等待搜索结果
                            await new Promise(r => setTimeout(r, 2000));
                            
                            // 点击第一个搜索结果
                            const firstResult = document.querySelector('[role="listitem"]');
                            if (!firstResult) {
                                return { success: false, error: '未找到联系人' };
                            }
                            firstResult.click();
                            
                            // 等待聊天打开
                            await new Promise(r => setTimeout(r, 2000));
                            
                            // 找到消息输入框
                            const messageBox = document.querySelector('[contenteditable="true"][data-tab="10"]');
                            if (!messageBox) {
                                return { success: false, error: '未找到消息输入框' };
                            }
                            
                            // 输入消息
                            messageBox.focus();
                            messageBox.innerText = \`${msg}\`;
                            messageBox.dispatchEvent(new Event('input', { bubbles: true }));
                            
                            // 等待发送按钮
                            await new Promise(r => setTimeout(r, 500));
                            
                            // 点击发送按钮
                            const sendButton = document.querySelector('[data-testid="send"]');
                            if (sendButton) {
                                sendButton.click();
                                return { success: true, message: '消息已发送' };
                            }
                            
                            // 或者按 Enter 发送
                            messageBox.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
                            return { success: true, message: '消息已发送（Enter）' };
                            
                        } catch (e) {
                            return { success: false, error: e.message };
                        }
                    })()`
                }
            }));
        });
        
        ws.on('message', (data) => {
            const msg = JSON.parse(data);
            if (msg.id === 2 && msg.result) {
                if (msg.result.result.value) {
                    try {
                        const result = JSON.parse(msg.result.result.value);
                        if (result.success) {
                            console.log('✅', result.message);
                            resolve(true);
                        } else {
                            console.error('❌', result.error);
                            resolve(false);
                        }
                    } catch (e) {
                        console.error('解析失败:', e.message);
                        resolve(false);
                    }
                }
                ws.close();
            }
        });
        
        ws.on('error', (err) => {
            console.error('❌ WebSocket 错误:', err.message);
            resolve(false);
        });
        
        setTimeout(() => {
            ws.close();
            resolve(false);
        }, 15000);
    });
}

async function main() {
    console.log('\n📱 WhatsApp 消息发送工具');
    console.log('='.repeat(60));
    console.log('收件人:', phoneNumber);
    console.log('消息:', message.substring(0, 50) + '...');
    console.log('='.repeat(60) + '\n');
    
    const targetId = getWhatsAppTargetId();
    
    if (!targetId) {
        console.log('❌ 未找到 WhatsApp Web 标签页');
        console.log('\n请先在浏览器中打开 https://web.whatsapp.com 并登录');
        process.exit(1);
    }
    
    console.log('🔍 找到 WhatsApp Web 标签页:', targetId);
    
    const success = await sendMessageViaWhatsApp(targetId, phoneNumber, message);
    
    if (success) {
        console.log('\n✅ 消息发送成功！\n');
        process.exit(0);
    } else {
        console.log('\n❌ 消息发送失败\n');
        console.log('提示：请确保 WhatsApp Web 已登录且页面可见');
        process.exit(1);
    }
}

main();
