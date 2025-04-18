import jinja2

from .process_text import process_text_prompt

prompts_env = jinja2.Environment()

process_text = prompts_env.from_string(process_text_prompt)
