"""
Default prompts used by Large Language Models
"""

from typing import Final

import jinja2

prompts_env = jinja2.Environment()

HYDE_PROMPT: Final[str] = """
Write a paragraph which answers this question: 
"{{ question }}"
""".strip()

HYDE = prompts_env.from_string(HYDE_PROMPT)
