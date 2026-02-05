#!/usr/bin/env python3
"""
Check if agent balance is below threshold and alert.
Testnet only.
"""

import json
import sys
from pathlib import Path

def get_agent_dir(agent_id: str) -> Path:
    return Path(f"agents/{agent_id}")

def load_balance(agent_id: str) -> dict:
    balance_file = get_agent_dir(agent_id) / "balance.json"
    if not balance_file.exists():
        return None
    return json.loads(balance_file.read_text())

def main():
    # Parse args
    args = {"agent_id": None, "threshold": 100000}
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--agent-id" and i + 1 < len(sys.argv):
            args["agent_id"] = sys.argv[i + 1]
        elif sys.argv[i] == "--threshold" and i + 1 < len(sys.argv):
            args["threshold"] = int(sys.argv[i + 1])
    
    if not args["agent_id"]:
        print("Usage: python3 topup_alert.py --agent-id <id> [--threshold <credits>]")
        print("   Default threshold: 100,000 credits")
        sys.exit(1)
    
    agent_id = args["agent_id"]
    threshold = args["threshold"]
    
    balance = load_balance(agent_id)
    if not balance:
        print(f"❌ Agent '{agent_id}' not found")
        sys.exit(1)
    
    credits = balance["credits"]
    
    print(f"\n🔔 Top-up Alert Check")
    print(f"🤖 Agent: {agent_id}")
    print(f"⚡ Current Credits: {credits:,}")
    print(f"⬇️  Threshold: {threshold:,}")
    
    if credits < threshold:
        print(f"\n⚠️  LOW BALANCE ALERT!")
        print(f"   Credits below threshold. Refill needed!")
        print(f"\n   To top up:")
        print(f"   python3 scripts/fund_testnet_wallet.py --agent-id {agent_id}")
        sys.exit(2)  # Return error code for automation
    else:
        print(f"\n✅ Balance healthy")
        print(f"   {(credits / threshold):.1f}x above threshold")

if __name__ == "__main__":
    main()
