
import asyncio
import http
import urllib.parse

from rich import print as rprint
from superagentx.pipeimpl.wspipe import WSPipe  # https://websockets.readthedocs.io/en/stable/

from trip_planner.config import AUTH_TOKEN
from trip_planner.pipe import get_trip_planner_pipe


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
    Launches the trip_planner pipeline websocket server for processing requests and handling data.
    """
    pipe = await get_trip_planner_pipe()
    ws_pipe = WSPipe(
        search_name='SuperAgentX trip_planner Websocket Server',
        agentx_pipe=pipe,
        process_request=query_param_auth
    )
    await ws_pipe.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")
