#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Complete workflow for foreign-trade-email-writer
.DESCRIPTION
    完整的开发信工作流程：获取客户信息 → 生成开发信 → 发送邮件
#>

$VERSION = "2.1.0"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

function Show-Header {
    Clear-Host
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Foreign Trade Email Writer v$VERSION" -ForegroundColor Cyan
    Write-Host "  外贸开发信生成器 - 完整工作流程" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Check-Prerequisites {
    Write-Host "[检查] 正在检查前置配置..." -ForegroundColor Yellow
    
    # Check Python
    try {
        python --version 2>&1 | Out-Null
        Write-Host "  [OK] Python: 已安装" -ForegroundColor Green
    } catch {
        Write-Host "  [X] Python: 未安装" -ForegroundColor Red
    }
    
    # Check Tavily
    if ($env:TAVILY_API_KEY) {
        Write-Host "  [OK] Tavily API: 已配置" -ForegroundColor Green
    } else {
        Write-Host "  [X] Tavily API: 未配置" -ForegroundColor Red
    }
    
    Write-Host ""
}

function Select-Mode {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  选择工作模式" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [1] Precise 模式 - 精准个性化" -ForegroundColor White
    Write-Host "  [2] Auto 模式 - 自动调研" -ForegroundColor White  
    Write-Host "  [3] Blind 模式 - 通用模板" -ForegroundColor White
    Write-Host ""
    
    do {
        $mode = Read-Host "请选择模式 (1/2/3)"
    } while ($mode -notin @('1', '2', '3'))
    
    return $mode
}

function Get-CustomerInfo {
    param($Mode)
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  输入客户信息" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $info = @{}
    
    switch ($Mode) {
        '1' { # Precise
            $info['company'] = Read-Host "客户公司名"
            $info['industry'] = Read-Host "行业 (textile/electronics/packaging/machinery/consumer/general)"
            $info['country'] = Read-Host "客户国家"
            $info['painpoint'] = Read-Host "客户痛点"
        }
        '2' { # Auto
            $info['url'] = Read-Host "客户网站 URL"
            $info['country'] = Read-Host "客户国家"
            Write-Host "[调研] 正在分析网站..." -ForegroundColor Yellow
            $info['industry'] = 'general'
            $info['painpoint'] = 'supplier reliability'
        }
        '3' { # Blind
            $info['industry'] = Read-Host "行业 (textile/electronics/packaging/machinery/consumer/general)"
            $info['country'] = Read-Host "客户国家"
            $info['painpoint'] = 'supplier reliability'
        }
    }
    
    $info['valueprop'] = Read-Host "你的价值主张"
    $info['sender'] = Read-Host "你的名字"
    $info['sender_company'] = Read-Host "你的公司名"
    
    return $info
}

function Generate-Email {
    param($Info, $Mode)
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  生成开发信" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $b2bScript = Join-Path $SCRIPT_DIR "b2b-cold.ps1"
    
    $args = @("sequence")
    
    if ($Mode -eq '1') {
        $args += @("-mode", "precise", "-c", $Info['company'], "-p", $Info['painpoint'])
    } elseif ($Mode -eq '2') {
        $args += @("-mode", "auto", "-u", $Info['url'])
    } else {
        $args += @("-MailOnly")
    }
    
    $args += @("-i", $Info['industry'], "-co", $Info['country'], "-v", $Info['valueprop'], "-s", $Info['sender'], "-sc", $Info['sender_company'])
    
    & $b2bScript @args
}

function Send-EmailPrompt {
    param($Info)
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  发送邮件" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $send = Read-Host "是否发送邮件? (y/n)"
    
    if ($send -eq 'y') {
        $email = Read-Host "客户邮箱地址"
        $subject = Read-Host "邮件主题"
        $body = Read-Host "邮件内容 (或文件路径)"
        
        $sendScript = Join-Path $SCRIPT_DIR "send-email.ps1"
        & $sendScript -To $email -Subject $subject -Body $body
    }
}

# Main
Show-Header
Check-Prerequisites
$mode = Select-Mode
$info = Get-CustomerInfo -Mode $mode
Generate-Email -Info $info -Mode $mode
Send-EmailPrompt -Info $info

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  工作流程完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
