from langchain_ollama import ChatOllama
from composio import Composio
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
load_dotenv()
import os



llm = ChatOllama(model="llama3.2:latest")
external_user_id = "pg-test-baad7476-63b1-43c8-8980-3cf47519cdf3"


composio = Composio(api_key=os.environ["COMPOSIO"])

session = composio.create(user_id=external_user_id)

async def main():
    mcp_cleint = MultiServerMCPClient(
        {
            "composio":{
                "transport":"streamable_http",
                "url": session.mcp.url,
                "headers": session.mcp.headers
            }
        }
    )

    tools = await mcp_cleint.get_tools()

    agent = create_agent(
        tools = tools,
        model = llm
    )

    result =await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "search for brommstick in amazon"
                }
            ]
        }
    )

    print(result['messages'][-1].content)


import asyncio
asyncio.run(main())
