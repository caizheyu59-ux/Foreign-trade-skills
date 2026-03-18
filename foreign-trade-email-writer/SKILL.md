---
version: "1.0.0"
name: foreign-trade-email-writer
description: "B2B cold email sequence generator for foreign trade professionals. Generates personalized 3-email sequences with industry-specific templates for international business outreach."
author: Morment
homepage: https://github.com/yourusername/foreign-trade-email-writer
source: https://github.com/yourusername/foreign-trade-email-writer
---

# Foreign Trade Email Writer

Generate personalized B2B cold email sequences for international trade and sales outreach.

## What It Does

This tool generates **3-email progressive sequences** that follow the B2B sales funnel:

1. **Email 1**: Build connection (low pressure, no selling)
2. **Email 2**: Deliver value (address pain points)
3. **Email 3**: Call to action (urgency + clear CTA)

## Why Use This?

- **Industry-Specific**: 6 built-in industries with tailored messaging
- **Pain Point Driven**: Content automatically adapts to customer challenges
- **Professional English**: Suitable for global B2B outreach
- **Proven Structure**: Based on 10+ years of B2B sales best practices

## Quick Start

### Windows (PowerShell)

```powershell
# Generate complete sequence
.\scripts\b2b-cold.ps1 sequence -i electronics -c "Tech Corp" -p "long lead times" -v "48hr delivery"

# Generate subject lines only
.\scripts\b2b-cold.ps1 subject -i textile
```

### Mac/Linux (Bash)

```bash
# Generate complete sequence
bash scripts/b2b-cold.sh sequence -i electronics -c "Tech Corp" -p "long lead times" -v "48hr delivery"

# Generate first email only
bash scripts/b2b-cold.sh first -i packaging -c "Package Brand"
```

## Commands

| Command | Purpose |
|---------|---------|
| `sequence` | Full 3-email sequence |
| `first` | Email 1: Connection |
| `second` | Email 2: Value |
| `third` | Email 3: Action |
| `subject` | Subject lines only |
| `followup` | No-reply follow-up |
| `help` | Show help |

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `-i` | Industry | `textile`, `electronics`, `packaging`, `machinery`, `consumer`, `general` |
| `-c` | Target company | `"Fashion Brand Inc"` |
| `-co` | Country | `"USA"`, `"Germany"` |
| `-p` | Pain point | `"long lead time"` |
| `-v` | Value proposition | `"7-day fast delivery"` |
| `-s` | Sender name | `"Mike Zhang"` |
| `-sc` | Sender company | `"ABC Textile Co."` |

## Supported Industries

- **textile**: Fabrics, fashion, sustainable materials
- **electronics**: Components, quality control, stock management
- **packaging**: Custom packaging, eco-friendly materials
- **machinery**: Industrial parts, OEM/ODM services
- **consumer**: Retail products, flexible MOQ
- **general**: Universal template for any industry

## The 3-Email Strategy

### Email 1: Building Connection
- Opens with industry-specific compliment
- Introduces sender without hard selling
- Asks for dialogue, not a meeting
- Tone: Friendly, curious, respectful

### Email 2: Delivering Value
- Addresses specific pain point
- Lists concrete value propositions
- Includes social proof
- Soft CTA for a brief call

### Email 3: Call to Action
- "Last email" creates urgency
- Recaps key benefits
- Easy opt-out option
- Clear calendar/schedule CTA

## Full Example

Input:
```powershell
.\scripts\b2b-cold.ps1 sequence `
  -i textile `
  -c "Fashion Brand Inc" `
  -co "USA" `
  -p "long lead time" `
  -v "7-day fast delivery with custom prints" `
  -s "Mike Zhang" `
  -sc "ABC Textile Co."
```

Output:
```
=== HIGH-OPEN-RATE SUBJECT LINES ===
1. Quick question about your textile sourcing
2. Solving long lead time for textile companies
3. Fashion Brand Inc + potential collaboration
4. Are you open to a quick chat about textile?
5. Last try: textile opportunity

=== EMAIL 1: BUILDING CONNECTION ===
Subject: Quick question about your textile sourcing

Hi there,

I've been following your brand and love how you've been pushing the 
boundaries of fashion.

I'm Mike Zhang from ABC Textile Co. We specialize in premium fabrics, 
sustainable materials, custom prints.

I'm not trying to sell you anything today—I just wanted to introduce 
myself and see if there's an opportunity for us to connect.

We've worked with several USA companies already.

If you have a few minutes next week, I'd be happy to chat about what 
trends or challenges you're seeing.

Any thoughts?

Best regards,
Mike Zhang
ABC Textile Co.

[Email 2 and 3 follow...]
```

## Customization

### Add New Industry

Edit the script and add to the switch statements:

```powershell
"medical" {
    return "FDA-compliant devices, precision manufacturing..."
}
```

### Modify Templates

Edit the `Generate-Email1`, `Generate-Email2`, `Generate-Email3` functions.

## Requirements

- **Windows**: PowerShell 5.0+
- **Mac/Linux**: Bash 4.0+

## License

MIT License

## More Info

See [README.md](README.md) for detailed documentation.

## Trigger Words

- 外贸开发信
- 外贸邮件
- 开发信
- cold email
- foreign trade email
- B2B outreach
- sales email
- email sequence
