import asyncio

# Import core modules from SuperAgentX framework
from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.browser_engine import BrowserEngine
from superagentx.engine import Engine
from superagentx.llm import LLMClient
from superagentx.prompt import PromptTemplate

# Custom handler to write data to CSV
from data_handler import DataWriterHandler


async def main():
    print(f"Welcome to SuperAgentX - Browser Multi Agents Automation Tutorial")

    # 1. Set up LLM configuration and client
    llm_config = {"model": "gpt-4.1", "llm_type": "openai"}  # Specify LLM model and provider
    llm = LLMClient(llm_config=llm_config)  # Initialize LLM client with config

    # 2. Define system message to instruct browser agent for precise data collection
    system_message = """You are a precise data collection agent. Go to https://www.google.com/shopping, extract the 
    following details for each product: Name, Price, Seller, Rating.

    Output the results in CSV format with headers: Name, Price, Seller, Rating.

    Important Notes:
    - Price ONLY numeric value (e.g., 1999.99)
    - Rating is a numeric value (e.g., 4.5)
    - Seller ONLY name (E.g., Amazon, Croma)
    - All fields are accurately captured.
    """

    # Create a prompt template using the system message
    prompt_template = PromptTemplate(system_message=system_message)

    # 3. Initialize a browser engine that will use the LLM and prompt to automate browsing
    browser_engine = BrowserEngine(llm=llm, prompt_template=prompt_template)

    # 4. Create an agent to browse and extract eCommerce product data
    browser_agent = Agent(
        llm=llm,
        prompt_template=prompt_template,
        goal="Complete User Input",
        role="You're an ecommerce agent",
        engines=[browser_engine]
    )

    # 5. Define prompt for CSV generation
    csv_prompt = PromptTemplate(system_message="""
        Write data from previous agent's result in csv.
    """)

    # 6. Create a CSV tool handler to write structured data to CSV
    csv_tool = DataWriterHandler()

    # 7. Wrap CSV handler inside an engine
    csv_engine = Engine(
        llm=llm,
        prompt_template=csv_prompt,
        handler=csv_tool
    )

    # 8. Create a second agent responsible for generating a CSV from the scraped data
    csv_agent = Agent(
        name="CSV Agent",
        goal="Write data in csv ",
        role="You are CSV data Expert",
        llm=llm,
        prompt_template=csv_prompt,
        max_retry=1,
        engines=[csv_engine]
    )

    # 9. Compose both agents into a pipeline (browser_agent → csv_agent)
    pipe = AgentXPipe(
        agents=[browser_agent, csv_agent]
    )

    # 10. Execute the pipeline with the given instruction
    result = await pipe.flow(
        query_instruction="Find details about iPhone models and how much they cost."
    )

    # 11. Print final result
    print(f"Result {result}")


# Run the async main function when script is executed directly
if __name__ == "__main__":
    asyncio.run(main())
