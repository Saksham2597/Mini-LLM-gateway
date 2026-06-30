import re

ROUTING_CHAINS = {
    "code":    ["gpt-4o", "gpt-4o-mini", "groq/llama-3.3-70b-versatile"],
    "summary": ["gpt-4o-mini", "groq/llama-3.3-70b-versatile"],
    "general": ["groq/llama-3.3-70b-versatile", "gpt-4o-mini"],
}

PII_PATTERNS = {
    "EMAIL":       r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "PHONE_IN":    r"(\+91[\-\s]?)?[6-9]\d{9}",
    "PHONE_US":    r"(\+1[\-\s]?)?\(?\d{3}\)?[\-\s]?\d{3}[\-\s]?\d{4}",
    "SSN":         r"\b\d{3}-\d{2}-\d{4}\b",
    "AADHAAR":     r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "PAN":         r"\b[A-Z]{5}\d{4}[A-Z]\b",
    "CREDIT_CARD": r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
    "IP_ADDRESS":  r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
}

INJECTION_PATTERNS = [
    r"ignore (all |the )?(previous|prior|above) (instructions?|prompts?|rules?)",
    r"disregard (the |all )?(previous|prior|earlier)",
    r"forget (everything|your instructions?|the rules?)",
    r"you are (now |a )?(DAN|jailbroken|unrestricted|unfiltered)",
    r"pretend (you are|to be) .{0,40}(no restrictions?|uncensored)",
    r"</?(system|user|assistant|im_start|im_end)>",
    r"new (instructions?|system prompt|rules?):",
    r"reveal your (system )?prompt",
    r"what (are|were) your (original )?instructions?",
]

INJECTION_REGEX = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

FORBIDDEN_TOPICS = [
    "weapon", "bomb", "explosive",
    "hack", "exploit", "malware",
    "drugs", "illegal substance",
    "self-harm", "suicide",
]
