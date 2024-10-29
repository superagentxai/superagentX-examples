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

  * LLM CONFIGURATION : Leverages the power of large language models to handle and process requests, ensuring high accuracy and adaptability in various e-commerce scenarios.

  * Prompt Template: Creates a customizable prompt template that guides the engine's interactions with each platform, ensuring clear, efficient communication with each handler.

  * Marketplace Engines: Develops separate engines for Amazon and Walmart, allowing the application to interface with each marketplace's unique requirements and capabilities.

  * Parallel Processing with Agents: Utilizes a powerful agent to run the Amazon and Walmart engines simultaneously, allowing users to search for products across both platforms in parallel for faster and broader results.

### ECOM WSPIPE CLI :
The ecom_wspipe_cli component introduces a WebSocket client that connects directly to the e-commerce pipeline server to handle search requests in real time. This client interface is ideal for users who want a live, interactive experience while querying the e-commerce pipeline.

* Connect to WebSocket Server : The client initiates a connection to the WebSocket server at ws://localhost:8765, establishing a live data exchange channel.

* User Input : Using a prompt, the client prompts the user to enter their search query. This input is then packaged as JSON data, ready to be processed by the WebSocket server.

Send Query: The client sends the query to the server, where it is received and processed by the e-commerce pipeline, interacting with Amazon and Walmart as configured.

Receive and Display Results: The server responds with search results or relevant product data, which the client then displays in real-time for the user.

### Example Usage
To launch the WebSocket CLI and begin a search:

```shell
# Launch the WebSocket client:
uri = "ws://localhost:8765"
rprint(f'[bold blue]{10*"-"} Superagentx Ecom WebSocket CLI {10*"-"}')

async with connect(uri) as websocket:
    while True:
        query = await sync_to_async(Prompt.ask, '\n[bold green]Enter your search here')
        await websocket.send(json.dumps({'query': query}))
        res = await websocket.recv()
        rprint(f'{res}')
```

This example code demonstrates a streamlined search workflow where user input is sent to the server, and results are returned in real-time for a responsive and efficient e-commerce experience.
