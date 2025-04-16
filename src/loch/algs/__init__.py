"""
docstring TODO                                      
"""

from loch import constants
from loch.data_models.query_algorithm import QueryAlgorithm

from .fts_bm25 import FtsBm25
from .llm_auto_tagging import LlmAutoTagging
from .llm_knowledge_graph import LlmKnowledgeGraph
from .llm_question_answering import LlmQuestionAnswering
from .pyramid_search import PyramidSearch
from .semantic_search import SemanticSearch

ALGS: dict[str, QueryAlgorithm] = {
    "fts_bm25": FtsBm25(),
    "llm_auto_tagging": LlmAutoTagging(),
    "llm_knowledge_graph": LlmKnowledgeGraph(),
    "llm_question_answering": LlmQuestionAnswering(),
    "pyramid_search": PyramidSearch(),
    "semantic_search": SemanticSearch(),
}

assert all((alg_name in ALGS for alg_name in constants.ALG_NAMES.keys))
