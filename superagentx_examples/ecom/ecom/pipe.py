from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.engine import Engine
from superagentx.llm import LLMClient
from superagentx.memory import Memory
from superagentx.prompt import PromptTemplate
from superagentx_handlers import AmazonHandler
from superagentx_handlers.ecommerce.walmart import WalmartHandler


async def get_ecom_pipe() -> AgentXPipe:
    # LLM Configuration
    llm_config = {
        'llm_type': 'openai'
    }
    llm_client = LLMClient(llm_config=llm_config)

    # Enable Memory
    memory = Memory(memory_config={"llm_client": llm_client})

    # Add Two Handlers (Tools) - Amazon, Walmart
    amazon_ecom_handler = AmazonHandler()
    walmart_ecom_handler = WalmartHandler()

    # Prompt Template
    prompt_template = PromptTemplate()

    # Amazon & Walmart Engine to execute handlers
    amazon_engine = Engine(
        handler=amazon_ecom_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )
    walmart_engine = Engine(
        handler=walmart_ecom_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )

    # Create Agent with Amazon, Walmart Engines execute in Parallel - Search Products from user prompts
    ecom_agent = Agent(
        name='Ecom Agent',
        goal="Get me the best search results",
        role="You are the best product searcher",
        llm=llm_client,
        prompt_template=prompt_template,
        engines=[[amazon_engine, walmart_engine]]
    )

    # Pipe Interface to send it to public accessible interface (Cli Console / WebSocket / Restful API)
    pipe = AgentXPipe(
        agents=[ecom_agent],
        memory=memory
    )
    return pipe
