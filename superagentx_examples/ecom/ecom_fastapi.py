from contextlib import asynccontextmanager

from fastapi import FastAPI
from superagentx.agentxpipe import AgentXPipe
from superagentx.result import GoalResult

from superagentx_examples.ecom.pipe import get_ecom_pipe

pipes = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    pipes['ecom_pipe'] = await get_ecom_pipe()
    yield
    pipes.clear()


ecom_app = FastAPI(
    title='Ecom Search',
    lifespan=lifespan
)


@ecom_app.get('/search')
async def search(query: str) -> list[GoalResult]:
    ecom_pipe: AgentXPipe = pipes.get('ecom_pipe')
    return await ecom_pipe.flow(query_instruction=query)


"""
# To Run This using, install `pip install 'fastapi[standard]'`

# Development Mode
fastapi dev superagentx_examples/ecom/ecom_fastapi.py

# Server Mode
fastapi run superagentx_examples/ecom/ecom_fastapi.py
"""
