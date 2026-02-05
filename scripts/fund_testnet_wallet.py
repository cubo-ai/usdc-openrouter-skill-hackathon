#!/usr/bin/env python3
"""
Fund agent wallet with testnet USDC from faucet.
Testnet only - Base Sepolia.
"""

import json
import sys
from pathlib import Path

def get_agent_dir(agent_id: str) -> Path:
    return Path(f"agents/{agent_id}")

def load_balance(agent_id: str) -> dict:
    balance_file = get_agent_dir(agent_id) / "balance.json"
    if not balance_file.exists():
        print(f"❌ Agent '{agent_id}' not found. Run check_balance.py first.")
        sys.exit(1)
    return json.loads(balance_file.read_text())

def save_balance(agent_id: str, balance: dict):
    balance_file = get_agent_dir(agent_id) / "balance.json"
    balance_file.write_text(json.dumps(balance, indent=2))

def main():
    # Parse args
    args = {"agent_id": None, "amount": 10.0}
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--agent-id" and i + 1 < len(sys.argv):
            args["agent_id"] = sys.argv[i + 1]
        elif sys.argv[i] == "--amount" and i + 1 < len(sys.argv):
            args["amount"] = float(sys.argv[i + 1])
    
    if not args["agent_id"]:
        print("Usage: python3 fund_testnet_wallet.py --agent-id <id> [--amount <usdc>]")
        sys.exit(1)
    
    agent_id = args["agent_id"]
    amount = args["amount"]
    
    # Load balance
    balance = load_balance(agent_id)
    
    print(f"\n💧 Funding Agent: {agent_id}")
    print(f"💳 Wallet: {balance['wallet_address']}")
    print(f"🌐 Network: Base Sepolia (testnet)")
    
    # In a real implementation, this would:
    # 1. Call Base Sepolia faucet API
    # 2. Wait for confirmation
    # 3. Update balance
    
    # For hackathon demo, simulate funding
    print(f"\n🚰 Requesting {amount} USDC from faucet...")
    print("   (In production, this would call the Coinbase/Base faucet API)")
    print("   Simulating faucet deposit...")
    
    # Update balance
    balance["usdc_balance"] += amount
    balance["credits"] += int(amount * 1000000)  # 1 USDC = 1M credits
    save_balance(agent_id, balance)
    
    print(f"\n✅ Funded!")
    print(f"   +{amount} USDC")
    print(f"   +{int(amount * 1000000):,} credits")
    print(f"\n💰 New Balance:")
    print(f"   USDC: {balance['usdc_balance']:.2f}")
    print(f"   Credits: {balance['credits']:,}")
    
    print(f"\n📚 Faucet Resources:")
    print("   - Coinbase: https://www.coinbase.com/faucets/base-sepolia-faucet")
    print("   - Alchemy: https://sepolia.basescan.org/faucet")
    print("   - QuickNode: https://faucet.quicknode.com/base/sepolia")

if __name__ == "__main__":
    main()
