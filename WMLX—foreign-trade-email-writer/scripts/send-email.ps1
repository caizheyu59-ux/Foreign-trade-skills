#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Send email via Gmail API using foreign-trade-email-sorter credentials
.DESCRIPTION
    This script sends emails using Gmail API, reusing credentials from foreign-trade-email-sorter
.EXAMPLE
    .\send-email.ps1 -To "client@example.com" -Subject "Hello" -Body "Email content"
    .\send-email.ps1 -To "client@example.com" -Subject "Hello" -BodyFile "email.txt"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$To,
    
    [Parameter(Mandatory=$true)]
    [string]$Subject,
    
    [Parameter(Mandatory=$true, ParameterSetName="BodyText")]
    [string]$Body,
    
    [Parameter(Mandatory=$true, ParameterSetName="BodyFile")]
    [string]$BodyFile
)

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$SENDER_SCRIPT = Join-Path $SCRIPT_DIR "gmail_sender.py"

# 检查 Python 脚本是否存在
if (-not (Test-Path $SENDER_SCRIPT)) {
    Write-Error "gmail_sender.py not found at: $SENDER_SCRIPT"
    exit 1
}

# 构建参数
$pythonArgs = @($SENDER_SCRIPT, "--to", $To, "--subject", $Subject)

if ($BodyFile) {
    $pythonArgs += @("--body", $BodyFile, "--body-file")
} else {
    # 将 body 保存到临时文件
    $tempFile = [System.IO.Path]::GetTempFileName()
    $Body | Out-File -FilePath $tempFile -Encoding UTF8
    $pythonArgs += @("--body", $tempFile, "--body-file")
}

# 运行 Python 脚本
Write-Host "Sending email to: $To"
Write-Host "Subject: $Subject"
Write-Host ""

& python $pythonArgs

$exitCode = $LASTEXITCODE

# 清理临时文件
if ($Body -and (Test-Path $tempFile)) {
    Remove-Item $tempFile -ErrorAction SilentlyContinue
}

if ($exitCode -eq 0) {
    Write-Host "`n✅ Email sent successfully!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Failed to send email" -ForegroundColor Red
}

exit $exitCode
