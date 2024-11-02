from contextlib import asynccontextmanager

from fastapi import FastAPI
from superagentx.agentxpipe import AgentXPipe
from superagentx.result import GoalResult

from superagentx_examples.weather.pipe import get_weather_pipe

pipes = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    pipes['weatherman_pipe'] = await get_weather_pipe()
    yield
    pipes.clear()


ecom_app = FastAPI(
    title='Weatherman Teller',
    lifespan=lifespan
)


@ecom_app.get('/search')
async def search(query: str) -> list[GoalResult]:
    ecom_pipe: AgentXPipe = pipes.get('weatherman_pipe')
    return await ecom_pipe.flow(query_instruction=query)


"""
# To Run This using, install `pip install 'fastapi[standard]'`

# Development Mode
fastapi dev superagentx_examples/weather/weather_fastapi.py

# Server Mode
fastapi run superagentx_examples/weather/weather_fastapi.py
"""
