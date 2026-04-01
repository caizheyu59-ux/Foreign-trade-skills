#!/usr/bin/env node
/**
 * 1688 价格监控 - 价格提醒脚本
 * 功能：
 * 1. 批量监控配置的商品价格
 * 2. 检测价格变化
 * 3. 发送 WhatsApp 通知
 */

const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG_PATH = path.join(__dirname, 'config', 'monitored-products.json');
const DATA_PATH = path.join(__dirname, 'data', 'price-history.csv');
const ALERT_LOG_PATH = path.join(__dirname, 'data', 'alert-log.json');

class PriceAlert {
    constructor() {
        this.config = this.loadConfig();
        this.history = this.loadHistory();
        this.alerts = this.loadAlerts();
    }

    loadConfig() {
        const data = fs.readFileSync(CONFIG_PATH, 'utf-8');
        return JSON.parse(data);
    }

    loadHistory() {
        if (!fs.existsSync(DATA_PATH)) {
            return {};
        }
        
        const csv = fs.readFileSync(DATA_PATH, 'utf-8');
        const lines = csv.trim().split('\n');
        const history = {};
        
        // 跳过表头
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i];
            const parts = line.split(',');
            if (parts.length >= 4) {
                const url = parts[1];
                const price = parseFloat(parts[3]) || 0;
                const timestamp = parts[0];
                
                // 保留最新价格
                if (!history[url] || timestamp > history[url].timestamp) {
                    history[url] = { price, timestamp };
                }
            }
        }
        
        return history;
    }

    loadAlerts() {
        if (!fs.existsSync(ALERT_LOG_PATH)) {
            return [];
        }
        return JSON.parse(fs.readFileSync(ALERT_LOG_PATH, 'utf-8'));
    }

    saveAlerts() {
        fs.writeFileSync(ALERT_LOG_PATH, JSON.stringify(this.alerts, null, 2));
    }

    /**
     * 获取页面 targetId
     */
    async getTargetId(url) {
        try {
            // 使用 browser 工具打开页面
            const result = execSync(
                `openclaw browser open "${url}" --profile openclaw`,
                { encoding: 'utf-8', stdio: 'pipe' }
            );
            
            // 解析返回的 JSON
            const data = JSON.parse(result);
            return data.targetId;
        } catch (e) {
            console.error(`❌ 打开页面失败：${url}`);
            console.error(e.message);
            return null;
        }
    }

    /**
     * 抓取商品价格
     */
    async fetchPrice(targetId) {
        return new Promise((resolve) => {
            const wsUrl = `ws://127.0.0.1:18800/devtools/page/${targetId}`;
            const ws = new WebSocket(wsUrl);
            
            let resolved = false;
            
            ws.on('open', () => {
                ws.send(JSON.stringify({
                    id: 1,
                    method: 'Runtime.enable'
                }));
                
                ws.send(JSON.stringify({
                    id: 2,
                    method: 'Runtime.evaluate',
                    params: {
                        expression: `(() => {
                            const result = {
                                title: document.querySelector('h1, .title, .product-name')?.innerText?.trim() || 'N/A',
                                price: null
                            };
                            
                            const priceSelectors = ['.price-title', '.offer-price', '[data-price]', '.price', '.current-price'];
                            for (const sel of priceSelectors) {
                                const el = document.querySelector(sel);
                                if (el && el.innerText.trim()) {
                                    const priceText = el.innerText.trim();
                                    const match = priceText.match(/[¥￥]\\s*(\\d+\\.?\\d*)/);
                                    if (match) {
                                        result.price = parseFloat(match[1]);
                                        break;
                                    }
                                }
                            }
                            
                            return JSON.stringify(result);
                        })()`
                    }
                }));
            });
            
            ws.on('message', (data) => {
                if (resolved) return;
                
                const msg = JSON.parse(data);
                if (msg.id === 2 && msg.result?.result?.value) {
                    try {
                        const info = JSON.parse(msg.result.result.value);
                        resolve(info);
                        resolved = true;
                    } catch (e) {
                        resolve({ title: 'Error', price: null });
                        resolved = true;
                    }
                }
            });
            
            ws.on('error', () => {
                if (!resolved) {
                    resolve({ title: 'Error', price: null });
                    resolved = true;
                }
            });
            
            // 超时处理
            setTimeout(() => {
                if (!resolved) {
                    resolve({ title: 'Timeout', price: null });
                    resolved = true;
                }
                ws.close();
            }, 10000);
        });
    }

    /**
     * 检测价格变化
     */
    checkPriceChange(product, currentPrice) {
        const oldPrice = this.history[product.url]?.price;
        
        if (!oldPrice) {
            return { changed: false, reason: '首次监控' };
        }
        
        const change = currentPrice - oldPrice;
        const changePercent = (change / oldPrice) * 100;
        const threshold = product.notify_threshold || this.config.settings.notify_threshold || 10;
        
        // 检测是否超过阈值
        if (Math.abs(changePercent) >= threshold) {
            return {
                changed: true,
                oldPrice,
                currentPrice,
                change,
                changePercent,
                direction: change > 0 ? '上涨' : '下降',
                reason: `价格${change > 0 ? '上涨' : '下降'}${Math.abs(changePercent).toFixed(1)}%`
            };
        }
        
        // 检测是否低于目标价格
        if (product.target_price && currentPrice <= product.target_price) {
            return {
                changed: true,
                oldPrice,
                currentPrice,
                change,
                changePercent,
                direction: '目标价',
                reason: `价格降至目标价 ¥${product.target_price} 以下！`
            };
        }
        
        return { changed: false, reason: '变化在阈值内' };
    }

    /**
     * 发送 WhatsApp 消息
     */
    async sendWhatsApp(message) {
        try {
            // 使用 OpenClaw message 工具发送
            const cmd = `openclaw message send --target whatsapp --message "${message.replace(/"/g, '\\"')}"`;
            execSync(cmd, { encoding: 'utf-8', stdio: 'pipe' });
            console.log('✅ WhatsApp 消息已发送');
            return true;
        } catch (e) {
            console.error('❌ WhatsApp 发送失败:', e.message);
            return false;
        }
    }

    /**
     * 格式化 WhatsApp 消息
     */
    formatAlert(product, change) {
        const emoji = change.direction === '下降' ? '📉' : change.direction === '目标价' ? '🎯' : '📈';
        
        return `
${emoji} *1688 价格提醒*

📦 商品：${product.name}
💰 当前价格：¥${change.currentPrice}
📊 原价：¥${change.oldPrice}
📈 变化：${change.changePercent > 0 ? '+' : ''}${change.changePercent.toFixed(1)}%
🔗 链接：${product.url}

${change.reason}
        `.trim();
    }

    /**
     * 保存价格记录
     */
    savePriceRecord(product, priceInfo) {
        const exists = fs.existsSync(DATA_PATH);
        const csvLine = `${new Date().toISOString()},${product.url},"${priceInfo.title}",${priceInfo.price || 0},,,\n`;
        
        if (!exists) {
            fs.writeFileSync(DATA_PATH, 'timestamp,target_id,product_name,price,price_range,min_order,supplier\n');
        }
        fs.appendFileSync(DATA_PATH, csvLine);
    }

    /**
     * 执行监控
     */
    async monitor() {
        console.log('\n' + '='.repeat(60));
        console.log('🔍 开始 1688 价格监控');
        console.log(`📦 监控商品数：${this.config.products.length}`);
        console.log('='.repeat(60) + '\n');
        
        const alerts = [];
        
        for (const product of this.config.products) {
            console.log(`\n📦 检查：${product.name}`);
            
            // 抓取价格
            console.log('  🔍 抓取价格中...');
            const priceInfo = await this.fetchPrice(product.targetId);
            
            if (!priceInfo.price) {
                console.log('  ⚠️ 无法获取价格，跳过');
                continue;
            }
            
            console.log(`  💰 当前价格：¥${priceInfo.price}`);
            
            // 保存记录
            this.savePriceRecord(product, priceInfo);
            
            // 检测变化
            const change = this.checkPriceChange(product, priceInfo.price);
            
            if (change.changed) {
                console.log(`  ⚠️ ${change.reason}`);
                
                // 检查是否已发送过相同提醒（避免重复）
                const alertKey = `${product.id}-${Date.now()}`;
                const recentAlert = this.alerts.find(a => 
                    a.productId === product.id && 
                    (Date.now() - a.timestamp < 3600000) // 1 小时内不重复
                );
                
                if (!recentAlert) {
                    // 格式化消息
                    const message = this.formatAlert(product, change);
                    
                    // 发送 WhatsApp
                    const sent = await this.sendWhatsApp(message);
                    
                    if (sent) {
                        this.alerts.push({
                            productId: product.id,
                            productName: product.name,
                            timestamp: Date.now(),
                            oldPrice: change.oldPrice,
                            newPrice: change.currentPrice,
                            changePercent: change.changePercent
                        });
                        
                        alerts.push({
                            product: product.name,
                            message,
                            sent: true
                        });
                    }
                } else {
                    console.log('  ⏭️ 1 小时内已发送过提醒，跳过');
                }
            } else {
                console.log(`  ✅ ${change.reason}`);
            }
        }
        
        // 保存提醒记录
        this.saveAlerts();
        
        // 汇总报告
        console.log('\n' + '='.repeat(60));
        console.log('📊 监控完成');
        console.log(`📦 检查商品：${this.config.products.length}`);
        console.log(`⚠️ 价格变化：${alerts.length}`);
        console.log('='.repeat(60) + '\n');
        
        return alerts;
    }
}

// 主函数
async function main() {
    const alert = new PriceAlert();
    
    try {
        const results = await alert.monitor();
        
        if (results.length > 0) {
            console.log('📋 发送的提醒:');
            results.forEach(r => {
                console.log(`  - ${r.product}`);
            });
        }
        
        process.exit(0);
    } catch (e) {
        console.error('❌ 监控失败:', e.message);
        console.error(e.stack);
        process.exit(1);
    }
}

// 导出给其他模块使用
module.exports = PriceAlert;

// 命令行执行
if (require.main === module) {
    main();
}
