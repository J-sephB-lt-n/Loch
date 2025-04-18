process_text_prompt = """
<input-text>
{{ input_text }}
</input-text>

<processing-instructions>
{{ processing_instructions }}
</processing-instructions>

Please process the input text according to the processing instructions.
Return only the processed text.
""".strip()
