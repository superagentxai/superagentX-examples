import asyncio

from rich import print as rprint
from superagentx.pipeimpl.iopipe import IOPipe

from superagentx_examples.weather.pipe import get_weather_pipe


async def main():
    """
    Launches the weather pipeline console client for processing requests and handling inputs.
    """

    pipe = await get_weather_pipe()

    # Create IO Cli Console - Interface
    io_pipe = IOPipe(
        search_name='SuperAgentX Weather Man',
        agentx_pipe=pipe,
        read_prompt=f"\n[bold green]Enter your search here"
    )
    await io_pipe.start()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")
