# Mini-LLM-Gateway 🚀

A lightweight, high-performance, and extensible API gateway designed for Large Language Models (LLMs). **Mini-LLM-Gateway** acts as a centralized proxy between your applications and various LLM providers, offering unified endpoints, load balancing, rate limiting, and observability.

---

## 🌟 Features

- **Unified API Interface:** Switch between different LLM providers (e.g., OpenAI, Anthropic, local models via Ollama) using a single, standardized API request format.
- **Load Balancing & Failover:** Distribute traffic across multiple provider instances or automatically fallback to a secondary model/provider if the primary one fails or hits rate limits.
- **Authentication & Rate Limiting:** Secure your gateway endpoints with API key validation and protect your backend resources with per-user or global rate limiting.
- **Request/Response Logging:** Monitor usage, track latency, and audit token consumption with built-in logging.
- **Extensible Architecture:** Easily plug in custom middleware for caching, prompt guardrails, or content moderation.

---

## 🏗️ Architecture Overview

```text
 [ Client Application ]
         │
         ▼
 ┌──────────────────────┐
 │  Mini-LLM-Gateway    │  ──► [ Rate Limiting & Auth Middleware ]
 └──────────────────────┘  ──► [ Router / Load Balancer ]
         │
         ├──► [ OpenAI Provider ]
         ├──► [ Anthropic Provider ]
         └──► [ Local / Custom LLM (Ollama / vLLM) ]
