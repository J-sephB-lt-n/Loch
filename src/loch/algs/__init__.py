"""
docstring TODO

NOTE: Should be using the registry pattern for this
"""

from loch import constants
from loch.data_models.query_algorithm import QueryAlgorithm

from .entire_doc_vector_search import EntireDocumentVectorSearch
from .llm_auto_tagging import LlmAutoTagging
from .llm_knowledge_graph import LlmKnowledgeGraph
from .llm_question_answering import LlmQuestionAnswering
from .pyramid_search import PyramidSearch
from .semantic_code_search import SemanticCodeSearch

ALGS: dict[str, QueryAlgorithm] = {
    "entire_doc_vector_search": EntireDocumentVectorSearch(),
    "llm_auto_tagging": LlmAutoTagging(),
    "llm_knowledge_graph": LlmKnowledgeGraph(),
    "llm_question_answering": LlmQuestionAnswering(),
    "pyramid_search": PyramidSearch(),
    # "semantic_code_search": SemanticCodeSearch(),
}

assert all((alg_name in ALGS for alg_name in constants.ALG_NAMES.keys))
