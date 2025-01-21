import asyncio

from rich import print as rprint

from pipe import get_whisper_pipe
from superagentx.pipeimpl.openaivoicepipe import WhisperPipe


async def main():
    """
    Launches the voice_to_text pipeline console client for processing requests and handling data.
    """

    pipe = await get_whisper_pipe()

    # Create IO Cli Console - Interface
    io_pipe = WhisperPipe(
        search_name='SuperAgentX voice_to_text',
        agentx_pipe=pipe,
        read_prompt=f"\n[bold green]Enter your search here"
    )
    await io_pipe.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")
