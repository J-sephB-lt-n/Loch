import jinja2

from .extract_semantic_triples import extract_semantic_triples_prompt
from .process_text import process_text_prompt
from .query_processed_file_contents import query_processed_file_contents_prompt

prompts_env = jinja2.Environment()

extract_semantic_triples = prompts_env.from_string(extract_semantic_triples_prompt)
process_text = prompts_env.from_string(process_text_prompt)
query_processed_file_contents = prompts_env.from_string(
    query_processed_file_contents_prompt
)
