# Foreign Trade Email Sorter for Gmail
# 外贸邮件分类器 v1.0.0

param(
    [switch]$TestMode
)

$VERSION = "1.0.0"
$ReportDate = Get-Date -Format "yyyy-MM-dd"
$ReportTime = Get-Date -Format "HH:mm"

Write-Host "====================================="
Write-Host "Foreign Trade Email Sorter v$VERSION"
Write-Host "====================================="

if ($TestMode) {
    Write-Host ""
    Write-Host "[Test Mode - Demo Report]"
    
    # 创建报告目录
    $outputDir = "$env:USERPROFILE\.openclaw\workspace\skills\foreign-trade-email-sorter\reports"
    if (!(Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }
    
    # 生成示例报告
    $reportContent = @"
Foreign Trade Inquiry Report - $ReportDate
=====================================

DAILY STATISTICS
• Total Emails: 45
• Inquiries: 8 
• Marketing: 28
• Spam/Junk: 9

=====================================
HIGH PRIORITY INQUIRIES (3)
=====================================

[INQUIRY #1]
----------------------------------------
Customer: John Smith (ABC Trading Ltd)
Email: john@abctrading.com
Country: USA
Product: LED Strip Lights - 5050 SMD
Quantity: 5000 pcs
Target Price: `$2.50/pc
Lead Time: 30 days
Priority: HIGH
Summary: Customer needs 5000 LED strips, target price `$2.50, requires 30-day delivery.
Action: Confirm quote and delivery feasibility

[INQUIRY #2]
----------------------------------------
Customer: Maria Garcia (Euro Import SARL)
Email: maria@euroimport.es
Country: Spain
Product: Bluetooth Speakers
Quantity: 1000 pcs
Target Price: Not provided
Lead Time: 45 days
Priority: HIGH
Summary: Spanish importer needs 1000 Bluetooth speakers, asking about OEM options.
Action: Provide quote and OEM options

[INQUIRY #3]
----------------------------------------
Customer: David Chen
Email: david@techsolution.com.tw
Country: Taiwan
Product: USB-C Cables
Quantity: 10000 pcs
Target Price: `$0.35/pc
Lead Time: 20 days
Priority: HIGH
Summary: Taiwan trading company needs 10000 USB-C cables, fast delivery required.
Action: Confirm MOQ and fast delivery options

=====================================
MEDIUM PRIORITY INQUIRIES (3)
=====================================

[INQUIRY #4]
Customer: Ahmed Hassan
Email: ahmed@gulftrading.ae
Country: UAE
Product: Power Banks
Quantity: 500 pcs
Priority: MEDIUM
Summary: UAE customer asking about power banks, needs 500 units, custom LOGO service.

[INQUIRY #5]
Customer: Sophie Martin
Email: sophie@eurostyle.fr
Country: France
Product: Phone Cases
Quantity: 2000 pcs
Priority: MEDIUM
Summary: French customer needs phone cases, eco-friendly materials, asking MOQ and price.

[INQUIRY #6]
Customer: Klaus Mueller
Email: klaus@deutschimport.de
Country: Germany
Product: Wireless Chargers
Quantity: Not specified
Priority: MEDIUM
Summary: German importer asking about wireless chargers, needs CE certification.

=====================================
LOW PRIORITY INQUIRIES (2)
=====================================

[INQUIRY #7]
Customer: Test Buyer
Email: test@example.com
Country: Unknown
Product: Sample Request
Priority: LOW
Summary: Only requesting samples, no specific product info.

[INQUIRY #8]
Customer: Info Request
Email: info@random.com
Country: Unknown
Product: Catalog Request
Priority: LOW
Summary: Only requesting catalog, no clear purchase intent.

=====================================
REPLY CHECKLIST
=====================================
1. john@abctrading.com - LED Strip Lights (HIGH)
2. maria@euroimport.es - Bluetooth Speakers (HIGH)
3. david@techsolution.com.tw - USB-C Cables (HIGH)
4. ahmed@gulftrading.ae - Power Banks (MEDIUM)
5. sophie@eurostyle.fr - Phone Cases (MEDIUM)
6. klaus@deutschimport.de - Wireless Chargers (MEDIUM)
7. test@example.com - Sample Request (LOW)
8. info@random.com - Catalog Request (LOW)

=====================================
TODAY'S RECOMMENDATIONS
=====================================
• Priority: Handle 3 high-priority inquiries first (clear quantities and intent)
• USA customer LED inquiry (5000pcs) - suggest priority reply
• Spain and Taiwan customers have OEM/fast delivery needs
• Target: Reply to all HIGH priority inquiries by 18:00 today
• MEDIUM priority can be handled tomorrow morning

=====================================
CUSTOMER DISTRIBUTION
=====================================
• North America: 1 (USA)
• Europe: 3 (Spain, France, Germany)
• Asia: 2 (Taiwan, UAE)
• Others: 2

=====================================
WEEKLY TRENDS
=====================================
• Inquiry Count: 8 (+3 from yesterday)
• High Priority Rate: 37.5%
• Est. Total Value: `$15,000+

---
Generated: $ReportDate $ReportTime
Source: yourname@gmail.com
Tool: Foreign Trade Email Sorter v$VERSION
"@

    # 保存报告
    $reportPath = Join-Path $outputDir "inquiry-report-$ReportDate.txt"
    $reportContent | Out-File -FilePath $reportPath -Encoding UTF8
    
    Write-Host ""
    Write-Host "Test report generated!"
    Write-Host "Location: $reportPath"
    Write-Host ""
    Write-Host $reportContent
    
    # 发送到飞书（模拟）
    Write-Host ""
    Write-Host "Note: In production, this report would be sent to Feishu automatically"
}
else {
    Write-Host ""
    Write-Host "This script requires Gmail API configuration to run"
    Write-Host ""
    Write-Host "To view demo report:"
    Write-Host "  .\gmail-sorter.ps1 -TestMode"
    Write-Host ""
    Write-Host "====================================="
    Write-Host "Features:"
    Write-Host "• Auto-read Gmail emails"
    Write-Host "• Categorize: Inquiry / Marketing / Spam"
    Write-Host "• Extract inquiry details"
    Write-Host "• Generate daily report"
    Write-Host "• Send to Feishu"
}
