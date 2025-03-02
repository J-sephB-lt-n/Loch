# import datetime
#
# print(datetime.datetime.now().strftime("%H:%M:%S"))

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer(
    "mixedbread-ai/mxbai-embed-large-v1",
    # truncate_dim=512
)

# docs_embeddings = model.encode(
#     [
#         "The man is unhappy",
#         "The goat is happy",
#         "The kid is happy",
#         "The woman is sad",
#     ]
# )
#
# query_embedding = model.encode(
#     "Represent this sentence for searching relevant passages: " +
#     "I am happy",
# )
#
# similarities = cos_sim(query_embedding, docs_embeddings)
# print('similarities:', similarities)
#
# print(datetime.datetime.now().strftime("%H:%M:%S"))
