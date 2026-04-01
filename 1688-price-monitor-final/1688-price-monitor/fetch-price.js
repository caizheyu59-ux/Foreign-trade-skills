const WebSocket = require('ws');

const targetId = process.argv[2];
const wsUrl = `ws://127.0.0.1:18800/devtools/page/${targetId}`;

const ws = new WebSocket(wsUrl);

ws.on('open', () => {
    console.log('🔗 Connected to CDP');
    
    ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.enable'
    }));
    
    // Execute JavaScript to extract price
    ws.send(JSON.stringify({
        id: 2,
        method: 'Runtime.evaluate',
        params: {
            expression: `(() => {
                const result = {
                    title: document.querySelector('h1, .title, .product-name')?.innerText?.trim() || 'N/A',
                    price: null,
                    priceRange: null,
                    minOrder: null,
                    supplier: null,
                    rawHtml: document.body.innerHTML.substring(0, 5000)
                };
                
                // Try to find price with multiple selectors
                const priceSelectors = ['.price-title', '.offer-price', '[data-price]', '.price', '.current-price'];
                for (const sel of priceSelectors) {
                    const el = document.querySelector(sel);
                    if (el && el.innerText.trim()) {
                        result.price = el.innerText.trim();
                        break;
                    }
                }
                
                // Try to find price range
                const rangeEl = document.querySelector('.price-range, .sku-price');
                if (rangeEl) {
                    result.priceRange = rangeEl.innerText.trim();
                }
                
                // Try to find min order
                const moqSelectors = ['.min-order', '.moq', '.start-amount'];
                for (const sel of moqSelectors) {
                    const el = document.querySelector(sel);
                    if (el && el.innerText.trim()) {
                        result.minOrder = el.innerText.trim();
                        break;
                    }
                }
                
                // Try to find supplier
                const supplierSelectors = ['.supplier-name', '.company-name', '.seller-info'];
                for (const sel of supplierSelectors) {
                    const el = document.querySelector(sel);
                    if (el && el.innerText.trim()) {
                        result.supplier = el.innerText.trim();
                        break;
                    }
                }
                
                return JSON.stringify(result);
            })()`
        }
    }));
});

ws.on('message', (data) => {
    const msg = JSON.parse(data);
    
    if (msg.id === 2 && msg.result && msg.result.result) {
        console.log('\n📊 1688 商品价格信息');
        console.log('=' .repeat(60));
        
        if (msg.result.result.value) {
            try {
                const info = JSON.parse(msg.result.result.value);
                console.log('📦 商品标题:', info.title);
                console.log('💰 价格:', info.price || '未找到');
                console.log('📈 价格区间:', info.priceRange || 'N/A');
                console.log('📋 最小起订:', info.minOrder || 'N/A');
                console.log('🏭 供应商:', info.supplier || 'N/A');
                console.log('=' .repeat(60));
                
                // Save to CSV
                const fs = require('fs');
                const path = require('path');
                const csvPath = path.join(__dirname, 'data', 'price-history.csv');
                
                if (!fs.existsSync(path.dirname(csvPath))) {
                    fs.mkdirSync(path.dirname(csvPath), { recursive: true });
                }
                
                const exists = fs.existsSync(csvPath);
                const csvLine = `${new Date().toISOString()},${targetId},"${info.title}",${info.price},"${info.priceRange || ''}","${info.minOrder || ''}","${info.supplier || ''}"\n`;
                
                if (!exists) {
                    fs.writeFileSync(csvPath, 'timestamp,target_id,product_name,price,price_range,min_order,supplier\n');
                }
                fs.appendFileSync(csvPath, csvLine);
                
                console.log('\n💾 已保存到:', csvPath);
            } catch (e) {
                console.error('解析失败:', e.message);
                console.log('原始数据:', msg.result.result.value.substring(0, 500));
            }
        }
        
        ws.close();
    }
});

ws.on('error', (err) => {
    console.error('❌ WebSocket error:', err.message);
    process.exit(1);
});
