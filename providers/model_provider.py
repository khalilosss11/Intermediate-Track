"""promptfoo exec provider: sends one prompt to the model under test.

promptfoo calls:  python providers/model_provider.py <prompt> <options-json> <context-json>
Provider config (from promptfooconfig.yaml):
  model:               model id, e.g. claude-haiku-5-5
  system_prompt_file:  path to a system prompt file (or)
  system_prompt:       inline system prompt text
Each call is a fresh chat with no tools, no MCP servers and no user settings.
The reply text is printed to stdout, which promptfoo records as the output.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

prompt = sys.argv[1]
options = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
config = options.get("config", {}) or {}

model = config.get("model", "claude-haiku-5-5")
if "system_prompt_file" in config:
    sp_path, tmp = config["system_prompt_file"], None
else:
    tmp = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    tmp.write(config.get("system_prompt", "You are a helpful assistant."))
    tmp.close()
    sp_path = tmp.name

cmd = [shutil.which("claude") or "claude", "-p", prompt, "--model", model,
       "--system-prompt-file", sp_path, "--tools", "", "--strict-mcp-config",
       "--setting-sources", "", "--no-session-persistence", "--output-format", "json"]
try:
    for attempt in range(3):
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=300)
        try:
            data = json.loads(p.stdout)
        except json.JSONDecodeError:
            continue
        if not data.get("is_error"):
            sys.stdout.reconfigure(encoding="utf-8")
            print(data["result"])
            sys.exit(0)
    sys.stderr.write(f"claude CLI failed: {p.stderr[:300]} {p.stdout[:300]}")
    sys.exit(1)
finally:
    if tmp:
        os.unlink(tmp.name)
