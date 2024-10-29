from contextlib import asynccontextmanager

import uvicorn
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


app = FastAPI(lifespan=lifespan)


@app.get('/search')
async def search(query: str) -> list[GoalResult]:
    ecom_pipe: AgentXPipe = pipes.get('ecom_pipe')
    return await ecom_pipe.flow(query_instruction=query)


if __name__ == '__main__':
    uvicorn.run('app', port=8000)
