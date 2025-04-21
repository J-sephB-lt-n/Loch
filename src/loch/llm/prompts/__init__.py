import jinja2

from .process_text import process_text_prompt
from .query_processed_file_contents import query_processed_file_contents_prompt

prompts_env = jinja2.Environment()

process_text = prompts_env.from_string(process_text_prompt)
query_processed_file_contents = prompts_env.from_string(
    query_processed_file_contents_prompt
)
