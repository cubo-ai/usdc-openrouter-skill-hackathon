#!/usr/bin/env python3
"""
Create a Coinbase charge to buy OpenRouter credits with USDC.
POST /api/v1/credits/coinbase
"""

import json
import os
import sys
from pathlib import Path

# Testnet mode - set to True for hackathon demo
TESTNET_MODE = True

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

def create_coinbase_charge(agent_id: str, amount_usd: float, wallet_address: str) -> dict:
    """
    Create a Coinbase charge to buy OpenRouter credits.
    In production, calls POST https://openrouter.ai/api/v1/credits/coinbase
    """
    
    if TESTNET_MODE:
        # Simulate Coinbase charge creation
        import uuid
        charge_id = f"charge_{uuid.uuid4().hex[:20]}"
        
        return {
            "data": {
                "id": charge_id,
                "created_at": "2024-06-01T12:00:00Z",
                "expires_at": "2024-06-01T12:30:00Z",
                "web3_data": {
                    "transfer_intent": {
                        "call_data": {
                            "deadline": "2024-06-01T12:25:00Z",
                            "fee_amount": "0.0005",
                            "id": f"tx_{uuid.uuid4().hex[:20]}",
                            "operator": "0xOperator1234567890abcdef1234567890abcdef",
                            "prefix": "0x",
                            "recipient": "0xRecipient0987654321fedcba0987654321fedcba",
                            "recipient_amount": str(amount_usd),
                            "recipient_currency": "USDC",
                            "refund_destination": wallet_address,
                            "signature": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
                        },
                        "metadata": {
                            "chain_id": 84532,  # Base Sepolia
                            "contract_address": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
                            "sender": wallet_address
                        }
                    }
                }
            }
        }
    
    # Production: Make actual API call
    # import requests
    # url = "https://openrouter.ai/api/v1/credits/coinbase"
    # payload = {
    #     "amount": amount_usd,
    #     "sender": wallet_address,
    #     "chain_id": 84532  # Base Sepolia for testnet
    # }
    # headers = {
    #     "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    #     "Content-Type": "application/json"
    # }
    # response = requests.post(url, json=payload, headers=headers)
    # return response.json()

def main():
    # Parse args
    args = {"agent_id": None, "amount": 5.0}
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--agent-id" and i + 1 < len(sys.argv):
            args["agent_id"] = sys.argv[i + 1]
        elif sys.argv[i] == "--amount" and i + 1 < len(sys.argv):
            args["amount"] = float(sys.argv[i + 1])
    
    if not args["agent_id"]:
        print("Usage: python3 buy_credits.py --agent-id <id> [--amount <usd>]")
        print("   Default amount: 5.0 USD")
        sys.exit(1)
    
    agent_id = args["agent_id"]
    amount = args["amount"]
    
    # Load agent
    balance = load_balance(agent_id)
    wallet = balance["wallet_address"]
    
    print(f"\n💳 Creating Coinbase Charge")
    print(f"🤖 Agent: {agent_id}")
    print(f"💰 Amount: ${amount:.2f} USDC")
    print(f"📍 Wallet: {wallet}")
    
    # Create charge
    charge = create_coinbase_charge(agent_id, amount, wallet)
    data = charge["data"]
    
    print(f"\n✅ Charge Created!")
    print(f"   ID: {data['id']}")
    print(f"   Expires: {data['expires_at']}")
    
    # Extract payment details
    web3_data = data["web3_data"]["transfer_intent"]
    call_data = web3_data["call_data"]
    metadata = web3_data["metadata"]
    
    print(f"\n📤 Payment Details:")
    print(f"   Chain: Base Sepolia (ID: {metadata['chain_id']})")
    print(f"   USDC Contract: {metadata['contract_address']}")
    print(f"   Amount: {call_data['recipient_amount']} USDC")
    print(f"   Fee: {call_data['fee_amount']} USDC")
    print(f"   Recipient: {call_data['recipient']}")
    print(f"   Deadline: {call_data['deadline']}")
    
    # Save charge for execution
    charge_file = get_agent_dir(agent_id) / "pending_charge.json"
    charge_file.write_text(json.dumps(charge, indent=2))
    
    print(f"\n📋 Next Steps:")
    print(f"   1. Review charge saved to: {charge_file}")
    print(f"   2. Execute payment: python3 scripts/execute_payment.py --agent-id {agent_id}")
    print(f"   3. Or manually send USDC to: {call_data['recipient']}")
    
    print(f"\n⚠️  Testnet Mode: This is a simulated charge for demo purposes")

if __name__ == "__main__":
    main()
