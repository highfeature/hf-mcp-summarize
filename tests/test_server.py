import asyncio
import json
from typing import Any, Dict

from fastmcp.client import Client

from pydantic import BaseModel

from src.main import mcp
from src.summarizers.text_summarizer import TextSummarizer

# TODO: implement unit and functionnal tests
# async def test_resolve_library_id() -> None:
#     """Tests the resolve-library-id tool."""
#     library_name = "fastMCP"
#     response = await search_libraries(library_name)

#     print("\nTest: resolve-library-id")
#     print(f"Response: {json.dumps(response.model_dump(), indent=2)}")

# async def test_get_library_docs() -> None:
#     """Tests the get-library-docs tool."""
#     library_id = "/jlowin/fastMCP"
#     topic = "streamable-http"
#     tokens = 1000

#     try:
#         response = await fetch_library_documentation(
#             library_id,
#             tokens=tokens,
#             topic=topic
#         )
#         print("\nTest: get-library-docs")
#         print(f"Response type: {type(response)}")
#         if isinstance(response, str):
#             print(f"Response (truncated): {response[:200]}...")
#     except Exception as e:
#         print(f"\nError in test_get_library_docs: {str(e)}")

# async def main() -> None:
#     """Runs tests against the MCP server."""
#     # Test individual functions
#     await test_resolve_library_id()
#     await test_get_library_docs()

#     # Start a simple stdio server for manual testing
#     print("\nStarting MCP server on stdio...")
#     try:
#         await mcp.run_stdio_async()
#         print("MCP server running with stdio transport")
#         # Keep the server running
#         while True:
#             await asyncio.sleep(1)
#     except Exception as e:
#         print(f"Error starting server: {str(e)}")

# if __name__ == "__main__":
#     asyncio.run(main())