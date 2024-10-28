import asyncio
import os

from rich import print as rprint
from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.engine import Engine
from superagentx.llm import LLMClient
from superagentx.pipeimpl.wspipe import WSPipe
from superagentx.prompt import PromptTemplate
from superagentx_handlers.ecommerce.amazon import AmazonHandler
from superagentx_handlers.ecommerce.flipkart import FlipkartHandler


async def main():
    """
    Launches the e-commerce pipeline websocket server for processing requests and handling data.
    """
    llm_config = {'model': 'gpt-4-turbo-2024-04-09', 'llm_type': 'openai'}

    llm_client: LLMClient = LLMClient(llm_config=llm_config)
    amazon_ecom_handler = AmazonHandler(
        api_key=os.getenv('RAPID_API_KEY'),
        country="IN"
    )
    flipkart_ecom_handler = FlipkartHandler(
        api_key=os.getenv('RAPID_API_KEY'),
    )
    prompt_template = PromptTemplate()
    amazon_engine = Engine(
        handler=amazon_ecom_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )
    flipkart_engine = Engine(
        handler=flipkart_ecom_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )
    ecom_agent = Agent(
        name='Ecom Agent',
        goal="Get me the best search results",
        role="You are the best product searcher",
        llm=llm_client,
        prompt_template=prompt_template,
        engines=[[amazon_engine, flipkart_engine]]
    )
    pipe = AgentXPipe(
        agents=[ecom_agent]
    )
    ws_pipe = WSPipe(
        search_name='SuperAgentX Ecom Websocket Server',
        agentx_pipe=pipe
    )
    await ws_pipe.start()


if __name__ =='__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")
