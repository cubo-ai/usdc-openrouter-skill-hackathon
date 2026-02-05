---
name: usdc-openrouter
description: Enable agents to pay for OpenRouter API calls using USDC. Use when building self-sustaining agents that need to manage their own compute costs on testnet. Supports Base Sepolia testnet USDC deposits, credit tracking, and OpenRouter API integration for LLM calls.
---

# USDC OpenRouter

**⚠️ TESTNET ONLY** - This skill is for hackathon demonstration purposes. Uses Base Sepolia testnet USDC and demo API keys. No real funds.

## Overview

This skill enables agents to become economically self-sustaining by:
1. Accepting USDC deposits on Base Sepolia testnet
2. Tracking agent "compute credits" locally
3. Making OpenRouter API calls that deduct from credit balance
4. Alerting when balance is low

Perfect for Moltbook hackathon submissions demonstrating "agents that pay for themselves."

## Quick Start

```bash
# 1. Fund agent wallet with Base Sepolia USDC
python3 scripts/fund_testnet_wallet.py --agent-id my-agent

# 2. Check agent's credit balance
python3 scripts/check_balance.py --agent-id my-agent

# 3. Make an LLM call (deducts credits)
python3 scripts/openrouter_call.py \
  --agent-id my-agent \
  --model "openai/gpt-4o-mini" \
  --prompt "What is the meaning of life?"
```

## How It Works

### Credit System (Demo Mode)

Since this is testnet-only, credits are tracked locally:
- **1 USDC** = **1,000,000 credits**
- Credits deducted based on OpenRouter pricing (see `references/pricing.md`)
- Demo API key used for OpenRouter calls (no real charges)

### Agent Wallet

Each agent gets a unique Base Sepolia address:
- Deposit testnet USDC to fund the agent
- Balance tracked in local `agents/{agent_id}/balance.json`

## Scripts

| Script | Purpose |
|--------|---------|
| `fund_testnet_wallet.py` | Get testnet USDC from faucet |
| `check_balance.py` | Check USDC + compute credits |
| `openrouter_call.py` | Make LLM call, deduct credits |
| `topup_alert.py` | Warn if balance below threshold |

## Testnet Resources

- **Base Sepolia Faucet:** https://www.coinbase.com/faucets/base-sepolia-faucet
- **Testnet USDC Contract:** `0x036CbD53842c5426634e7929541eC2318f3dCF7e`
- **OpenRouter Demo Key:** Use `sk-or-demo-***` (no real charges)

## References

- `references/pricing.md` - OpenRouter model pricing per token
- `references/base_sepolia.md` - Testnet contract addresses

## Hackathon Demo Flow

1. Create agent wallet
2. Fund with testnet USDC (faucet)
3. Show credit balance
4. Make LLM call
5. Show updated balance
6. (Optional) Agent earns testnet USDC by providing services

## Safety

- ⚠️ **Never use mainnet credentials**
- ⚠️ **Never use real private keys**
- ⚠️ **Testnet USDC has no real value**
