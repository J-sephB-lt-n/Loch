extract_semantic_triples: str = """
<document>
{{ document_contents }}
</document>

Extract all information from this document in the form of semantic triples (RDF triples).
Your output should be easily understood by someone for whom English is their second language.
Make subject, predicate and object as short as possible.

<non-negotiable-output-format>
```json
[
    ["<subject 1>", "<predicate 1>", "<object 1>"],
    ["<subject 2>", "<predicate 2>", "<object 2>"],
    ...
]
```
</non-negotiable-output-format>
""".strip()
