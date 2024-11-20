
from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.engine import Engine
from superagentx.llm import LLMClient
from superagentx.memory import Memory
from superagentx.prompt import PromptTemplate

# Import handlers
from coffeecompass.handler.coffeecompass_handler import CoffeeCompassHandler


async def get_coffeecompass_pipe() -> AgentXPipe:
    # LLM Configuration
    llm_config = { "model":'anthropic.claude-3-5-haiku-20241022-v1:0', "llm_type":'bedrock'}

    llm_client = LLMClient(llm_config=llm_config)

    # Enable Memory
    memory = Memory(memory_config={"llm_client": llm_client})

    coffee_compass_handler = CoffeeCompassHandler()

    # Set System Prompt to provide instructions for the LLM
    system_prompt = """
    You're provided with a tool that can get the coordinates for a specific city 'get_lat_long' and a tool that can
     get best cafe in that city, but requires the coordinates 'find_coffee_shops'; only use the tool if required. 
    You can call the tool multiple times in the same response. Don't make reference to the tools in your final answer.
    Generate ONLY the expected JSON
    """


    # Prompt Template
    coffee_shop_system_prompt= PromptTemplate(system_message=system_prompt)

    coffee_compass_engine = Engine(
        handler=coffee_compass_handler,
        llm=llm_client,
        prompt_template=coffee_shop_system_prompt
    )

    # Agent - Get latitude & longitude from Coffee Compass Handler using engine.
    lat_and_long_agent = Agent(
        name="Latitude Longitude Agent",
        role="You're a map expert to find latitude & longitude for the given place",
        goal="Get the latitude and longitude for the given place",
        llm=llm_client,
        max_retry=2,  # Default Max Retry is 5
        prompt_template=coffee_shop_system_prompt,
        engines=[coffee_compass_engine],
    )

    # Agent - To find Coffee shops nearby with an input of latitude & longitude.
    coffee_compass_agent = Agent(
        name='Cafe Finder Agent',
        goal="Find the good cafes with features list",
        role="You are the best cafe shop finder",
        llm=llm_client,
        prompt_template=coffee_shop_system_prompt,
        engines=[coffee_compass_engine]
    )


    # Create Pipe - Interface

    # Pipe Interface to send it to publicly accessible interface (Cli Console / WebSocket / Restful API)
    pipe = AgentXPipe(
        agents=[lat_and_long_agent, coffee_compass_agent],
        memory=memory
    )
    return pipe
