query_processed_file_contents_prompt = """
<processed-file-contents>
{{ processed_file_contents }}
</processed-file-contents>

{{ user_query }}
""".strip()
