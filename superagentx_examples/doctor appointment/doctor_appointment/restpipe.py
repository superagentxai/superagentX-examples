
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException  # https://fastapi.tiangolo.com/
from fastapi.security import APIKeyHeader
from superagentx.agentxpipe import AgentXPipe
from superagentx.result import GoalResult

from doctor_appointment.config import AUTH_TOKEN
from doctor_appointment.pipe import get_doctor_appointment_pipe

pipes = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    pipes['doctor_appointment_pipe'] = await get_doctor_appointment_pipe()
    yield
    pipes.clear()


ecom_app = FastAPI(
    title='doctor appointment Search',
    lifespan=lifespan
)


async def verify_api_token(
    api_token: str = Depends(APIKeyHeader(name='api-token', auto_error=False))
):
    if api_token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail='Invalid API Token!')


@ecom_app.get('/search', dependencies=[Depends(verify_api_token)])
async def search(query: str) -> list[GoalResult]:
    doctor_appointment_pipe: AgentXPipe = pipes.get('doctor_appointment_pipe')
    return await doctor_appointment_pipe.flow(query_instruction=query)


"""
# To Run this, please install `pip install 'fastapi[standard]'`

# Development Mode
fastapi dev superagentx_examples/ecom/ecom_fastapi.py

# Server Mode
fastapi run superagentx_examples/ecom/ecom_fastapi.py
"""
