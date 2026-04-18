import os
from dotenv import load_dotenv
load_dotenv()
print("OS ENV KEY:", os.getenv("GEMINI_API_KEY"))

import config
print("CONFIG KEY:", config.GEMINI_API_KEY)

try:
    from agent.llm import decide_with_llm
    print("Agent Result:", decide_with_llm("test", []))
except Exception as e:
    print("ERROR:", repr(e))
