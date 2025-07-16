from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastmcp import FastMCP
from pydantic import BaseModel
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from src.summarizers.text_summarizer import TextSummarizer

# Initialize Sentry =========================================
sentry_sdk.init(
    dsn="http://a87a15429de8e0c6e17217403ece2c13@0.0.0.0:18990/2",
    # Add request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
)

# Initialize FastMCP =========================================
mcp = FastMCP("HighfeatureMcpServerSummarize")

# Define tool for FastMCP

# add --------------------------------------------------------
@mcp.tool()
def add(a: int, b: int) -> int:
    """ This simple tools make very difficult addition a + b, and cheat by adding 10 to the sum. """
    return a + b + 10

# summarizers ------------------------------------------------
summarizers = {
    'TEXT':TextSummarizer()
}

class TextRequest(BaseModel):
    text: str

@mcp.tool()
def summarize_text(data: TextRequest):
    """ This tool summarize a text passed in parameter, the parameter is a dict like: 
    {'text':'Your text here. It is recommended to be within the context size of the LLM.'}"""
    try:
        result = summarizers['TEXT'].summarize(data.text)
        if 'content' in result:
            return {"status": "success", "summary":result['content']}
        else:
            raise HTTPException(status_code=500, detail=str(result['error']))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount the MCP app as a sub-application
mcp_app = mcp.http_app()




# Initialize FastAPI =========================================

# from: https://gofastmcp.com/deployment/asgi#fastapi-integration
# For Streamable HTTP transport, you must pass the lifespan context from the 
# FastMCP app to the resulting FastAPI app, as nested lifespans are not recognized. 
# Otherwise, the FastMCP server’s session manager will not be properly initialized.

# Create a FastAPI app and mount the MCP server
app = FastAPI(
    title="hf-mcp-summarize",
    version="1.0.0",
    description="Leverages an LLM to summarize data",  
    lifespan=mcp_app.router.lifespan_context,
    openapi_url="/mcp-server/openapi.json",
)

# add sentry middleware
app.add_middleware(SentryAsgiMiddleware)

# Mount the FastMCP app to the FastAPI app
app.mount("/mcp-server", mcp_app, "mcp")

# Add response on OPTIONS for openapi_url, workaround for support openwebui
@app.options("/mcp-server/openapi.json")
async def options_openapi(request: Request):
    # Customize the response for the OPTIONS method
    response = {
        "method": "OPTIONS",
        "allowed_methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        "description": "Custom OPTIONS response for /openapi.json"
    }
    return JSONResponse(content=response)

# Define FastAPI routes ----------------------------------------
@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint showing service information."""
    return {
        "service": "Highfeature Sumarize MCP Service",
        "version": "1.0.0",
        "status": "running",
    }

@app.get("/health-check")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

# import asyncio
# # from server import run, server

# async def main():
#     app.run()
#     # asyncio.run(app,run())

# if __name__ == "__main__":
#     # asyncio.run(main())
#     app.run()
