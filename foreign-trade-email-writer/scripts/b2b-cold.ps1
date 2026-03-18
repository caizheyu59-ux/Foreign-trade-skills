# B2B Cold Email Writer v1.0.0
# Usage: .\b2b-cold.ps1 <command> [options]

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [string]$i,
    [string]$c,
    [string]$co,
    [string]$p,
    [string]$v,
    [string]$s,
    [string]$sc
)

$VERSION = "1.0.0"
$INDUSTRY = if ($i) { $i } else { "general" }
$COMPANY = $c
$COUNTRY = $co
$PAINPOINT = $p
$VALUEPROP = $v
$SENDER = $s
$SENDER_COMPANY = $sc

function Show-Help {
    Write-Host ""
    Write-Host "B2B Cold Email Writer v$VERSION"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  sequence    Generate 3-email sequence"
    Write-Host "  first       Email 1: Connection"
    Write-Host "  second      Email 2: Value"
    Write-Host "  third       Email 3: Action"
    Write-Host "  subject     Generate subject lines"
    Write-Host "  followup    Follow-up email"
    Write-Host "  help        Show help"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -i <type>    Industry: textile|electronics|packaging|machinery|consumer|general"
    Write-Host "  -c <name>    Target company name"
    Write-Host "  -co <country> Target country"
    Write-Host "  -p <issue>   Customer pain point"
    Write-Host "  -v <value>   Your value proposition"
    Write-Host "  -s <name>    Sender name"
    Write-Host "  -sc <co>     Sender company"
    Write-Host ""
    Write-Host "Example:"
    Write-Host '  .\b2b-cold.ps1 sequence -i textile -c "Fashion Brand" -p "long lead time" -v "7-day delivery"'
    Write-Host ""
}

function Get-Compliment($ind) {
    switch ($ind) {
        "textile" { return "I've been following your brand and love how you've been pushing the boundaries of fashion." }
        "electronics" { return "I've been impressed by your company's innovation in the electronics space." }
        "packaging" { return "I've been keeping an eye on your brand. The way you elevate product presentation is impressive." }
        "machinery" { return "I've been following your company's growth in the industrial sector." }
        "consumer" { return "I've been following your brand's journey and your innovative products." }
        default { return "I've been following your company's growth and market presence." }
    }
}

function Get-Value($ind) {
    switch ($ind) {
        "textile" { return "premium fabrics, sustainable materials, custom prints" }
        "electronics" { return "reliable components, competitive pricing, strict quality control" }
        "packaging" { return "custom packaging, eco-friendly materials, unique designs" }
        "machinery" { return "precision-engineered parts, OEM/ODM services, technical support" }
        "consumer" { return "high-quality manufacturing, flexible MOQ, fast samples" }
        default { return "high-quality products, competitive pricing, reliable delivery" }
    }
}

function Get-PainPoint($ind) {
    switch ($ind) {
        "textile" { return "quality inconsistency, long production cycles" }
        "electronics" { return "component shortages, long lead times" }
        "packaging" { return "high costs, environmental concerns" }
        "machinery" { return "equipment downtime, parts availability" }
        "consumer" { return "supplier reliability, delivery delays" }
        default { return "supplier reliability, quality control" }
    }
}

function Generate-Subjects {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "HIGH-OPEN-RATE SUBJECT LINES"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "1. Quick question about your $INDUSTRY sourcing"
    if ($PAINPOINT) {
        Write-Host "2. Solving $PAINPOINT for $INDUSTRY companies"
    } else {
        Write-Host "2. A better way to source $INDUSTRY products"
    }
    if ($COMPANY) {
        Write-Host "3. $COMPANY + potential collaboration"
    } else {
        Write-Host "3. Idea for your $INDUSTRY business"
    }
    Write-Host "4. Are you open to a quick chat about $INDUSTRY?"
    Write-Host "5. Last try: $INDUSTRY opportunity"
    Write-Host ""
}

function Generate-Email1 {
    $compliment = Get-Compliment $INDUSTRY
    $value = Get-Value $INDUSTRY
    $senderName = if ($SENDER) { $SENDER } else { "[Your Name]" }
    $senderCo = if ($SENDER_COMPANY) { $SENDER_COMPANY } else { "[Your Company]" }
    
    Write-Host "========================================"
    Write-Host "EMAIL 1: BUILDING CONNECTION"
    Write-Host "Goal: Low-pressure introduction"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Subject: Quick question about your $INDUSTRY sourcing"
    Write-Host ""
    Write-Host "Hi there,"
    Write-Host ""
    Write-Host $compliment
    Write-Host ""
    Write-Host "I'm $senderName from $senderCo. We specialize in $value."
    Write-Host ""
    Write-Host "I'm not trying to sell you anything today—I just wanted to introduce myself and see if there's an opportunity for us to connect."
    if ($COUNTRY) {
        Write-Host "We've worked with several $COUNTRY companies already."
    } else {
        Write-Host "We've helped many companies in the $INDUSTRY space."
    }
    Write-Host ""
    Write-Host "If you have a few minutes next week, I'd be happy to chat about what trends or challenges you're seeing."
    Write-Host ""
    Write-Host "Any thoughts?"
    Write-Host ""
    Write-Host "Best regards,"
    Write-Host $senderName
    Write-Host $senderCo
    Write-Host ""
}

function Generate-Email2 {
    $pp = if ($PAINPOINT) { $PAINPOINT } else { Get-PainPoint $INDUSTRY }
    $vp = if ($VALUEPROP) { $VALUEPROP } else { Get-Value $INDUSTRY }
    $senderName = if ($SENDER) { $SENDER } else { "[Your Name]" }
    $senderCo = if ($SENDER_COMPANY) { $SENDER_COMPANY } else { "[Your Company]" }
    $co = if ($COMPANY) { $COMPANY } else { "your company" }
    
    Write-Host "========================================"
    Write-Host "EMAIL 2: DELIVERING VALUE"
    Write-Host "Goal: Show how you solve their pain point"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Subject: Re: Quick question about your $INDUSTRY sourcing"
    Write-Host ""
    Write-Host "Hi there,"
    Write-Host ""
    Write-Host "I wanted to follow up and share something that might interest you."
    Write-Host ""
    Write-Host "Many $INDUSTRY companies we work with were struggling with $pp before they found us."
    Write-Host ""
    Write-Host "Here's what we bring to the table:"
    Write-Host "• $vp"
    Write-Host "• Dedicated account management"
    Write-Host "• Flexible terms for growing businesses"
    Write-Host ""
    Write-Host "One of our clients saw a 30% improvement in their supply chain efficiency within 3 months of working with us."
    Write-Host ""
    Write-Host "Would you be open to a brief call to explore if we could help $co achieve similar results?"
    Write-Host ""
    Write-Host "Best regards,"
    Write-Host $senderName
    Write-Host $senderCo
    Write-Host ""
}

function Generate-Email3 {
    $senderName = if ($SENDER) { $SENDER } else { "[Your Name]" }
    $senderCo = if ($SENDER_COMPANY) { $SENDER_COMPANY } else { "[Your Company]" }
    $co = if ($COMPANY) { $COMPANY } else { "your company" }
    $vp = if ($VALUEPROP) { $VALUEPROP } else { "Better quality and faster delivery" }
    
    Write-Host "========================================"
    Write-Host "EMAIL 3: CALL TO ACTION"
    Write-Host "Goal: Create urgency and get response"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Subject: Last try: $INDUSTRY opportunity for $co"
    Write-Host ""
    Write-Host "Hi there,"
    Write-Host ""
    Write-Host "I don't want to clutter your inbox, so this will be my last email unless I hear back from you."
    Write-Host ""
    Write-Host "I truly believe we could help $co with:"
    Write-Host "• $vp"
    Write-Host "• Reducing supply chain headaches"
    Write-Host "• Competitive pricing without compromising quality"
    Write-Host ""
    Write-Host 'If now isn''t the right time, I completely understand. Just reply with "not now" and I''ll circle back in a few months.'
    Write-Host ""
    Write-Host "Otherwise, here's my calendar link: [Your Calendar Link]"
    Write-Host "Or simply reply with a time that works for you."
    Write-Host ""
    Write-Host "Best regards,"
    Write-Host $senderName
    Write-Host $senderCo
    Write-Host "[Your Phone/WhatsApp]"
    Write-Host ""
}

function Generate-Followup {
    $senderName = if ($SENDER) { $SENDER } else { "[Your Name]" }
    $senderCo = if ($SENDER_COMPANY) { $SENDER_COMPANY } else { "[Your Company]" }
    $vp = if ($VALUEPROP) { $VALUEPROP } else { "how we could help with your $INDUSTRY sourcing" }
    
    Write-Host "========================================"
    Write-Host "FOLLOW-UP EMAIL (No Reply)"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Subject: Bumping this up - $INDUSTRY sourcing"
    Write-Host ""
    Write-Host "Hi there,"
    Write-Host ""
    Write-Host "I know you're busy, so I'll keep this short."
    Write-Host ""
    Write-Host "I reached out about $vp and wanted to make sure my email didn't get lost in your inbox."
    Write-Host ""
    Write-Host "If this isn't a priority right now, no worries at all. Just let me know and I'll follow up at a better time."
    Write-Host ""
    Write-Host "If it is, I'd love to jump on a quick 10-minute call to see if we're a good fit."
    Write-Host ""
    Write-Host "What works best for you?"
    Write-Host ""
    Write-Host "Best regards,"
    Write-Host $senderName
    Write-Host $senderCo
    Write-Host ""
}

# Main
switch ($Command) {
    "sequence" {
        Generate-Subjects
        Generate-Email1
        Generate-Email2
        Generate-Email3
    }
    "first" { Generate-Email1 }
    "second" { Generate-Email2 }
    "third" { Generate-Email3 }
    "subject" { Generate-Subjects }
    "followup" { Generate-Followup }
    default { Show-Help }
}
