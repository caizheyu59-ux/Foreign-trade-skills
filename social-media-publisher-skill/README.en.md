# Social Media Publisher Skill

**Version**: 1.1.0  
**Release Date**: 2026-04-08  
**Author**: Shutiao + Longxia  
**License**: MIT

---

## 📋 Overview

An automated multi-platform video publishing skill for OpenClaw. Upload videos to major social media platforms using Chrome DevTools Protocol (CDP).

**Supported Platforms**:
- ✅ Xiaohongshu (Little Red Book)
- ✅ Bilibili (B Station)
- ✅ YouTube
- ✅ Douyin (TikTok China)

**Core Features**:
- 🎯 Auto upload video files
- ✍️ Auto fill titles and descriptions
- 🏷️ Auto add tags/hashtags
- 💾 Support save draft or publish

---

## 🚀 Quick Start

### Prerequisites

**Required**:
1. ✅ OpenClaw v1.0.0+
2. ✅ web-access skill v2.4.0+
3. ✅ Chrome Browser v90+ (with remote debugging)
4. ✅ Node.js v18+

**Detailed setup**: See [`docs/DEPENDENCIES.md`](docs/DEPENDENCIES.md)

### Installation

1. **Install dependencies**
   ```bash
   # Install OpenClaw
   npm install -g openclaw
   
   # Install web-access skill
   openclaw skill install web-access
   ```

2. **Copy skill files**
   ```bash
   cp -r social-media-publisher-skill ~/.openclaw/skills/
   ```

3. **Configure Chrome remote debugging**
   - Open Chrome browser
   - Visit: `chrome://inspect/#remote-debugging`
   - Check: ✅ "Allow remote debugging for this browser instance"
   - Restart Chrome (if needed)

4. **Start CDP Proxy**
   ```bash
   node ~/.openclaw/skills/web-access/scripts/cdp-proxy.mjs
   ```

5. **Test connection**
   ```bash
   cd scripts
   node test-connection.js
   ```

---

## 📖 Usage

### Basic Commands

```bash
# Upload to Xiaohongshu
node upload-xhs.js "C:\video.mp4" "C:\content.txt"

# Test connection
node test-connection.js
```

### Content File Format

Create a text file (e.g., `content.txt`):

```
1. Short Title
AI Era: How to Make Overseas Customers Trust You at First Sight?

4. First-Person Summary
Trust is precious in the AI era:
In today's B2B industry, trust is everything...

How to use this feature:
Customers can switch between different lenses in real-time...

Tags: #ForeignTrade #CrossBorderEcommerce #B2B
```

---

## 🔧 Technical Details

### CDP Proxy API

All operations use web-access CDP Proxy (port 3456):

```bash
# List tabs
curl -s http://localhost:3456/targets

# Open page
curl -s "http://localhost:3456/new?url=https://example.com"

# Execute JS
curl -s -X POST "http://localhost:3456/eval?target=TARGET_ID" -d "document.title"

# Upload file
curl -s -X POST "http://localhost:3456/setFiles?target=TARGET_ID" -d '{"selector":"input[type=file]","files":["video.mp4"]}'

# Screenshot
curl -s "http://localhost:3456/screenshot?target=TARGET_ID&file=check.png"
```

### Platform Selectors

Each platform has precise CSS selectors:
- See `docs/platform-selectors.md` for complete list
- See `docs/buttons.md` for button selectors

---

## ⚠️ Important Notes

### 1. Chrome Remote Debugging
- Must enable remote debugging port (default 9222)
- Must check "Allow remote debugging"
- May need to restart Chrome

### 2. Login Status
- All platforms require prior login in Chrome
- CDP reuses Chrome login session
- Manually re-login if session expires

### 3. File Upload
- Use `DOM.setFileInputFiles` + `objectId`
- ❌ Don't use `nodeId` (will fail)
- Must trigger `change` event after upload

### 4. Text Input
- Title: Direct set `value` (except YouTube)
- Description: Use `execCommand` or `innerText`
- Tags: Press `Enter` after input

---

## 🐛 Troubleshooting

### Common Issues

**Issue 1**: CDP connection failed
```
Error: ECONNREFUSED
Solution: Check Chrome remote debugging, port 9222
```

**Issue 2**: File upload failed
```
Error: Cannot set files
Solution: Use objectId, not nodeId
```

**Issue 3**: YouTube description invalid
```
Error: Description empty
Solution: Must use document.execCommand('insertText')
```

**Issue 4**: Douyin tags not showing
```
Error: Tags not added
Solution: Input #hashtag directly in description box
```

See `docs/troubleshooting.md` for detailed guide.

---

## 📁 File Structure

```
social-media-publisher-skill/
├── SKILL.md              # Skill definition
├── README.md             # This file (English)
├── README.zh.md          # Chinese version
├── LICENSE               # MIT License
├── docs/                 # Documentation
│   ├── platform-selectors.md
│   ├── buttons.md
│   ├── quick-start.md
│   ├── troubleshooting.md
│   └── DEPENDENCIES.md
├── scripts/              # Executable scripts
│   ├── cdp-lib.js
│   ├── upload-xhs.js
│   └── test-connection.js
└── examples/             # Examples
    └── content-template.txt
```

---

## 📝 Changelog

### v1.1.0 (2026-04-08)
- ✅ Optimized selector stability
- ✅ Added configuration options (30+ settings)
- ✅ Enhanced logging with progress bars
- ✅ Added error recovery mechanism
- ✅ Added auto-retry logic

### v1.0.0 (2026-04-08)
- ✅ Initial release
- ✅ Support 4 major platforms
- ✅ Complete documentation
- ✅ All platforms tested and verified

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

**GitHub Repository**: (To be created)

---

## 📄 License

MIT License - See LICENSE file

---

**Happy Publishing!** 🍟
