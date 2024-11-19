<div align="center">

<img src="https://github.com/superagentxai/superagentX/blob/master/docs/images/fulllogo_transparent.png?raw=True" width="350">


<br/>

**Superagentx Examples**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![GitHub Repo stars](https://img.shields.io/github/stars/superagentxai/superagentX-examples)](https://github.com/superagentxai/superagentX-examples)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/superagentxai/superagentX-examples/blob/master/LICENSE)
</div>

### OVERVIEW :
The SuperagentX-Examples repository provides streamlines interactions with major online platforms. It uses Large Language Models (LLMs) to create agents that can search, retrieve , and also interact with e-commerce platforms like Amazon and Walmart.
# Environment Setup
```shell
$ git clone https://github.com/superagentxai/superagentx.git
$ cd <path-to>/superagentX-examples
$ python3.12 -m venv venv
$ source venv/bin/activate
(venv) $ pip install poetry
(venv) $ poetry install
```


### Getting Started


##### Usage - Example SuperAgentX Code
This SuperAgentX-ecom-example utilizes two handlers, Amazon and Walmart, to search for product items based on user input from the IO Console.

1. It uses Parallel execution of handler in the agent 
2. Memory Context Enabled
3. LLM configured to OpenAI
4. Pre-requisites

### Install SuperAgentX :
```shell
pip install superagentx superagentx-handlers
```

### Set OpenAI KEY :  
```shell
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxx
```

### Set RAPIDAPI KEY :

Set Rapid API Key <a href="https://rapidapi.com/auth/sign-up" target="_blank">Free Subscription</a> for Amazon, Walmart Search APIs
```shell
export RAPID_API_KEY= xxxxxxxxxxxxxxxxxxxxxxxx
```

# Ecom IOPipe
``` python
import asyncio

from rich import print as rprint
from superagentx.pipeimpl.iopipe import IOPipe

from superagentx_examples.ecom.pipe import get_ecom_pipe


async def main():
    """
    Launches the e-commerce pipeline console client for processing requests and handling data.
    """

    pipe = await get_ecom_pipe()

    # Create IO Cli Console - Interface
    io_pipe = IOPipe(
        search_name='SuperAgentX Ecom',
        agentx_pipe=pipe,
        read_prompt=f"\n[bold green]Enter your search here"
    )
    await io_pipe.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")

```

### To Run IOPipe :
```shell
python3 superagentx_examples/ecom/ecom_iopipe.py
```

# Ecom WSPipe

### Example Usage
To launch the WebSocket PIPE, follow these steps:


``` python 
import asyncio

from rich import print as rprint
from superagentx.pipeimpl.wspipe import WSPipe

from superagentx_examples.ecom.pipe import get_ecom_pipe


async def main():
    """
    Launches the e-commerce pipeline websocket server for processing requests and handling data.
    """
    pipe = await get_ecom_pipe()
    ws_pipe = WSPipe(
        search_name='SuperAgentX Ecom Websocket Server',
        agentx_pipe=pipe
    )
    await ws_pipe.start()


if __name__ =='__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        rprint("\nUser canceled the [bold yellow][i]pipe[/i]!")

```

# Ecom WSPipe cli
The ecom_wspipe_cli component is a WebSocket client that connects to the e-commerce server to handle real-time search requests. It’s perfect for users wanting a live, interactive way to query the e-commerce pipeline.


### Example Usage
To launch the WebSocket CLI and begin a search:

```python
import asyncio
import json

from rich import print as rprint
from rich.prompt import Prompt
from superagentx.utils.helper import sync_to_async
from websockets.asyncio.client import connect


async def ecom_pipe_cli():
    """
    Launches the e-commerce pipeline websocket client for processing requests and handling data.
    """

    uri = "ws://localhost:8765"
    rprint(f'[bold blue]{10*"-"}Superagentx Ecom Websocket Cli{10*"-"}')

    async with connect(uri) as websocket:
        while True:
            query = await sync_to_async(Prompt.ask, '\n[bold green]Enter your search here')
            await websocket.send(json.dumps({'query': query}))
            res = await websocket.recv()
            rprint(f'{res}')


if __name__ == "__main__":
    asyncio.run(ecom_pipe_cli())
```



### To run through websocket :
Step 1 : To start SuperagentX websocket server
```shell
python3 superagentx_examples/ecom/wspipe.py
```
Step 2 : To run SuperagentX Ecom Websocket cli
```shell
python3 superagentx_examples/ecom/ecom_wspipe_cli.py
```


# Ecom FastAPI 
The ecom_fastapi module creates a RESTful API service that provides a search endpoint to interact with the e-commerce pipeline. This API makes it easy to send search queries programmatically and receive e-commerce data in a structured JSON format.

### EXAMPLE USAGE :
To launch the FastAPI service, follow these steps:

### Install FastAPI and its dependencies
```shell
pip install 'fastapi[standard]'
```
```python
from contextlib import asynccontextmanager

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


ecom_app = FastAPI(
    title='Ecom Search',
    lifespan=lifespan
)


@ecom_app.get('/search')
async def search(query: str) -> list[GoalResult]:
    ecom_pipe: AgentXPipe = pipes.get('ecom_pipe')
    return await ecom_pipe.flow(query_instruction=query)

```

### To Run in Development Mode :
```
fastapi dev superagentx_examples/ecom/ecom_fastapi.py
```

### To Run in Server Mode :
```
fastapi run superagentx_examples/ecom/ecom_fastapi.py
```

##### Usage - Example SuperAgentX Ecom Result
SuperAgentX Ecom searches for product items requested by the user in the console, validates them against the set goal, and returns the result. It retains the context, allowing it to respond to the user's next prompt in the IO Console intelligently. 

![Output](https://github.com/superagentxai/superagentX/blob/master/docs/images/examples/ecom-output-console.png?raw=True)
