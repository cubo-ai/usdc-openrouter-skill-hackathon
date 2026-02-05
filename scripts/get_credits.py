#!/usr/bin/env python3
"""
Get OpenRouter credits balance.
GET /api/v1/credits (requires provisioning key)
"""

import json
import os
import sys
from pathlib import Path

TESTNET_MODE = True

def get_openrouter_credits() -> dict:
    """
    Get OpenRouter credits balance.
    In production, calls GET https://openrouter.ai/api/v1/credits
    Requires provisioning API key.
    """
    
    if TESTNET_MODE:
        # Return mock data
        return {
            "data": {
                "total_credits": 10000000,  # $100.00
                "total_usage": 2500000,     # $25.00 used
                "remaining_credits": 7500000  # $75.00 remaining
            }
        }
    
    # Production: Make actual API call
    # import requests
    # url = "https://openrouter.ai/api/v1/credits"
    # headers = {
    #     "Authorization": f"Bearer {os.getenv('OPENROUTER_PROVISIONING_KEY')}"
    # }
    # response = requests.get(url, headers=headers)
    # return response.json()

def format_credits(credits: int) -> str:
    """Format credits as dollars (1 credit = $0.0001)."""
    return f"${credits / 10000:.2f}"

def main():
    print("\n🔍 Checking OpenRouter Credits")
    print("-" * 40)
    
    credits = get_openrouter_credits()
    data = credits["data"]
    
    print(f"💰 Total Credits Purchased: {format_credits(data['total_credits'])}")
    print(f"📊 Total Usage:            {format_credits(data['total_usage'])}")
    print(f"⚡ Remaining Credits:       {format_credits(data['remaining_credits'])}")
    
    print("\n📚 To add credits:")
    print("   python3 scripts/buy_credits.py --agent-id <agent_id> --amount <usd>")
    
    if TESTNET_MODE:
        print("\n⚠️  Testnet Mode: Showing simulated data")

if __name__ == "__main__":
    main()
