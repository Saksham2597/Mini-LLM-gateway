import time
import litellm
from litellm import completion, completion_cost
from config import ROUTING_CHAINS
from guardrails import master_input_guardrail

litellm.input_callback = [master_input_guardrail]

def classify_task(user_query: str) -> str:
    try:
        cls = completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": (
                    f"Classify the following query into EXACTLY one word: "
                    f"'code', 'summary', or 'general'. Query: {user_query}\n\nAnswer:"
                )
            }],
            max_tokens=5
        )
        return cls.choices[0].message.content.strip().lower()
    except Exception:
        return "general"

def call_with_fallbacks(model_chain, messages):
    last_error = None
    for model in model_chain:
        try:
            return completion(model=model, messages=messages)
        except Exception as e:
            print(f"    ⚠️  Model {model} failed ({type(e).__name__}), switching to next tier...")
            last_error = e
            continue
    raise last_error

def smart_chat(user_query: str):
    task = classify_task(user_query)
    model_chain = ROUTING_CHAINS.get(task, ROUTING_CHAINS["general"])

    start_time = time.time()
    response = call_with_fallbacks(
        model_chain=model_chain,
        messages=[{"role": "user", "content": user_query}]
    )
    latency = time.time() - start_time

    try:
        cost = completion_cost(completion_response=response)
        cost_str = f"${cost:.6f}"
    except Exception:
        cost_str = "n/a"

    return {
        "detected_task": task,
        "model_used":    response.model,
        "answer":        response.choices[0].message.content,
        "latency_sec":   round(latency, 2),
        "cost_usd":      cost_str
    }
