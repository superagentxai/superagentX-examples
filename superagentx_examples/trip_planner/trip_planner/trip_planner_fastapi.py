from contextlib import asynccontextmanager

from fastapi import FastAPI
from superagentx.agentxpipe import AgentXPipe
from superagentx.result import GoalResult

from superagentx_examples.trip_planner.pipe import get_trip_planner_pipe

pipes = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    pipes['trip_planner_pipe'] = await get_trip_planner_pipe()
    yield
    pipes.clear()


ecom_app = FastAPI(
    title='Trip Planner',
    lifespan=lifespan
)


@ecom_app.get('/search')
async def search(query: str) -> list[GoalResult]:
    trip_planner_pipe: AgentXPipe = pipes.get('trip_planner_pipe')
    return await trip_planner_pipe.flow(query_instruction=query)


"""
# To Run This using, install `pip install 'fastapi[standard]'`

# Development Mode
fastapi dev superagentx_examples/trip_planner/trip_planner_fastapi.py

# Server Mode
fastapi run superagentx_examples/trip_planner/trip_planner_fastapi.py
"""
