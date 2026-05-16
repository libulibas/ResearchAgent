import os, sys
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()
MODEL = "claude-sonnet-4-20250514"

def claude(prompt, system="", max_tokens=2000):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Set ANTHROPIC_API_KEY (copy .env.example to .env).")
    c = Anthropic(api_key=key)
    kw = dict(model=MODEL, max_tokens=max_tokens,
              messages=[{"role": "user", "content": prompt}])
    if system:
        kw["system"] = system
    r = c.messages.create(**kw)
    return "".join(b.text for b in r.content if b.type == "text")



def research(topic: str) -> str:
    sys_p = ("You are a research analyst. Produce a structured markdown report "
             "with: # Title, ## Executive Summary, ## Key Findings (bullets), "
             "## Detailed Analysis, ## Open Questions, ## Sources/Caveats.")
    return claude(f"Research this topic thoroughly: {topic}", system=sys_p,
                  max_tokens=3000)

if __name__ == "__main__":
    t = " ".join(sys.argv[1:]) or "The state of agentic AI in 2025"
    report = research(t)
    out = "report.md"
    open(out, "w", encoding="utf-8").write(report)
    print(report)
    print(f"\n[saved -> {out}]")
