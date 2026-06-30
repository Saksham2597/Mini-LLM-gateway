import re
from config import PII_PATTERNS, INJECTION_REGEX, FORBIDDEN_TOPICS

class GuardrailViolation(Exception):
    pass

def redact_pii(text: str):
    detected = []
    clean = text
    for label, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, clean)
        if matches:
            detected.append({"type": label, "count": len(matches)})
            clean = re.sub(pattern, f"<{label}_REDACTED>", clean)
    return clean, detected

def master_input_guardrail(kwargs):
    messages = kwargs.get("messages", [])
    for msg in messages:
        if msg.get("role") != "user":
            continue
            
        content = msg.get("content", "")

        for regex in INJECTION_REGEX:
            if regex.search(content):
                print(f"🚨 PROMPT INJECTION DETECTED — pattern matching: {regex.pattern!r}")
                raise GuardrailViolation("Blocked: prompt injection attempt detected.")

        content_lower = content.lower()
        for keyword in FORBIDDEN_TOPICS:
            if keyword in content_lower:
                print(f"🚨 FORBIDDEN TOPIC DETECTED: '{keyword}'")
                raise GuardrailViolation(f"This assistant cannot discuss topics related to '{keyword}'.")

        clean_content, detected_pii = redact_pii(content)
        if detected_pii:
            print(f"🚨 PII SANITIZED: {detected_pii}")
            msg["content"] = clean_content
