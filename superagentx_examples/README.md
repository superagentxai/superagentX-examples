<div align="center">

<img src="https://github.com/superagentxai/superagentX/blob/master/docs/images/fulllogo_transparent.png?raw=True" width="350">


<br/>

**Superagentx-Ecom-Examples**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![GitHub Repo stars](https://img.shields.io/github/stars/superagentxai/superagentX-examples)](https://github.com/superagentxai/superagentX-examples)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/superagentxai/superagentX-examples/blob/master/LICENSE)
</div>

### OVERVIEW :
The Superagentx-Ecom-Examples repository provides a robust e-commerce pipeline designed to simplify interactions with multiple online marketplaces. This project utilizes Large Language Model (LLM) configurations to build and manage agents that can search, retrieve, and interact with e-commerce data sources such as Amazon and Walmart.


### ECOM IOPIPE :
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


### ECOM WSPIPE CLI :
The ecom_wspipe_cli component introduces a WebSocket client that connects directly to the e-commerce pipeline server to handle search requests in real time. This client interface is ideal for users who want a live, interactive experience while querying the e-commerce pipeline.


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

This example code demonstrates a streamlined search workflow where user input is sent to the server, and results are returned in real-time for a responsive and efficient e-commerce experience.

### ECOM WSPIPE :
The ecom_wspipe component is a WebSocket server that powers real-time interaction between users and the e-commerce pipeline. 

Set Rapid API Key <a href="https://rapidapi.com/auth/sign-up" target="_blank">Free Subscription</a> for Amazon, Walmart Search APIs

```shell
export RAPID_API_KEY= xxxxxxxxxxxxxxxxxxxxxxxx
```

```python
import asyncio
import os

from rich import print as rprint
from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.engine import Engine
from superagentx.llm import LLMClient
from superagentx.pipeimpl.wspipe import WSPipe
from superagentx.prompt import PromptTemplate
from superagentx_handlers.ecommerce.amazon import AmazonHandler
from superagentx_handlers.ecommerce.flipkart import FlipkartHandler


async def main():
    """
    Launches the e-commerce pipeline websocket server for processing requests and handling data.
    """
    llm_config = {'model': 'gpt-4-turbo-2024-04-09', 'llm_type': 'openai'}

    llm_client: LLMClient = LLMClient(llm_config=llm_config)
    amazon_ecom_handler = AmazonHandler(
        api_key=os.getenv('RAPID_API_KEY'),
        country="IN"
    )
    flipkart_ecom_handler = FlipkartHandler(
        api_key=os.getenv('RAPID_API_KEY'),
    )
    prompt_template = PromptTemplate()
    amazon_engine = Engine(
        handler=amazon_ecom_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )
    flipkart_engine = Engine(
        handler=flipkart_ecom_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )
    ecom_agent = Agent(
        name='Ecom Agent',
        goal="Get me the best search results",
        role="You are the best product searcher",
        llm=llm_client,
        prompt_template=prompt_template,
        engines=[[amazon_engine, flipkart_engine]]
    )
    pipe = AgentXPipe(
        agents=[ecom_agent]
    )
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

### ECOM FASTAPI :
The ecom_fastapi module creates a RESTful API service that provides a search endpoint to interact with the e-commerce pipeline. This API makes it easy to send search queries programmatically and receive e-commerce data in a structured JSON format.

### EXAMPLE USAGE :
To launch the FastAPI service, follow these steps:

# Install FastAPI and its dependencies
```
pip install 'fastapi[standard]'
```


# Run in Development Mode
```
fastapi dev superagentx_examples/ecom/ecom_fastapi.py
```

# Run in Server Mode
```
fastapi run superagentx_examples/ecom/ecom_fastapi.py
```

##### Usage - Example SuperAgentX Result
SuperAgentX searches for product items requested by the user in the console, validates them against the set goal, and returns the result. It retains the context, allowing it to respond to the user's next prompt in the IO Console intelligently. 

### OUTPUT
[GoalResult(reason='The Vivo X90 is the most affordable option among the smartphones listed, with a price of 22002.08, and adequate features that fulfill the need for a smartphone that combines a good balance of performance, photography capabilities, and battery life.', result={'id': '14bad2987c884eb49e871e38c5ebf1d8', 'title': 'Vivo X90', 'price': 22002.08, 'description': "The Vivo X90 is a cutting-edge smartphone that epitomizes both style and functionality. This model is designed to cater to tech enthusiasts seeking advanced photography capabilities, robust performance, and all-day battery life. Equipped with Vivo's latest imaging system, it offers unparalleled photo clarity and color accuracy, ideal for capturing those spectacular moments in utmost detail. The X90 runs on a powerful chipset that ensures smooth, lightning-fast responses for both daily tasks and intense gaming sessions. Coupled with a vibrant, high-resolution display, the Vivo X90 guarantees a truly immersive viewing experience. Whether it's for professional photography, high-speed gaming, or day-to-day efficiency, the Vivo X90 is engineered to exceed expectations in every aspect, making it the ultimate companion for the modern smartphone user.", 'category': 'Mobile Phone, smartphone', 'provider': 'Flipkart', 'image': 'https://fakeflipkartstoreapi.com/img/Vivo X90.jpg', 'rating': {'rate': 2.7, 'count': 186}}, is_goal_satisfied=True)]
PASSED