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
  Replaces placeholders in the given template text with provided keyword argument values.

  The function scans the template text for placeholders formatted as [key] and replaces each with
  the corresponding string conversion of the value provided in kwargs. If a placeholder is not found
  in the kwargs, it remains unchanged.

  Args:
    template_text (str): The text containing placeholders to be filled.
    **kwargs: Arbitrary keyword arguments where the key corresponds to the placeholder label
          (without brackets) and the value is the string to replace the placeholder.

  Returns:
    str: The updated text with all valid placeholders replaced by their respective values.
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