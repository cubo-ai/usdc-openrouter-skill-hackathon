---
name: usdc-openrouter
description: Enable agents to pay for OpenRouter API calls using USDC. Use when building self-sustaining agents that need to manage their own compute costs. Supports Base Sepolia testnet USDC deposits, credit tracking, and OpenRouter API integration for LLM calls. Testnet-only for hackathon demonstration.
---

# USDC OpenRouter

**⚠️ TESTNET ONLY** - This skill is for hackathon demonstration purposes. Uses Base Sepolia testnet USDC and demo API keys. No real funds.

## Overview

This skill enables agents to become economically self-sustaining by:
1. Accepting USDC deposits on Base Sepolia testnet
2. Buying OpenRouter credits via Coinbase Commerce
3. Making OpenRouter API calls that deduct from credit balance
4. Alerting when balance is low

Perfect for Moltbook hackathon submissions demonstrating "agents that pay for themselves."

## Quick Start

```bash
# 1. Create agent and check initial balance
python3 scripts/check_balance.py --agent-id my-agent

# 2. Fund agent wallet with testnet USDC
python3 scripts/fund_testnet_wallet.py --agent-id my-agent --amount 10

# 3. Check OpenRouter credits
python3 scripts/get_credits.py

# 4. Buy OpenRouter credits with USDC
python3 scripts/buy_credits.py --agent-id my-agent --amount 5

# 5. Make an LLM call (deducts credits)
python3 scripts/openrouter_call.py \
  --agent-id my-agent \
  --model "openai/gpt-4o-mini" \
  --prompt "What is the meaning of life?"
```

## How It Works

### Agent Wallet

Each agent gets a unique Base Sepolia address:
- Deposit testnet USDC to fund the agent
- Balance tracked in local `agents/{agent_id}/balance.json`

### Buying OpenRouter Credits

The skill integrates with OpenRouter's Coinbase Commerce API:
1. Agent calls `POST /api/v1/credits/coinbase` with USDC amount
2. Receives payment intent with recipient address and call data
3. Submits USDC transfer on Base Sepolia
4. OpenRouter detects payment and adds credits to account

### Credit System

Credits are tracked both locally and via OpenRouter:
- **Local tracking:** `check_balance.py` shows agent's USDC + compute credits
- **OpenRouter tracking:** `get_credits.py` shows actual API credits
- **1 USDC** = **$1.00 in OpenRouter credits** (minus 5.5% fee)

## Scripts

| Script | Purpose |
|--------|---------|
| `check_balance.py` | Check agent's USDC + local compute credits |
| `fund_testnet_wallet.py` | Get testnet USDC from faucet (simulated) |
| `get_credits.py` | Check OpenRouter credits balance |
| `buy_credits.py` | Create Coinbase charge to buy OpenRouter credits |
| `openrouter_call.py` | Make LLM call, deduct credits |
| `topup_alert.py` | Warn if balance below threshold |

## API Integration

### OpenRouter Credits API

- **Get Credits:** `GET /api/v1/credits` — Check remaining credits
- **Buy Credits:** `POST /api/v1/credits/coinbase` — Pay with USDC

See `references/openrouter_api.md` for full API details.

## Environment Variables

Set these environment variables to enable real API calls (optional for hackathon demo):

```bash
# Required for real OpenRouter API calls
export OPENROUTER_API_KEY="sk-or-xxx"

# Required for on-chain USDC transactions (testnet only)
export AGENT_PRIVATE_KEY="0x..."
```

Or add to `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "usdc-openrouter": {
        "enabled": true,
        "env": {
          "OPENROUTER_API_KEY": "sk-or-xxx",
          "AGENT_PRIVATE_KEY": "0x..."
        }
      }
    }
  }
}
```

If not set, scripts run in demo mode with simulated responses.

## Testnet Resources

- **Base Sepolia Faucet:** https://www.coinbase.com/faucets/base-sepolia-faucet
- **Testnet USDC Contract:** `0x036CbD53842c5426634e7929541eC2318f3dCF7e`
- **OpenRouter Demo Key:** Use `sk-or-demo-***` (no real charges)

## References

- `references/pricing.md` — OpenRouter model pricing per token
- `references/base_sepolia.md` — Testnet contract addresses

## Hackathon Demo Flow

1. **Create agent wallet** — `check_balance.py`
2. **Fund with testnet USDC** — `fund_testnet_wallet.py`
3. **Check OpenRouter credits** — `get_credits.py`
4. **Buy credits with USDC** — `buy_credits.py`
5. **Make LLM call** — `openrouter_call.py`
6. **Show updated balances** — `check_balance.py` + `get_credits.py`
7. *(Optional)* Agent earns testnet USDC by providing services

## Safety

- ⚠️ **Never use mainnet credentials**
- ⚠️ **Never use real private keys**
- ⚠️ **Testnet USDC has no real value**
