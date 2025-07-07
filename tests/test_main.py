import json
import pytest
from collections.abc import Callable, Generator

# from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.client import Client
from fastapi.testclient import TestClient
from fastmcp.utilities.tests import run_server_in_process

from src.main import app, mcp


# for fastAPI tests
tclient = TestClient(app)

# for fastMCP tests
@pytest.fixture
def mcp_server():
    app.run(transport="streamable-http", host="127.0.0.1", port=19050) #, path="/mcp-server/mcp/")


# fastAPI tests
@pytest.mark.asyncio
async def test_fastapi_root():
    response = tclient.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "service": "Highfeature Sumarize MCP Service",
        "version": "1.0.0",
        "status": "running",
    }


@pytest.mark.asyncio
async def test_fastapi_health():
    response = tclient.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {'status': 'healthy'}


# fastAPI tests
@pytest.mark.asyncio
async def test_fastapi_openapi_json_get():
    response = tclient.get("/mcp-server/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert "openapi" in response.json()


# fastMCP tests
@pytest.mark.asyncio
async def test_mcp_tool_add():
    async with Client(mcp) as client:
        response = await client.call_tool_mcp("add", {"a": "1", "b": "2"})
        assert response.content[0].text == "13"

