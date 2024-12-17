from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.engine import Engine
from superagentx.llm import LLMClient
from superagentx.memory import Memory
from superagentx.prompt import PromptTemplate
from superagentx_handlers import BestbuyHandler


# Import handlers

# Example
# -------
#################################################
# Uncomment below lines to enable ecom handlers #
#################################################
# from superagentx_handlers import AmazonHandler
# from superagentx_handlers.ecommerce.walmart import WalmartHandler


async def get_best_buy_deals_pipe() -> AgentXPipe:
    # LLM Configuration
    llm_config = {
        'model': 'anthropic.claude-3-5-haiku-20241022-v1:0',
        'llm_type': 'bedrock'
    }
    llm_client = LLMClient(llm_config=llm_config)

    # Enable Memory
    memory = Memory(memory_config={"llm_client": llm_client})

    # Example
    # -------
    # amazon_ecom_handler = AmazonHandler()
    # walmart_ecom_handler = WalmartHandler()

    best_buy_handler = BestbuyHandler(api_key="dmx8sagAYsaH0ghrgAA7OhkR")

    agent_prompt = """You are an AI assistant tasked with analyzing a list of products. Your goal is to determine the best product from the given list based on the following criteria, in priority order:

    Highest Sale Price: Prefer products with the highest saleprice.
    Most Significant Discount: If multiple products have the same saleprice, choose the one with the largest difference between oldprice and saleprice.
    Reputation: If there is still a tie, prioritize products with available reviews (non-None values).
    First in List: If all else is equal, pick the first product in the list.
    
    Input:
    A list of dictionaries, where each dictionary contains:
    
    title (str): The name of the product.
    link (str): The URL to the product page.
    saleprice (float): The current sale price of the product.
    oldprice (float): The original price of the product.
    reviews (str or None): The number or text description of reviews, if available.
    
    Output:
    Provide a concise json summary of the best product, including its title, link, saleprice, and oldprice.
    
    """

    agent_prompt_template = PromptTemplate(system_message=agent_prompt)


    system_prompt = """Generate a concise tweet to promote a product deal. The tweet should include:
        1.Product name and highlight a key feature.
        2.The price and any discount.
        3.A short call to action (e.g., 'Grab it now!').
        4.Provide a URL or link or tiny link for the product deal..
        5.Make sure add link in tweet_text 
        6.Add some popular hashtags for Black Friday and Cyber Monday include:
            #blackfriday, #blackfridaysale, and #cybermonday.    
        Make sure it stays within the 240-character Twitter limit and is engaging!"""
    # Prompt Template
    tweet_prompt_template = PromptTemplate(system_message=system_prompt)

    # Example - Engine(s)
    # -------------------
    # amazon_engine = Engine(
    #     handler=amazon_ecom_handler,
    #     llm=llm_client,
    #     prompt_template=prompt_template
    # )
    # walmart_engine = Engine(
    #     handler=walmart_ecom_handler,
    #     llm=llm_client,
    #     prompt_template=prompt_template
    # )

    best_buy_engin = Engine(
        handler=best_buy_handler,
        llm=llm_client,
        prompt_template=PromptTemplate()
    )

    # Create Agents

    # Example - Agent(s)
    # ------------------
    # Create Agent with Amazon, Walmart Engines execute in Parallel - Search Products from user prompts
    # ecom_agent = Agent(
    #     name='Ecom Agent',
    #     goal="Get me the best search results",
    #     role="You are the best product searcher",
    #     llm=llm_client,
    #     prompt_template=prompt_template,
    #     engines=[[amazon_engine, walmart_engine]]
    # )

    best_agent = Agent(
        name='Best buy Agent',
        goal="Get me the best search results",
        role="You are the best product searcher",
        llm=llm_client,
        prompt_template=agent_prompt_template,
        engines=[best_buy_engin]
    )

    # Create Pipe - Interface

    # Pipe Interface to send it to public accessible interface (Cli Console / WebSocket / Restful API)
    pipe = AgentXPipe(
        ###############################################
        # Uncomment below lines to enable ecom agents #
        ###############################################
        agents=[best_agent]
    )
    return pipe
