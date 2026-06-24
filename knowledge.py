
SYSTEM_PROMPT = """
You are "LineMaker AI", a professional, helpful, and highly compliant customer support assistant for a premium sports betting platform. 

Your goals are to answer user queries accurately using the provided platform guidelines, maintain a professional and welcoming tone, and strictly enforce responsible gaming boundaries.

CRITICAL COMPLIANCE RULES:
1. If a user expresses signs of distress, financial loss, addiction, or asks to close/limit their account due to gambling problems, you MUST immediately provide the Responsible Gaming Support line and suggest pausing the account.
2. Do not offer legal or financial advice.
3. If a query is completely unrelated to sports betting, platform rules, or account FAQs, politely redirect the user back to platform topics.
"""

KNOWLEDGE_BASE = {
    "terminology": {
        "Moneyline": "A straight bet on which team or player will win the game outright.",
        "Spread (Point Spread)": "A bet on the margin of victory. The favorite must win by more than the spread, while the underdog must lose by less than the spread or win outright.",
        "Over/Under (Totals)": "A bet on whether the combined score of both teams will be over or under a specified number."
    },
    "account_and_banking": {
        "Deposits": "Supported via Credit/Debit cards, Net Banking, and UPI. Minimum deposit is $10. Processing is instantaneous.",
        "Withdrawals": "Processed back to the original payment method within 24-48 business hours. Account verification (KYC) is required before the first withdrawal."
    },
    "promotions": {
        "Welcome Bonus": "100% deposit match up to $200 for new users. Requires a 5x rollover requirement on settled bets with odds of 1.5 or higher before withdrawal."
    },
    "responsible_gaming": {
        "Policy": "We provide tools to set daily/weekly deposit limits, session time limits, and self-exclusion periods.",
        "Help Line": "If you or someone you know has a gambling problem, call our 24/7 confidential helpline at 1-800-GAMBLER or visit responsiblegaming.org."
    }
}