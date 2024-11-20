
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException  # https://fastapi.tiangolo.com/
from fastapi.security import APIKeyHeader
from superagentx.agentxpipe import AgentXPipe
from superagentx.result import GoalResult

from coffeecompass.config import AUTH_TOKEN
from coffeecompass.pipe import get_coffeecompass_pipe

pipes = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    pipes['coffeecompass_pipe'] = await get_coffeecompass_pipe()
    yield
    pipes.clear()


ecom_app = FastAPI(
    title='coffeecompass Search',
    lifespan=lifespan
)


async def verify_api_token(
    api_token: str = Depends(APIKeyHeader(name='api-token', auto_error=False))
):
    if api_token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail='Invalid API Token!')


@ecom_app.get('/search', dependencies=[Depends(verify_api_token)])
async def search(query: str) -> list[GoalResult]:
    coffeecompass_pipe: AgentXPipe = pipes.get('coffeecompass_pipe')
    return await coffeecompass_pipe.flow(query_instruction=query)


"""
# To Run this, please install `pip install 'fastapi[standard]'`

# Development Mode
fastapi dev superagentx_examples/ecom/ecom_fastapi.py

# Server Mode
fastapi run superagentx_examples/ecom/ecom_fastapi.py
"""
