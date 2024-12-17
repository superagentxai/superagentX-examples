
import asyncio

from rich import print as rprint
from superagentx.pipeimpl.iopipe import IOPipe

from doctor_appointment.pipe import get_doctor_appointment_pipe


async def main():
    """
    Launches the doctor appointment pipeline console client for processing requests and handling data.
    """

    pipe = await get_doctor_appointment_pipe()

    # Create IO Cli Console - Interface
    io_pipe = IOPipe(
        search_name='SuperAgentX doctor appointment',
        agentx_pipe=pipe,
        read_prompt=f"\n[bold green]Enter your search here"
    )
    await io_pipe.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")
