import pytest
from src.summarizers.text_summarizer import TextSummarizer

# TODO: implement unit and functionnal tests

# @pytest.fixture
# def sample_search_result():
#     return SearchResult(
#         id="/facebook/react",
#         title="React",
#         description="A JavaScript library for building user interfaces.",
#         branch="main",
#         lastUpdateDate="2023-01-01",
#         state=DocumentState.FINALIZED,
#         totalTokens=1000,
#         totalSnippets=50,
#         totalPages=10,
#         stars=100000,
#         trustScore=9.8,
#         versions=["17.0.2", "18.0.0"]
#     )

# @pytest.fixture
# def sample_search_response():
#     return SearchResponse(
#         results=[
#             SearchResult(
#                 id="/facebook/react",
#                 title="React",
#                 description="A JavaScript library for building user interfaces.",
#                 branch="main",
#                 lastUpdateDate="2023-01-01",
#                 state=DocumentState.FINALIZED,
#                 totalTokens=1000,
#                 totalSnippets=50,
#                 totalPages=10,
#                 stars=100000,
#                 trustScore=9.8,
#                 versions=["17.0.2", "18.0.0"]
#             ),
#             SearchResult(
#                 id="/pytorch/pytorch",
#                 title="PyTorch",
#                 description="An open source machine learning framework.",
#                 branch="main",
#                 lastUpdateDate="2023-02-01",
#                 state=DocumentState.FINALIZED,
#                 totalTokens=2000,
#                 totalSnippets=100,
#                 totalPages=20,
#                 stars=80000,
#                 trustScore=9.5,
#                 versions=["2.0.0", "2.1.0"]
#             )
#         ]
#     )

# def test_format_search_result(sample_search_result):
#     formatted = format_search_result(sample_search_result)
#     assert "- Title: React" in formatted
#     assert "- hf-context7-compatible library ID: /facebook/react" in formatted
#     assert "- Description: A JavaScript library for building user interfaces." in formatted
#     assert "- Code Snippets: 50" in formatted
#     assert "- Trust Score: 9.8" in formatted
#     assert "- Versions: 17.0.2, 18.0.0" in formatted

# def test_format_search_results(sample_search_response):
#     formatted = format_search_results(sample_search_response)
#     assert "React" in formatted
#     assert "PyTorch" in formatted
#     assert "hf-context7-compatible library ID: /facebook/react" in formatted
#     assert "hf-context7-compatible library ID: /pytorch/pytorch" in formatted

# def test_format_empty_search_results():
#     empty_response = SearchResponse(results=[])
#     formatted = format_search_results(empty_response)
#     assert formatted == "No documentation libraries found matching your query."