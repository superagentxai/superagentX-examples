from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.engine import Engine
from superagentx.handler import SerperDevToolHandler, AIHandler
from superagentx.llm import LLMClient
from superagentx.memory import Memory
from superagentx.prompt import PromptTemplate
from superagentx_handlers import ScrapeHandler

output_prompt = """
Change the output format from the context. Give me list of link

Desired Format: 
    [put here website links],
Don't include any other information.
"""


async def get_trip_planner_pipe():
    llm_config = {
        'model': 'anthropic.claude-3-5-haiku-20241022-v1:0',
        'llm_type': 'bedrock'
    }
    llm_client: LLMClient = LLMClient(llm_config=llm_config)

    prompt_template = PromptTemplate()

    memory = Memory(
        memory_config={"llm_client": llm_client}
    )

    serper_handler = SerperDevToolHandler()
    scrape_handler = ScrapeHandler()

    city_ai_handler = AIHandler(
        llm=llm_client,
        role="City Selection Expert",
        story_content="An expert in analyzing travel data to pick ideal destinations"
    )
    travel_concierge_handler = AIHandler(
        llm=llm_client,
        role="Amazing Travel Concierge",
        story_content="Specialist in travel planning and logistics with decades of experience"
    )

    serper_engine = Engine(
        handler=serper_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )
    scraper_engine = Engine(
        handler=scrape_handler,
        llm=llm_client,
        prompt_template=prompt_template,
    )
    city_ai_engine = Engine(
        handler=city_ai_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )
    travel_concierge_engine = Engine(
        handler=travel_concierge_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )

    serper_agent = Agent(
        name="Serper Agent",
        role=f'You are the website link extractor and generate the following format.\n\n'
             f'Format:\n{output_prompt}',
        goal='Generate the list of website urls',
        llm=llm_client,
        prompt_template=prompt_template,
        engines=[serper_engine],
        output_format=output_prompt
    )
    scraper_agent = Agent(
        name="Crawler Agent",
        role=f'You are the travel data extractor. Extract the city, locations, hotels, weather, seasons, months and '
             f'prices with full information based on the user question and context. And generate the below output '
             f'format \n\n{output_prompt}',
        goal='Extract the city, locations, hotels, weather, seasons, months and prices',
        llm=llm_client,
        prompt_template=prompt_template,
        engines=[scraper_engine]
    )
    city_selection_agent = Agent(
        name="City Selection Agent",
        role='City Selection Expert',
        goal='Select the best city based on weather, locations, hotels season, months, itineraries and prices',
        llm=llm_client,
        prompt_template=prompt_template,
        engines=[city_ai_engine]
    )
    travel_concierge_agent = Agent(
        name="Trip Planner Agent",
        role='Amazing Trip planner',
        goal='Create the most amazing travel with budget and packing suggestions for the city',
        llm=llm_client,
        prompt_template=prompt_template,
        engines=[travel_concierge_engine]
    )

    pipe = AgentXPipe(
        name="Trip Planner Pipe",
        agents=[
            serper_agent,
            scraper_agent,
            city_selection_agent,
            travel_concierge_agent
        ],
        memory=memory
    )

    return pipe
