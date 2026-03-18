#!/bin/bash
# B2B Cold Email Writer v1.0.0
# Usage: bash b2b-cold.sh <command> [options]

VERSION="1.0.0"
INDUSTRY="general"
COMPANY=""
COUNTRY=""
PAINPOINT=""
VALUEPROP=""
SENDER=""
SENDER_COMPANY=""

show_help() {
    cat << 'EOF'
B2B Cold Email Writer v1.0.0

Commands:
  sequence    Generate 3-email sequence
  first       Email 1: Connection
  second      Email 2: Value
  third       Email 3: Action
  subject     Generate subject lines
  followup    Follow-up email
  help        Show help

Options:
  -i, --industry <type>      textile|electronics|packaging|machinery|consumer|general
  -c, --company <name>       Target company name
  -co, --country <country>   Target country
  -p, --painpoint <issue>    Customer pain point
  -v, --valueprop <value>    Your value proposition
  -s, --sender <name>        Sender name
  -sc, --sender-company <co> Sender company

Example:
  bash b2b-cold.sh sequence -i textile -c "Fashion Brand" -p "long lead time" -v "7-day delivery"
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -i|--industry) INDUSTRY="$2"; shift 2 ;;
            -c|--company) COMPANY="$2"; shift 2 ;;
            -co|--country) COUNTRY="$2"; shift 2 ;;
            -p|--painpoint) PAINPOINT="$2"; shift 2 ;;
            -v|--valueprop) VALUEPROP="$2"; shift 2 ;;
            -s|--sender) SENDER="$2"; shift 2 ;;
            -sc|--sender-company) SENDER_COMPANY="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
}

get_compliment() {
    case $1 in
        textile) echo "I've been following your brand and love how you've been pushing the boundaries of fashion." ;;
        electronics) echo "I've been impressed by your company's innovation in the electronics space." ;;
        packaging) echo "I've been keeping an eye on your brand. The way you elevate product presentation is impressive." ;;
        machinery) echo "I've been following your company's growth in the industrial sector." ;;
        consumer) echo "I've been following your brand's journey and your innovative products." ;;
        *) echo "I've been following your company's growth and market presence." ;;
    esac
}

get_value() {
    case $1 in
        textile) echo "premium fabrics, sustainable materials, custom prints" ;;
        electronics) echo "reliable components, competitive pricing, strict quality control" ;;
        packaging) echo "custom packaging, eco-friendly materials, unique designs" ;;
        machinery) echo "precision-engineered parts, OEM/ODM services, technical support" ;;
        consumer) echo "high-quality manufacturing, flexible MOQ, fast samples" ;;
        *) echo "high-quality products, competitive pricing, reliable delivery" ;;
    esac
}

get_painpoint() {
    case $1 in
        textile) echo "quality inconsistency, long production cycles" ;;
        electronics) echo "component shortages, long lead times" ;;
        packaging) echo "high costs, environmental concerns" ;;
        machinery) echo "equipment downtime, parts availability" ;;
        consumer) echo "supplier reliability, delivery delays" ;;
        *) echo "supplier reliability, quality control" ;;
    esac
}

generate_subjects() {
    echo ""
    echo "=== HIGH-OPEN-RATE SUBJECT LINES ==="
    echo ""
    echo "1. Quick question about your $INDUSTRY sourcing"
    [[ -n "$PAINPOINT" ]] && echo "2. Solving $PAINPOINT for $INDUSTRY companies" || echo "2. A better way to source $INDUSTRY products"
    [[ -n "$COMPANY" ]] && echo "3. $COMPANY + potential collaboration" || echo "3. Idea for your $INDUSTRY business"
    echo "4. Are you open to a quick chat about $INDUSTRY?"
    echo "5. Last try: $INDUSTRY opportunity"
    echo ""
}

generate_email_1() {
    echo "=== EMAIL 1: BUILDING CONNECTION ==="
    echo ""
    echo "Subject: Quick question about your $INDUSTRY sourcing"
    echo ""
    echo "Hi there,"
    echo ""
    echo "$(get_compliment $INDUSTRY)"
    echo ""
    echo "I'm ${SENDER:-[Your Name]} from ${SENDER_COMPANY:-[Your Company]}. We specialize in $(get_value $INDUSTRY)."
    echo ""
    echo "I'm not trying to sell you anything today—I just wanted to introduce myself and see if there's an opportunity for us to connect."
    [[ -n "$COUNTRY" ]] && echo "We've worked with several $COUNTRY companies already." || echo "We've helped many companies in the $INDUSTRY space."
    echo ""
    echo "If you have a few minutes next week, I'd be happy to chat about what trends or challenges you're seeing."
    echo ""
    echo "Any thoughts?"
    echo ""
    echo "Best regards,"
    echo "${SENDER:-[Your Name]}"
    echo "${SENDER_COMPANY:-[Your Company]}"
    echo ""
}

generate_email_2() {
    local pp=${PAINPOINT:-$(get_painpoint $INDUSTRY)}
    local vp=${VALUEPROP:-$(get_value $INDUSTRY)}
    echo "=== EMAIL 2: DELIVERING VALUE ==="
    echo ""
    echo "Subject: Re: Quick question about your $INDUSTRY sourcing"
    echo ""
    echo "Hi there,"
    echo ""
    echo "I wanted to follow up and share something that might interest you."
    echo ""
    echo "Many $INDUSTRY companies we work with were struggling with $pp before they found us."
    echo ""
    echo "Here's what we bring to the table:"
    echo "• $vp"
    echo "• Dedicated account management"
    echo "• Flexible terms for growing businesses"
    echo ""
    echo "One of our clients saw a 30% improvement in their supply chain efficiency within 3 months of working with us."
    echo ""
    echo "Would you be open to a brief call to explore if we could help ${COMPANY:-your company} achieve similar results?"
    echo ""
    echo "Best regards,"
    echo "${SENDER:-[Your Name]}"
    echo "${SENDER_COMPANY:-[Your Company]}"
    echo ""
}

generate_email_3() {
    echo "=== EMAIL 3: CALL TO ACTION ==="
    echo ""
    echo "Subject: Last try: $INDUSTRY opportunity for ${COMPANY:-your company}"
    echo ""
    echo "Hi there,"
    echo ""
    echo "I don't want to clutter your inbox, so this will be my last email unless I hear back from you."
    echo ""
    echo "I truly believe we could help ${COMPANY:-your company} with:"
    echo "• ${VALUEPROP:-Better quality and faster delivery}"
    echo "• Reducing supply chain headaches"
    echo "• Competitive pricing without compromising quality"
    echo ""
    echo "If now isn't the right time, I completely understand. Just reply with \"not now\" and I'll circle back in a few months."
    echo ""
    echo "Otherwise, here's my calendar link: [Your Calendar Link]"
    echo "Or simply reply with a time that works for you."
    echo ""
    echo "Best regards,"
    echo "${SENDER:-[Your Name]}"
    echo "${SENDER_COMPANY:-[Your Company]}"
    echo "[Your Phone/WhatsApp]"
    echo ""
}

generate_followup() {
    echo "=== FOLLOW-UP EMAIL (No Reply) ==="
    echo ""
    echo "Subject: Bumping this up - $INDUSTRY sourcing"
    echo ""
    echo "Hi there,"
    echo ""
    echo "I know you're busy, so I'll keep this short."
    echo ""
    echo "I reached out about ${VALUEPROP:-how we could help with your $INDUSTRY sourcing} and wanted to make sure my email didn't get lost in your inbox."
    echo ""
    echo "If this isn't a priority right now, no worries at all. Just let me know and I'll follow up at a better time."
    echo ""
    echo "If it is, I'd love to jump on a quick 10-minute call to see if we're a good fit."
    echo ""
    echo "What works best for you?"
    echo ""
    echo "Best regards,"
    echo "${SENDER:-[Your Name]}"
    echo "${SENDER_COMPANY:-[Your Company]}"
    echo ""
}

## Main
case "${1:-help}" in

# Main
case "${1:-help}" in
    sequence)
        shift
        parse_args "$@"
        generate_subjects
        generate_email_1
        generate_email_2
        generate_email_3
        ;;
    first)
        shift
        parse_args "$@"
        generate_email_1
        ;;
    second)
        shift
        parse_args "$@"
        generate_email_2
        ;;
    third)
        shift
        parse_args "$@"
        generate_email_3
        ;;
    subject)
        shift
        parse_args "$@"
        generate_subjects
        ;;
    followup)
        shift
        parse_args "$@"
        generate_followup
        ;;
    help|--help|-h|*)
        show_help
        ;;
esac
