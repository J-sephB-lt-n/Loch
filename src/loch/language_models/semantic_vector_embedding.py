import lancedb.embeddings


def create_semantic_vector_embedding_model(model_name: str):
    return (
        lancedb.embeddings.get_registry()
        .get("sentence-transformers")
        .create(
            name=model_name,
        )
    )
