from langchain_mcp_adapters.client import MultiServerMCPClient
from config import COMPOSIO_EXTERNAL_USER_ID
from composio import Composio
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

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


class Tools:

    def __init__(self):
        self.tools = asyncio.run(fetch_tools())

    async def fetch_tools(self):
        tools = await mcp_client.get_tools()
        return tools
