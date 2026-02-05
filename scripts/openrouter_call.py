#!/usr/bin/env python3
"""
Make OpenRouter API call and deduct credits from agent balance.
Testnet only - uses demo API key, no real charges.
"""

import json
import os
import sys
from pathlib import Path

# Demo pricing per 1K tokens (approximate, for hackathon demo)
MODEL_PRICING = {
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.60},  # per 1M tokens
    "openai/gpt-4o": {"input": 2.50, "output": 10.00},
    "anthropic/claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
    "anthropic/claude-3-haiku": {"input": 0.25, "output": 1.25},
    "google/gemini-flash-1.5": {"input": 0.075, "output": 0.30},
    "meta-llama/llama-3.1-8b-instruct": {"input": 0.02, "output": 0.02},
}

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

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost in USDC cents."""
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["openai/gpt-4o-mini"])
    
    input_cost = (input_tokens / 1000000) * pricing["input"] * 100  # cents
    output_cost = (output_tokens / 1000000) * pricing["output"] * 100
    
    return input_cost + output_cost

def mock_openrouter_call(prompt: str, model: str) -> dict:
    """
    Mock OpenRouter API call for demo.
    In real implementation, this would call https://openrouter.ai/api/v1/chat/completions
    """
    # Simulate response
    mock_responses = {
        "meaning of life": "The meaning of life is a philosophical question concerning the significance of living or existence in general. Many philosophical and religious traditions suggest that life's meaning is found in achieving virtue, happiness, or connection with others.",
        "hello": "Hello! I'm an AI assistant running on OpenRouter. How can I help you today?",
        "default": f"This is a mock response to: '{prompt[:50]}...' In production, this would call OpenRouter API."
    }
    
    prompt_lower = prompt.lower()
    response_text = mock_responses["default"]
    for key in mock_responses:
        if key in prompt_lower:
            response_text = mock_responses[key]
            break
    
    # Estimate tokens (rough approximation: 1 token ≈ 4 chars)
    input_tokens = len(prompt) // 4
    output_tokens = len(response_text) // 4
    
    return {
        "content": response_text,
        "model": model,
        "usage": {
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens
        }
    }

def main():
    # Parse args
    args = {"agent_id": None, "model": "openai/gpt-4o-mini", "prompt": None}
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--agent-id" and i + 1 < len(sys.argv):
            args["agent_id"] = sys.argv[i + 1]
        elif sys.argv[i] == "--model" and i + 1 < len(sys.argv):
            args["model"] = sys.argv[i + 1]
        elif sys.argv[i] == "--prompt" and i + 1 < len(sys.argv):
            args["prompt"] = sys.argv[i + 1]
    
    if not args["agent_id"] or not args["prompt"]:
        print("Usage: python3 openrouter_call.py --agent-id <id> --prompt <text> [--model <model>]")
        print(f"\nAvailable models:")
        for m in MODEL_PRICING:
            print(f"  - {m}")
        sys.exit(1)
    
    agent_id = args["agent_id"]
    model = args["model"]
    prompt = args["prompt"]
    
    # Load balance
    balance = load_balance(agent_id)
    
    # Make mock API call
    print(f"\n🤖 Agent: {agent_id}")
    print(f"📤 Calling OpenRouter ({model})...")
    print(f"💬 Prompt: {prompt[:60]}{'...' if len(prompt) > 60 else ''}")
    
    result = mock_openrouter_call(prompt, model)
    
    # Calculate cost
    cost_cents = calculate_cost(model, result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"])
    cost_credits = int(cost_cents * 10000)  # Convert to credits
    
    # Check if agent has enough credits
    if balance["credits"] < cost_credits:
        print(f"\n❌ Insufficient credits!")
        print(f"   Required: {cost_credits:,} credits")
        print(f"   Available: {balance['credits']:,} credits")
        print(f"\n   Fund wallet with testnet USDC:")
        print(f"   python3 scripts/fund_testnet_wallet.py --agent-id {agent_id}")
        sys.exit(1)
    
    # Deduct credits
    balance["credits"] -= cost_credits
    save_balance(agent_id, balance)
    
    # Display result
    print(f"\n✅ Response:")
    print(f"   {result['content']}")
    print(f"\n📊 Usage:")
    print(f"   Input tokens: {result['usage']['prompt_tokens']:,}")
    print(f"   Output tokens: {result['usage']['completion_tokens']:,}")
    print(f"   Cost: {cost_credits:,} credits (${cost_cents/100:.4f} USDC)")
    print(f"\n💰 Remaining credits: {balance['credits']:,}")

if __name__ == "__main__":
    main()
