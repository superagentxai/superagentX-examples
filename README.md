<div align="center">

<img src="https://github.com/superagentxai/superagentX/blob/master/docs/images/fulllogo_transparent.png?raw=True" width="350">


<br/>


**Superagentx-Examples**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![GitHub Repo stars](https://img.shields.io/github/stars/superagentxai/superagentX-examples)](https://github.com/superagentxai/superagentX-examples)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/superagentxai/superagentX-examples/blob/master/LICENSE)
</div>

### Getting Started

```shell
pip install superagentx-examples
```
##### Usage - Example SuperAgentX Code
This SuperAgentX example utilizes two handlers, Amazon and Walmart, to search for product items based on user input from the IO Console.

1. It uses Parallel execution of handler in the agent 
2. Memory Context Enabled
3. LLM configured to OpenAI
4. Pre-requisites

Set OpenAI Key:  
```shell
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxx
```

Set Rapid API Key <a href="https://rapidapi.com/auth/sign-up" target="_blank">Free Subscription</a> for Amazon, Walmart Search APIs
```shell
export RAPID_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXX
```

```python 
# Additional lib needs to install
# python3 superagentx_examples/ecom_iopipe.py

import asyncio

from rich import print as rprint
from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.engine import Engine
from superagentx.llm import LLMClient
from superagentx.memory import Memory
from superagentx.pipeimpl.iopipe import IOPipe
from superagentx.prompt import PromptTemplate

from superagentx_handlers.ecommerce.amazon import AmazonHandler
from superagentx_handlers.ecommerce.walmart import WalmartHandler


async def main():
    """
    Launches the e-commerce pipeline console client for processing requests and handling data.
    """

    # LLM Configuration
    llm_config = {'llm_type': 'openai'}
    llm_client: LLMClient = LLMClient(llm_config=llm_config)

    # Enable Memory
    memory = Memory(memory_config={"llm_client": llm_client})

    # Add Two Handlers (Tools) - Amazon, Walmart
    amazon_ecom_handler = AmazonHandler()
    walmart_ecom_handler = WalmartHandler()

    # Prompt Template
    prompt_template = PromptTemplate()

    # Amazon & Walmart Engine to execute handlers
    amazon_engine = Engine(
        handler=amazon_ecom_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )
    walmart_engine = Engine(
        handler=walmart_ecom_handler,
        llm=llm_client,
        prompt_template=prompt_template
    )

    # Create Agent with Amazon, Walmart Engines execute in Parallel - Search Products from user prompts
    ecom_agent = Agent(
        name='Ecom Agent',
        goal="Get me the best search results",
        role="You are the best product searcher",
        llm=llm_client,
        prompt_template=prompt_template,
        engines=[[amazon_engine, walmart_engine]]
    )

    # Pipe Interface to send it to public accessible interface (Cli Console / WebSocket / Restful API)
    pipe = AgentXPipe(
        agents=[ecom_agent],
        memory=memory
    )

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
##### Usage - Example SuperAgentX Result
SuperAgentX searches for product items requested by the user in the console, validates them against the set goal, and returns the result. It retains the context, allowing it to respond to the user's next prompt in the IO Console intelligently. 

![Output](https://github.com/superagentxai/superagentX/blob/master/docs/images/examples/ecom-output-console.png?raw=True)
