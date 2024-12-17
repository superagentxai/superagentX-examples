
import asyncio

from rich import print as rprint
from superagentx.pipeimpl.iopipe import IOPipe

from best_buy_deals.pipe import get_best_buy_deals_pipe


async def main():
    """
    Launches the best buy deals pipeline console client for processing requests and handling data.
    """

    pipe = await get_best_buy_deals_pipe()

    # Create IO Cli Console - Interface
    io_pipe = IOPipe(
        search_name='SuperAgentX best buy deals',
        agentx_pipe=pipe,
        read_prompt=f"\n[bold green]Enter your search here"
    )
    await io_pipe.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")
