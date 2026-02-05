# OpenRouter Model Pricing

Pricing per 1 million tokens (input/output). Based on OpenRouter public pricing.

## Cheap Models (Good for Agents)

| Model | Input | Output | Use Case |
|-------|-------|--------|----------|
| meta-llama/llama-3.1-8b-instruct | $0.02 | $0.02 | Fast, cheap, local-like |
| google/gemini-flash-1.5 | $0.075 | $0.30 | Good balance |
| openai/gpt-4o-mini | $0.15 | $0.60 | Reliable, fast |
| anthropic/claude-3-haiku | $0.25 | $1.25 | Decent quality |

## Mid-Range

| Model | Input | Output | Use Case |
|-------|-------|--------|----------|
| openai/gpt-4o | $2.50 | $10.00 | High quality |
| anthropic/claude-3.5-sonnet | $3.00 | $15.00 | Best reasoning |

## Premium (Expensive)

| Model | Input | Output | Use Case |
|-------|-------|--------|----------|
| openai/gpt-5 | $120.00 | $120.00 | Only when necessary |
| anthropic/claude-3-opus | $15.00 | $75.00 | Complex tasks |

## Credit Conversion

- **1 USDC** = **1,000,000 credits**
- Cost in credits = (USDC cost) × 100 × 10,000

Example:
- GPT-4o-mini call costs $0.0015
- = 150 credits
- With 10 USDC = 10M credits = ~66,667 GPT-4o-mini calls

## Notes

- OpenRouter charges 5.5% fee on credit purchases (not applicable in testnet demo)
- Prices subject to change - check https://openrouter.ai/pricing
- Some models have free tiers with rate limits
