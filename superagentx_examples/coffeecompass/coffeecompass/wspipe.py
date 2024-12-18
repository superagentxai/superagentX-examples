
import asyncio
import http
import urllib.parse

from rich import print as rprint
from superagentx.pipeimpl.wspipe import WSPipe  # https://websockets.readthedocs.io/en/stable/

from coffeecompass.config import AUTH_TOKEN
from coffeecompass.pipe import get_coffeecompass_pipe


async def query_param_auth(connection, request):
    """Authenticate user from token in query parameter."""
    query = urllib.parse.urlparse(request.path).query
    params = urllib.parse.parse_qs(query)
    values = params.get('token', [])
    if values:
        token = values[0]
        if token is None:
            return connection.respond(http.HTTPStatus.UNAUTHORIZED, "Missing token\n")
        if token != AUTH_TOKEN:
            return connection.respond(http.HTTPStatus.UNAUTHORIZED, "Invalid token\n")


async def main():
    """
    Launches the coffeecompass pipeline websocket server for processing requests and handling data.
    """
    pipe = await get_coffeecompass_pipe()
    ws_pipe = WSPipe(
        search_name='SuperAgentX coffeecompass Websocket Server',
        agentx_pipe=pipe,
        process_request=query_param_auth
    )
    await ws_pipe.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")
