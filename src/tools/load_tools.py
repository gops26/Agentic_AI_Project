from langchain_mcp_adapters.client import MultiServerMCPClient
from composio import Composio
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

COMPOSIO_EXTERNAL_USER_ID = "pg-test-baad7476-63b1-43c8-8980-3cf47519cdf3"


composio = Composio(api_key=os.environ["COMPOSIO"])

session = composio.create(user_id=COMPOSIO_EXTERNAL_USER_ID)


mcp_client = MultiServerMCPClient(
    connections={
        "composio": {
            "transport":"streamable_http",
            "url": session.mcp.url,
            "headers":session.mcp.headers
        }
    }
)

async def fetch_tools():
    tools = await mcp_client.get_tools()
    return tools 


def load_tools():
    tools = asyncio.run(fetch_tools())
    return tools
