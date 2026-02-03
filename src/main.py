from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastmcp import FastMCP
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
import os
from pydantic import BaseModel
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sqlalchemy import create_engine, String, Column
from sqlalchemy.orm import declarative_base, sessionmaker
from src.summarizers.text_summarizer import TextSummarizer

load_dotenv()

# Initialize OpenTelemetry ==================================
provider = TracerProvider()
## set global default tracer provider
trace.set_tracer_provider(provider)
## creates a tracer from the global tracer provider
tracer = trace.get_tracer("hf.mcp.summarize.tracer")

# Initialize Database =======================================
# engine = create_engine('my.db')
PG_URL = os.getenv("PG_URL", default="127.0.0")
PG_PORT = os.getenv("PG_PORT", default="5432")
PG_DB = os.getenv("PG_DB", default="postgres")
PG_USER = os.getenv("PG_USER", default="")
PG_PWD = os.getenv("PG_PWD", default="")
url = f"postgresql://{PG_USER}:{PG_PWD}@/{PG_DB}?host={PG_URL}&port={PG_PORT}"
engine = create_engine(url)
factory = sessionmaker(bind=engine)

# Create dummy models =======================================
base = declarative_base()
class Orders(base):
    __tablename__ = "Orders"
    ShipName = Column(String,primary_key=True)
    ShipCity = Column(String)

# Initialize Sentry =========================================
sentry_sdk.init(
    dsn=os.getenv("SENTRY_URL", "http://a87a15429de8e0c6e17217403ece2c13@0.0.0.0:18990/2"),
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
# Otherwise, the FastMCP server's session manager will not be properly initialized.

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
async def trigger_error_sentry():
    division_by_zero = 1 / 0

@app.get("/jeager-intrumentation")
async def trigger_error_opentelemetry():
    with tracer.start_as_current_span('Here a nice divide by zero') as span:
        division_by_zero = 1 / 0

@app.get("/list-orders-intrumentated")
async def list_orders():
    session = factory()
    data = []
    for instance in session.query(Orders).filter_by(ShipCountry="UK"):
        with tracer.start_as_current_span('list_Orders') as span:
            data.append(
                {
                    "ShipName: ": instance.ShipName,
                    "ShipCity: ": instance.ShipCity
                }
            )
    return data
