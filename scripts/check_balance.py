#!/usr/bin/env python3
"""
Check agent's USDC balance and compute credits.
Testnet only - Base Sepolia.
"""

import json
import os
import sys
from pathlib import Path

def get_agent_dir(agent_id: str) -> Path:
    """Get or create agent directory."""
    agent_dir = Path(f"agents/{agent_id}")
    agent_dir.mkdir(parents=True, exist_ok=True)
    return agent_dir

def init_balance(agent_id: str) -> dict:
    """Initialize balance file for new agent."""
    agent_dir = get_agent_dir(agent_id)
    balance_file = agent_dir / "balance.json"
    
    if not balance_file.exists():
        # Generate mock wallet address for demo
        wallet_address = f"0x{os.urandom(20).hex()}"
        balance = {
            "agent_id": agent_id,
            "wallet_address": wallet_address,
            "usdc_balance": 0.0,
            "credits": 0,
            "network": "base-sepolia",
            "demo_mode": True
        }
        balance_file.write_text(json.dumps(balance, indent=2))
    else:
        balance = json.loads(balance_file.read_text())
    
    return balance

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_balance.py --agent-id <agent_id>")
        sys.exit(1)
    
    # Parse args
    args = {}
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--agent-id" and i + 1 < len(sys.argv):
            args["agent_id"] = sys.argv[i + 1]
    
    agent_id = args.get("agent_id", "default-agent")
    
    # Get or init balance
    balance = init_balance(agent_id)
    
    # Display
    print(f"\n🤖 Agent: {balance['agent_id']}")
    print(f"💳 Wallet: {balance['wallet_address']}")
    print(f"🌐 Network: {balance['network']}")
    print(f"💰 USDC Balance: {balance['usdc_balance']:.2f} (testnet)")
    print(f"⚡ Compute Credits: {balance['credits']:,}")
    print(f"🔧 Demo Mode: {balance['demo_mode']}")
    print(f"\n📍 To fund: Send Base Sepolia USDC to {balance['wallet_address']}")
    print("   Faucet: https://www.coinbase.com/faucets/base-sepolia-faucet")

if __name__ == "__main__":
    main()
