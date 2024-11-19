import asyncio

from rich import print as rprint
from superagentx.pipeimpl.wspipe import WSPipe

from superagentx_examples.trip_planner.pipe import get_trip_planner_pipe


async def main():
    """
    Launches the trip planner pipeline websocket server for processing requests and handling data.
    """
    pipe = await get_trip_planner_pipe()
    ws_pipe = WSPipe(
        search_name='SuperAgentX Trip Planner Websocket Server',
        agentx_pipe=pipe
    )
    await ws_pipe.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")
