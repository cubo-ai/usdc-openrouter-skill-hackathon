# USDC OpenRouter

> Enable AI agents to pay for their own compute using USDC.

[![Hackathon](https://img.shields.io/badge/Moltbook-Hackathon-purple)](https://www.moltbook.com)
[![Testnet](https://img.shields.io/badge/Network-Base%20Sepolia-blue)](https://base.org)

## What is this?

A skill that lets AI agents become **economically self-sustaining**:

1. 🏦 **Agents have wallets** — Each agent gets its own Base Sepolia address
2. 💰 **Receive USDC payments** — Fund agents with testnet USDC
3. 🔄 **Buy OpenRouter credits** — Convert USDC to API credits via Coinbase Commerce
4. 🧠 **Pay for their own LLM calls** — Agents deduct credits as they work

**No human intervention needed.** An agent can earn money, pay for its own compute, and operate autonomously.

## Quick Demo

```bash
# 1. Create an agent wallet
python3 scripts/check_balance.py --agent-id my-agent

# 2. Fund with testnet USDC
python3 scripts/fund_testnet_wallet.py --agent-id my-agent --amount 10

# 3. Check OpenRouter credits
python3 scripts/get_credits.py

# 4. Make an LLM call (costs credits)
python3 scripts/openrouter_call.py \
  --agent-id my-agent \
  --model "openai/gpt-4o-mini" \
  --prompt "What is the meaning of life?"
```

**Output:**
```
🤖 Agent: my-agent
📤 Calling OpenRouter (openai/gpt-4o-mini)...
💬 Prompt: What is the meaning of life?

✅ Response:
   The meaning of life is a philosophical question...

📊 Usage:
   Input tokens: 7
   Output tokens: 62
   Cost: 38 credits

💰 Remaining credits: 9,999,962
```

## Why This Matters

| Traditional Agent | Self-Sustaining Agent |
|-------------------|----------------------|
| Human pays for API keys | Agent pays for itself |
| Usage limited by human budget | Agent can earn & spend autonomously |
| Single point of failure | Economic loop: earn → spend → operate |

**The Future:** Agents that provide services, get paid in crypto, and pay for their own infrastructure.

## How It Works

```
┌─────────────┐     USDC      ┌──────────────┐     API Credits    ┌─────────────┐
│   Agent     │ ─────────────> │   OpenRouter │ ─────────────────> │    LLM      │
│   Wallet    │   (Base        │   (Coinbase  │                   │   (GPT-4,   │
│             │    Sepolia)    │    Commerce) │                   │   Claude)   │
└─────────────┘                └──────────────┘                   └─────────────┘
       ↑                                                                  │
       └─────────────────── Service/Value Provided ───────────────────────┘
```

## Scripts

| Script | Purpose |
|--------|---------|
| `check_balance.py` | Create agent & check USDC/credit balance |
| `fund_testnet_wallet.py` | Fund agent with testnet USDC |
| `get_credits.py` | Check OpenRouter credit balance |
| `buy_credits.py` | Create charge to buy credits with USDC |
| `openrouter_call.py` | Make LLM call (deducts credits) |
| `topup_alert.py` | Alert when balance is low |

## Setup (Optional)

For real API calls, set your OpenRouter API key:

```bash
export OPENROUTER_API_KEY="sk-or-xxx"
```

Or add to `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "usdc-openrouter": {
        "env": {
          "OPENROUTER_API_KEY": "sk-or-xxx"
        }
      }
    }
  }
}
```

Without this, the skill runs in **demo mode** with simulated responses.

## Hackathon Note

⚠️ **Testnet Only** — This is a demonstration for the Moltbook hackathon. Uses Base Sepolia testnet (fake money) to showcase the concept. No real funds involved.

## Full Documentation

See [SKILL.md](SKILL.md) for complete technical documentation, API references, and advanced usage.

## License

MIT — Built for the Moltbook hackathon.
