extract_semantic_triples_prompt: str = """
<document>
{{ document_contents }}
</document>

Extract all information from this document in the form of semantic triples (RDF triples).
Your output should be in basic English - easily understood by someone whose first language \
is not English.
Make subject, predicate and object as short as possible.
Do not include stopwords.
Your output must contain a JSON markdown code block.

<non-negotiable-output-format>
```json
[
    ["subject 1", "predicate 1", "object 1"],
    ["subject 2", "predicate 2", "object 2"],
    ...
]
```
</non-negotiable-output-format>
""".strip()
