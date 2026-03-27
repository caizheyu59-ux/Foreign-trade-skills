param(
    [Parameter(Position=0)]
    [string]$Command = "help",

    [Parameter(ParameterSetName="Sequence")]
    [string]$Mode = "auto",

    [Parameter(ParameterSetName="Sequence")]
    [string]$u,

    [Parameter(ParameterSetName="Sequence")]
    [switch]$MailOnly,

    [string]$i,
    [string]$c,
    [string]$co,
    [string]$p,
    [string]$v,
    [string]$s,
    [string]$sc
)

$VERSION = "2.0.0"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$SETTINGS_PATH = Join-Path $SCRIPT_DIR "settings.json"
$QUEUE_PATH = Join-Path $SCRIPT_DIR "send_queue.json"

if (Test-Path $SETTINGS_PATH) {
    $script:SETTINGS = Get-Content $SETTINGS_PATH | ConvertFrom-Json
} else {
    $script:SETTINGS = $null
}

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
    Write-Host "Intelligence Hierarchy System - 3 Intelligence Levels"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  sequence     Generate 3-email sequence (with auto intelligence)"
    Write-Host "  first        Email 1: Connection"
    Write-Host "  second       Email 2: Value"
    Write-Host "  third        Email 3: Action"
    Write-Host "  subject      Generate subject lines"
    Write-Host "  followup     Follow-up email"
    Write-Host "  send         Send generated emails via SMTP"
    Write-Host "  queue        Show pending emails in send queue"
    Write-Host "  clear-queue  Clear send queue"
    Write-Host "  help         Show help"
    Write-Host ""
    Write-Host "Intelligence Modes:"
    Write-Host "  -mode precise   Full personalization (requires: company, pain point)"
    Write-Host "  -mode auto      Auto-research from URL (requires: -u <url>)"
    Write-Host "  -mode blind     Generic outreach (requires: -mail-only or email only)"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -i <type>       Industry: textile|electronics|packaging|machinery|consumer|general"
    Write-Host "  -c <name>       Target company name"
    Write-Host "  -co <country>   Target country"
    Write-Host "  -p <issue>      Customer pain point"
    Write-Host "  -v <value>      Your value proposition"
    Write-Host "  -s <name>       Sender name"
    Write-Host "  -sc <co>        Sender company"
    Write-Host "  -u <url>        Target company URL (for auto mode)"
    Write-Host "  -mail-only      Run in blind mode (email only)"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host '  .\b2b-cold.ps1 sequence -mode precise -c "Tech Corp" -p "long lead times"'
    Write-Host '  .\b2b-cold.ps1 sequence -mode auto -u "www.targetclient.com"'
    Write-Host '  .\b2b-cold.ps1 sequence -mail-only'
    Write-Host '  .\b2b-cold.ps1 send'
    Write-Host ""
}

function Get-TimezoneByCountry {
    param([string]$Country)

    $tzMap = @{
        "USA" = "America/New_York"; "US" = "America/New_York"
        "UK" = "Europe/London"; "GB" = "Europe/London"
        "Germany" = "Europe/Berlin"; "DE" = "Europe/Berlin"
        "France" = "Europe/Paris"; "FR" = "Europe/Paris"
        "Japan" = "Asia/Tokyo"; "JP" = "Asia/Tokyo"
        "China" = "Asia/Shanghai"; "CN" = "Asia/Shanghai"
        "Australia" = "Australia/Sydney"; "AU" = "Australia/Sydney"
        "Brazil" = "America/Sao_Paulo"; "BR" = "America/Sao_Paulo"
        "India" = "Asia/Kolkata"; "IN" = "Asia/Kolkata"
    }

    $normalized = $Country.Trim().ToUpper()
    return $tzMap[$normalized]
}

function Get-OptimalSendTime {
    param([string]$Country)

    $tz = Get-TimezoneByCountry $Country
    if (-not $tz) {
        return (Get-Date).AddHours(1)
    }

    try {
        $timezone = [TimeZoneInfo]::FindSystemTimeZoneById($tz)
        $utcNow = [DateTime]::UtcNow
        $localTime = [TimeZoneInfo]::ConvertTimeFromUtc($utcNow, $timezone)
        $targetHour = 9
        $targetMinute = 30

        if ($localTime.Hour -lt $targetHour) {
            return $localTime.Date.AddHours($targetHour).AddMinutes($targetMinute)
        } else {
            return $localTime.Date.AddDays(1).AddHours($targetHour).AddMinutes($targetMinute)
        }
    } catch {
        return (Get-Date).AddHours(1)
    }
}

function Invoke-AutoResearch {
    param([string]$Url)

    Write-Host "[Auto-Scanning] Researching $Url ..."

    $result = @{
        BusinessType = "retailer"
        Products = @()
        PainPoints = @()
        Industry = "general"
    }

    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec 15 -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        $content = $response.Content.ToLower()

        if ($content -match "manufacturer|oem|factory|production") {
            $result.BusinessType = "manufacturer"
        } elseif ($content -match "distributor|wholesaler|supply") {
            $result.BusinessType = "distributor"
        }

        $industryKeywords = @{
            "textile|fabric|garment|apparel|fashion" = "textile"
            "electronic|component|pcb|semiconductor" = "electronics"
            "packaging|carton|box|container" = "packaging"
            "machinery|equipment|industrial|parts" = "machinery"
            "consumer|retail|product|goods" = "consumer"
        }

        foreach ($keyword in $industryKeywords.Keys) {
            if ($content -match $keyword) {
                $result.Industry = $industryKeywords[$keyword]
                break
            }
        }

        if ($SETTINGS.industry_knowledge.$($result.Industry)) {
            $indKnowledge = $SETTINGS.industry_knowledge.$($result.Industry)
            $result.PainPoints = $indKnowledge.pain_points | Get-Random -Count ([Math]::Min(3, $indKnowledge.pain_points.Count))
        }
    } catch {
        Write-Host "[Warning] Could not fetch URL, using generic defaults"
        $result.Industry = $INDUSTRY
        $result.PainPoints = @("supplier reliability", "quality control")
    }

    return $result
}

function Get-BlindHook {
    param([string]$Country, [string]$Industry)

    $hooks = @(
        "I've been researching ${Country}'s ${Industry} market and noticed some interesting trends in supply chain optimization..."
        "Recent regulatory changes in ${Country} are affecting how ${Industry} companies approach their sourcing strategies..."
        "Many ${Industry} companies in ${Country} are facing challenges with cost control and supplier reliability..."
        "Based on our analysis, ${Industry} businesses in ${Country} are increasingly focusing on supply chain resilience..."
    )

    return $hooks | Get-Random
}

function Get-Compliment {
    param([string]$ind, [string]$company)

    if ($company) {
        return "I've been following $company and love how you've been pushing the boundaries in the $ind space."
    }

    switch ($ind) {
        "textile" { return "I've been following brands in the fashion space and love how the industry is evolving." }
        "electronics" { return "I've been impressed by innovation in the electronics space." }
        "packaging" { return "I've been keeping an eye on brands that elevate product presentation." }
        "machinery" { return "I've been following growth in the industrial sector." }
        "consumer" { return "I've been following brands with innovative products." }
        default { return "I've been following your company's growth and market presence." }
    }
}

function Get-Value {
    param([string]$ind)

    switch ($ind) {
        "textile" { return "premium fabrics, sustainable materials, custom prints" }
        "electronics" { return "reliable components, competitive pricing, strict quality control" }
        "packaging" { return "custom packaging, eco-friendly materials, unique designs" }
        "machinery" { return "precision-engineered parts, OEM/ODM services, technical support" }
        "consumer" { return "high-quality manufacturing, flexible MOQ, fast samples" }
        default { return "high-quality products, competitive pricing, reliable delivery" }
    }
}

function Get-PainPoint {
    param([string]$ind)

    switch ($ind) {
        "textile" { return "quality inconsistency, long production cycles" }
        "electronics" { return "component shortages, long lead times" }
        "packaging" { return "high costs, environmental concerns" }
        "machinery" { return "equipment downtime, parts availability" }
        "consumer" { return "supplier reliability, delivery delays" }
        default { return "supplier reliability, quality control" }
    }
}

function Get-Certificate {
    param([string]$ind)

    if ($SETTINGS.industry_knowledge.$ind) {
        $certs = $SETTINGS.industry_knowledge.$ind.certifications
        return $certs | Get-Random -Count ([Math]::Min(2, $certs.Count))
    }

    return @("ISO 9001", "CE")
}

function Generate-Subjects {
    param(
        [string]$Industry,
        [string]$Company,
        [string]$PainPoint
    )

    Write-Host ""
    Write-Host "========================================"
    Write-Host "HIGH-OPEN-RATE SUBJECT LINES"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "1. Quick question about your $Industry sourcing"
    if ($PainPoint) {
        Write-Host "2. Solving $PainPoint for $Industry companies"
    } else {
        Write-Host "2. A better way to source $Industry products"
    }
    if ($Company) {
        Write-Host "3. $Company + potential collaboration"
    } else {
        Write-Host "3. Idea for your $Industry business"
    }
    Write-Host "4. Are you open to a quick chat about $Industry?"
    Write-Host "5. Last try: $Industry opportunity"
    Write-Host ""
}

function Generate-Email1 {
    param(
        [string]$Mode = "auto",
        [string]$Company,
        [string]$Country,
        [string]$Industry,
        [string]$Hook,
        [string]$SenderName,
        [string]$SenderCompany
    )

    $senderName = if ($SenderName) { $SenderName } else { "[Your Name]" }
    $senderCo = if ($SenderCompany) { $SenderCompany } else { "[Your Company]" }

    Write-Host "========================================"
    Write-Host "EMAIL 1: BUILDING CONNECTION"
    Write-Host "Mode: $Mode - Low-pressure introduction"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Subject: Quick question about your $Industry sourcing"
    Write-Host ""
    Write-Host "Hi there,"
    Write-Host ""

    if ($Mode -eq "blind") {
        $blindHook = Get-BlindHook -Country $Country -Industry $Industry
        Write-Host $blindHook
        Write-Host ""
        Write-Host "I'm $senderName from $senderCo. We specialize in $(Get-Value $Industry) and have been helping companies like yours streamline their supply chain."
    } elseif ($Mode -eq "auto" -and $Hook) {
        Write-Host $Hook
        Write-Host ""
        Write-Host "I'm $senderName from $senderCo. We specialize in $(Get-Value $Industry)."
    } else {
        $compliment = Get-Compliment -ind $Industry -company $Company
        Write-Host $compliment
        Write-Host ""
        Write-Host "I'm $senderName from $senderCo. We specialize in $(Get-Value $Industry)."
    }

    Write-Host ""
    Write-Host "I'm not trying to sell you anything today—I just wanted to introduce myself and see if there's an opportunity for us to connect."

    if ($Country) {
        Write-Host "We've worked with several $Country companies already."
    } else {
        Write-Host "We've helped many companies in the $Industry space."
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

    return @{
        Subject = "Quick question about your $Industry sourcing"
        Body = $null
    }
}

function Generate-Email2 {
    param(
        [string]$Mode = "auto",
        [string]$Company,
        [string]$Industry,
        [string]$PainPoint,
        [string]$ValueProp,
        [string]$SenderName,
        [string]$SenderCompany
    )

    $pp = if ($PainPoint) { $PainPoint } else { Get-PainPoint $Industry }
    $vp = if ($ValueProp) { $ValueProp } else { Get-Value $Industry }
    $senderName = if ($SenderName) { $SenderName } else { "[Your Name]" }
    $senderCo = if ($SenderCompany) { $SenderCompany } else { "[Your Company]" }
    $co = if ($Company) { $Company } else { "your company" }

    $certs = Get-Certificate -ind $Industry

    Write-Host "========================================"
    Write-Host "EMAIL 2: DELIVERING VALUE"
    Write-Host "Mode: $Mode - Address pain points"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Subject: Re: Quick question about your $Industry sourcing"
    Write-Host ""
    Write-Host "Hi there,"
    Write-Host ""
    Write-Host "I wanted to follow up and share something that might interest you."
    Write-Host ""
    Write-Host "Many $Industry companies we work with were struggling with $pp before they found us."
    Write-Host ""

    if ($Mode -eq "precise") {
        Write-Host "We've helped companies similar to $co achieve significant improvements by addressing exactly these challenges."
    }

    Write-Host "Here's what we bring to the table:"
    Write-Host "• $vp"
    Write-Host "• Dedicated account management"
    Write-Host "• Flexible terms for growing businesses"
    if ($certs) {
        Write-Host "• $($certs -join ', ') certified"
    }
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
    param(
        [string]$Mode = "auto",
        [string]$Company,
        [string]$Industry,
        [string]$ValueProp,
        [string]$SenderName,
        [string]$SenderCompany
    )

    $senderName = if ($SenderName) { $SenderName } else { "[Your Name]" }
    $senderCo = if ($SenderCompany) { $SenderCompany } else { "[Your Company]" }
    $co = if ($Company) { $Company } else { "your company" }
    $vp = if ($ValueProp) { $ValueProp } else { "Better quality and faster delivery" }

    Write-Host "========================================"
    Write-Host "EMAIL 3: CALL TO ACTION"
    Write-Host "Mode: $Mode - Create urgency and get response"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Subject: Last try: $Industry opportunity for $co"
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

    if ($Mode -eq "blind") {
        Write-Host "If you're not actively looking for suppliers right now, I'd be happy to send you our free product catalog for future reference."
    } else {
        Write-Host 'If now isn''t the right time, I completely understand. Just reply with "not now" and I''ll circle back in a few months.'
    }

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
    param(
        [string]$Industry,
        [string]$ValueProp,
        [string]$SenderName,
        [string]$SenderCompany
    )

    $senderName = if ($SenderName) { $SenderName } else { "[Your Name]" }
    $senderCo = if ($SenderCompany) { $SenderCompany } else { "[Your Company]" }
    $vp = if ($ValueProp) { $ValueProp } else { "how we could help with your $Industry sourcing" }

    Write-Host "========================================"
    Write-Host "FOLLOW-UP EMAIL (No Reply)"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Subject: Bumping this up - $Industry sourcing"
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

function Add-ToSendQueue {
    param(
        [string]$To,
        [string]$Subject,
        [string]$Body,
        [string]$ScheduledTime
    )

    $queue = @()
    if (Test-Path $QUEUE_PATH) {
        $queue = Get-Content $QUEUE_PATH | ConvertFrom-Json
    }

    $entry = @{
        id = [guid]::NewGuid().ToString()
        to = $To
        subject = $Subject
        body = $Body
        scheduled_time = $ScheduledTime
        status = "pending"
        created_at = (Get-Date).ToString("o")
    }

    $queue += $entry
    $queue | ConvertTo-Json | Set-Content $QUEUE_PATH

    Write-Host "[Queue] Email to $To added. Scheduled: $ScheduledTime"
}

function Send-QueuedEmails {
    if (-not $SETTINGS -or -not $SETTINGS.smtp) {
        Write-Host "[Error] SMTP not configured. Please edit scripts/settings.json"
        return
    }

    $smtp = $SETTINGS.smtp
    $sendSettings = $SETTINGS.send_settings

    if (-not $smtp.username -or -not $smtp.password) {
        Write-Host "[Error] SMTP credentials not configured in settings.json"
        return
    }

    $queue = @()
    if (Test-Path $QUEUE_PATH) {
        $queue = Get-Content $QUEUE_PATH | ConvertFrom-Json
    }

    $pending = $queue | Where-Object { $_.status -eq "pending" }

    if ($pending.Count -eq 0) {
        Write-Host "[Info] No pending emails in queue"
        return
    }

    Write-Host "[Info] Sending $($pending.Count) emails..."

    try {
        $smtpParams = @{
            SmtpServer = $smtp.server
            Port = $smtp.port
            UseSsl = $smtp.use_ssl
            Credential = New-Object System.Management.Automation.PSCredential($smtp.username, (ConvertTo-SecureString $smtp.password -AsPlainText -Force))
            From = $smtp.from_email
        }

        foreach ($email in $pending) {
            $delay = Get-Random -Minimum $sendSettings.random_delay_min -Maximum $sendSettings.random_delay_max
            Write-Host "[Send] Waiting ${delay}s before sending to $($email.to)..."
            Start-Sleep -Seconds $delay

            try {
                Send-MailMessage @smtpParams -To $email.to -Subject $email.subject -Body $email.body -BodyAsHtml
                $email.status = "sent"
                Write-Host "[Sent] $($email.to)"
            } catch {
                $email.status = "failed"
                Write-Host "[Failed] $($email.to): $_"
            }
        }

        $queue | ConvertTo-Json | Set-Content $QUEUE_PATH
        Write-Host "[Complete] Send queue updated"
    } catch {
        Write-Host "[Error] SMTP connection failed: $_"
    }
}

function Show-Queue {
    if (Test-Path $QUEUE_PATH) {
        $queue = Get-Content $QUEUE_PATH | ConvertFrom-Json
        Write-Host ""
        Write-Host "Send Queue:"
        Write-Host "========================================"
        foreach ($email in $queue) {
            Write-Host "ID: $($email.id)"
            Write-Host "To: $($email.to)"
            Write-Host "Subject: $($email.subject)"
            Write-Host "Status: $($email.status)"
            Write-Host "Scheduled: $($email.scheduled_time)"
            Write-Host "---"
        }
    } else {
        Write-Host "[Info] Queue is empty"
    }
}

function Clear-Queue {
    if (Test-Path $QUEUE_PATH) {
        Remove-Item $QUEUE_PATH
        Write-Host "[Info] Queue cleared"
    }
}

function Resolve-IntelligenceMode {
    if ($MailOnly) {
        return "blind"
    }

    if ($u) {
        return "auto"
    }

    if ($Company -and $PainPoint) {
        return "precise"
    }

    return "auto"
}

function Get-AutoResearchHook {
    param([hashtable]$Research)

    $businessType = $Research.BusinessType
    $products = $Research.Products -join ", "

    if ($businessType -eq "manufacturer") {
        return "I've been researching companies that manufacture $products and noticed how supply chain optimization has become crucial for producers like yourselves..."
    } elseif ($businessType -eq "distributor") {
        return "I've been studying the distribution landscape for $products and found that reliable supply partners make a significant difference..."
    } else {
        return "I've been following companies like yours that are focused on delivering quality products to their customers..."
    }
}

$resolvedMode = Resolve-IntelligenceMode

if ($resolvedMode -eq "auto" -and $u) {
    $research = Invoke-AutoResearch -Url $u
    $script:INDUSTRY = $research.Industry
    if ($research.PainPoints.Count -gt 0) {
        $script:PAINPOINT = $research.PainPoints[0]
    }
    $global:autoHook = Get-AutoResearchHook -Research $research
}

switch ($Command) {
    "sequence" {
        Generate-Subjects -Industry $INDUSTRY -Company $COMPANY -PainPoint $PAINPOINT
        Generate-Email1 -Mode $resolvedMode -Company $COMPANY -Country $COUNTRY -Industry $INDUSTRY -Hook $global:autoHook -SenderName $SENDER -SenderCompany $SENDER_COMPANY
        Generate-Email2 -Mode $resolvedMode -Company $COMPANY -Industry $INDUSTRY -PainPoint $PAINPOINT -ValueProp $VALUEPROP -SenderName $SENDER -SenderCompany $SENDER_COMPANY
        Generate-Email3 -Mode $resolvedMode -Company $COMPANY -Industry $INDUSTRY -ValueProp $VALUEPROP -SenderName $SENDER -SenderCompany $SENDER_COMPANY
    }
    "first" { Generate-Email1 -Mode $resolvedMode -Company $COMPANY -Country $COUNTRY -Industry $INDUSTRY -Hook $global:autoHook -SenderName $SENDER -SenderCompany $SENDER_COMPANY }
    "second" { Generate-Email2 -Mode $resolvedMode -Company $COMPANY -Industry $INDUSTRY -PainPoint $PAINPOINT -ValueProp $VALUEPROP -SenderName $SENDER -SenderCompany $SENDER_COMPANY }
    "third" { Generate-Email3 -Mode $resolvedMode -Company $COMPANY -Industry $INDUSTRY -ValueProp $VALUEPROP -SenderName $SENDER -SenderCompany $SENDER_COMPANY }
    "subject" { Generate-Subjects -Industry $INDUSTRY -Company $COMPANY -PainPoint $PAINPOINT }
    "followup" { Generate-Followup -Industry $INDUSTRY -ValueProp $VALUEPROP -SenderName $SENDER -SenderCompany $SENDER_COMPANY }
    "send" { Send-QueuedEmails }
    "queue" { Show-Queue }
    "clear-queue" { Clear-Queue }
    default { Show-Help }
}