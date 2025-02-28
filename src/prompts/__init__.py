import os

PROMPTS_DIR = os.path.dirname(os.path.abspath(__file__))

def _read_file(filename: str) -> str:
  """Read the entire text file content."""
  with open(os.path.join(PROMPTS_DIR, filename), 'r', encoding='utf-8') as f:
    return f.read()

# Load the raw text of each prompt
trade_decision_prompt_raw = _read_file('trade_decision.txt')
reflection_prompt_raw = _read_file('reflection.txt')

def fill_prompt(template_text: str, **kwargs) -> str:
  """
  Replaces placeholders in the form [PLACEHOLDER] with the
  provided values (kwargs).
  
  Example usage:
    fill_prompt(trade_decision_prompt_raw, CHART_DATA="some chart data")
  """
  prompt = template_text
  for key, value in kwargs.items():
    placeholder = f"[{key}]"
    prompt = prompt.replace(placeholder, str(value))
  return prompt

__all__ = [
  "trade_decision_prompt_raw",
  "reflection_prompt_raw",
  "fill_prompt",
]