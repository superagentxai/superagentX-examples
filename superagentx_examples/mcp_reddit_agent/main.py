import asyncio

from superagentx.agent import Agent
from superagentx.engine import Engine
from superagentx.handler.mcp import MCPHandler
from superagentx.llm import LLMClient
from superagentx.prompt import PromptTemplate


async def main():
    print("Welcome to SuperAgentX MCP Tutorial")

    # Step 1: Initialize LLM
    # Note: You need to setup your OpenAI API key before running this step.
    # export OPENAI_API_KEY=<your-api-key>
    llm_config = {"model": "gpt-4o", "llm_type": "openai"}
    llm_client = LLMClient(llm_config=llm_config)

    # Step 2: Setup MCP tool handler (Reddit trending analyzer) 
    # Note: You need to install the mcp-server-reddit package before running this step.
    # pip install mcp-server-reddit
    mcp_handler = MCPHandler(command="python", mcp_args=["-m", "mcp_server_reddit"])

    # Step 3: Create Prompt Template
    prompt_template = PromptTemplate()

    # Step 4: Create Engine for Reddit analysis using MCP
    reddit_engine = Engine(handler=mcp_handler, llm=llm_client,
                           prompt_template=prompt_template)

    # Step 5: Define Reddit Agent
    agent = Agent(goal="Summarize Reddit Messages",
                  role="You're Reddit Trend Analyzer",
                  llm=llm_client, prompt_template=prompt_template,
                  engines=[reddit_engine])

    result = await agent.execute(query_instruction="List top AI Trends")

    print(f"Reddit Agent Result : {result}")


if __name__ == "__main__":
    asyncio.run(main())


