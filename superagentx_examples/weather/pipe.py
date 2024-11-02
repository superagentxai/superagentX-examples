from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.engine import Engine
from superagentx.llm import LLMClient
from superagentx.prompt import PromptTemplate
from superagentx_handlers.weather import WeatherHandler

"""
  This SuperAgentX example gets real-time weather for the given place / city. To achieve this, we use two Agents.
  
  For OpenAI
  ----------  
  # llm_config = {'model': 'gpt-4o', 'llm_type': 'openai'}
    
  1. Agent 1 (`lat_and_long_agent`) : Get Latitude & Longitude for the given place / city 
  2. Agent 2 (`weather_agent_agent`) : Get real-time weather for the given city's latitude & longitude.
  
  SuperAgentX runs this example pipe to execute two agents in order sequence. Since, Agent 1's result (Lat & Long)
  should go to the next agent - Agent 2 as input to get real-time weather!
  
  `pipe = AgentXPipe(
        agents=[lat_and_long_agent, weather_agent_agent]  # Sequential Agents
    )`
  
"""


async def get_weather_pipe() -> AgentXPipe:

    # Gen AI model. Supports all major LLM models - OpenAI/ Azure OpenAI / Bedrock / Gemini /
    llm_config = {'model': 'anthropic.claude-3-5-sonnet-20241022-v2:0', 'llm_type': 'bedrock'}
    llm_client: LLMClient = LLMClient(llm_config=llm_config)

    # Set System Prompt to provide instructions for the LLM
    system_prompt = """You're provided with a tool that can get the coordinates for a specific city 
            'get_lat_long' and a tool that can get the weather for that city, but requires the coordinates 'get_weather'; 
            only use the tool if required. You can call the tool multiple times in the same response if required. Don't 
            make reference to the tools in your final answer. Generate ONLY the expected JSON"""

    weather_prompt = PromptTemplate(system_message=system_prompt)

    # Add Weather Handler as Tool and start the handler by the `engine`.
    weather_handler = WeatherHandler()
    weather_forecast_engine = Engine(
        handler=weather_handler,
        llm=llm_client,
        prompt_template=weather_prompt
    )

    # Agent - Get latitude & longitude from Weather Handler using engine.
    lat_and_long_agent = Agent(
        name="Latitude Longitude Agent",
        role="Weather Man",
        goal="Get the latitude and longitude for the given place",
        llm=llm_client,
        max_retry=2,  # Default Max Retry is 5
        prompt_template=weather_prompt,
        engines=[weather_forecast_engine],
    )

    # Agent - Get real-time weather for the given latitude & longitude from Weather Handler using engine.
    weather_agent_agent = Agent(
        name="Weather Man Agent",
        role="Weather Man",
        goal="Get the real-time weather based on the given latitude and longitude.",
        llm=llm_client,
        max_retry=2,  # Default Max Retry is 5
        prompt_template=weather_prompt,
        engines=[weather_forecast_engine],
    )

    # Pipe Interface to send it to public accessible interface (Cli Console / WebSocket / Restful API)
    pipe = AgentXPipe(
        agents=[lat_and_long_agent, weather_agent_agent]  # Sequential Agents
    )
    return pipe
