import asyncio
import json

from rich import print as rprint
from rich.prompt import Prompt
from superagentx.utils.helper import sync_to_async
from websockets.asyncio.client import connect


async def trip_planner_pipe_cli():
    """
    Launches the trip planner pipeline websocket client for processing requests and handling data.
    """

    uri = "ws://localhost:8765"
    rprint(f'[bold blue]{10*"-"}Superagentx Trip Planner Websocket Cli{10*"-"}')

    async with connect(uri) as websocket:
        while True:
            query = await sync_to_async(Prompt.ask, '\n[bold green]Enter your search here')
            await websocket.send(json.dumps({'query': query}))
            res = await websocket.recv()
            rprint(f'{res}')


if __name__ == "__main__":
    asyncio.run(trip_planner_pipe_cli())
