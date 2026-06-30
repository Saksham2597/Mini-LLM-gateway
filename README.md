# Mini-LLM-gateway 🚀

A lightweight, local-first intelligent LLM gateway and routing engine built with **LiteLLM**. This project dynamically classifies user intent to route queries to the most cost-effective model, provides automated multi-provider failover recovery, and enforces strict security guardrails entirely on your local machine before data ever hits an external API.

---

## 🏗️ Architecture & Features

This gateway acts as an intelligent proxy between your application and various LLM providers (OpenAI, Groq, etc.). It optimizes for three core metrics: **Cost**, **Latency**, and **Data Security**.

### 1. Intent-Based Routing
Every incoming query undergoes a pre-flight evaluation by a high-speed classifier model (`groq/llama-3.3-70b-versatile`). It categorizes the prompt into one of three buckets and maps it to a prioritized model chain:
* **Code**: Optimizes for logical reasoning (`gpt-4o` ➔ `gpt-4o-mini` ➔ Llama 3.3).
* **Summary**: Optimizes for token speed and value (`gpt-4o-mini` ➔ Llama 3.3).
* **General**: Default fallback path favoring rapid open-source endpoints (Llama 3.3 ➔ `gpt-4o-mini`).

### 2. Multi-Provider Resiliency (Fallbacks)
If a primary model faces a network timeout, rate limit (HTTP 429), or service outage, the gateway automatically intercepts the failure and cascades down to the next tier in the chain seamlessly without dropping the user's session.

### 3. Local Pre-Flight Guardrails
To prevent data leaks and malicious exploits, the gateway leverages LiteLLM's internal execution hooks (`input_callback`) to scrub data *locally*:
* **PII Sanitization**: Automatically matches and redacts sensitive patterns including Emails, US/Indian Phone Numbers, Social Security Numbers, Aadhaar, PAN Cards, Credit Cards, and IP Addresses.
* **Prompt Injection Blocking**: Intercepts and blocks systemic jailbreak variations (e.g., "Ignore all previous instructions", "You are now DAN").
* **Forbidden Content Policy**: Screens and hard-blocks keywords violating safe use guidelines (malware, hacking exploits, self-harm, etc.).

---

## 📂 Project Structure

```text
Mini-LLM-gateway/
├── config.py         # Global variables, routing chains, and regex patterns
├── guardrails.py     # Local pre-call security hooks and sanitizers
├── chatbot.py        # Routing logic, fallback loops, and cost tracking
├── main.py           # Verification script simulating edge-cases and happy paths
├── requirements.txt  # Project dependencies
└── README.md         # Documentation
