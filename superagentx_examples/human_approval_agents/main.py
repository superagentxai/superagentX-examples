import asyncio
import json
from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.browser_engine import BrowserEngine
from superagentx.llm import LLMClient
from superagentx.prompt import PromptTemplate


async def main():
    print("SuperAgentX – Food Checkout & Payment Automation")

    # ------------------------------------------------------------------
    # LLM SETUP
    # ------------------------------------------------------------------
    llm = LLMClient(
        llm_config={
            "model": "gemini/gemini-3-pro-preview",
            "temperature": 0.1
        }
    )

    # ------------------------------------------------------------------
    # AGENT 1: FOOD & SNACKS CHECKOUT AGENT
    # ------------------------------------------------------------------
    checkout_system_prompt = """
    You are a food & snacks checkout agent. Simulate Food & Snacks Checkout with items.

    Task:
    - Select food and snack items
    - Decide quantities
    - Calculate total amount
    - Prepare checkout summary for payment

    Rules:
    - DO NOT generate any payment or card details
    - DO NOT mention CVV, card numbers, or expiry
    - Output ONLY valid JSON

    JSON Schema:
    {
      "items": [
        {
          "name": string,
          "category": "food | snack",
          "quantity": number,
          "price_per_unit": number
        }
      ],
      "currency": "USD",
      "total_amount": number,
      "checkout_note": string
    }
    """

    checkout_prompt = PromptTemplate(system_message=checkout_system_prompt)

    checkout_agent = Agent(
        name="Food Checkout Agent",
        role="Food & Snacks Checkout Planner",
        goal="Prepare checkout summary",
        llm=llm,
        prompt_template=checkout_prompt,
        max_retry=1
    )

    # ------------------------------------------------------------------
    # AGENT 2: BROWSER REVIEW & PAY AGENT
    # ------------------------------------------------------------------
    browser_system_prompt = """
    You are a browser automation agent responsible for review and payment.

    Input:
    - You will receive a checkout summary JSON from the previous agent.

    Target Payment Form URL:
    https://superagentxai.github.io/payment-demo.github.io/

    Task:
    1. Review checkout summary (items & total) and MUST set the price from result.total_amount
    2. Show checkout summary in the popup with price
    3. Generate DUMMY credit card details for testing:
       - 16-digit test card number
       - Future expiry (MM/YY)
       - 3-digit CVV
       - Realistic cardholder name & address
    4. Fill the payment form using generated card details
    5. Submit the form


    Rules:
    - Change the Price value in the submit button with the actual amount from result.total_amount in USD:.
    - Card details must be generated ONLY by you
    - Use dummy/test card numbers only (e.g., 4111 1111 1111 1111)
    - Do NOT persist card data
    - Do NOT assume submission success
    - Extract confirmation text ONLY if visible

    Output JSON:
    {
      "submission_status": "success | failed",
      "reviewed_total_amount": number,
      "confirmation_text": string | null
    }
    """

    browser_prompt = PromptTemplate(system_message=browser_system_prompt)

    browser_engine = BrowserEngine(
        llm=llm,
        prompt_template=browser_prompt,
        headless=False  # set True in CI
    )

    browser_agent = Agent(
        name="Review & Pay Agent",
        role="Browser Payment Executor",
        goal="Review checkout and pay using credit card",
        llm=llm,
        human_approval=True,   # governance point
        prompt_template=browser_prompt,
        engines=[browser_engine],
        max_retry=2
    )

    # ------------------------------------------------------------------
    # PIPELINE: AGENT 1 → AGENT 2
    # ------------------------------------------------------------------
    pipe = AgentXPipe(
        agents=[checkout_agent, browser_agent], # Sequence Agent Workflow
        workflow_store=True
    )

    result = await pipe.flow(
        query_instruction="Checkout food and snacks, then review and pay using credit card."
    )

    formatted_result = [
        {
            "agent_name": r.name,
            "agent_id": r.agent_id,
            "goal_satisfied": r.is_goal_satisfied,
            "result": r.result
        }
        for r in result
    ]

    print(" Final Result (Formatted JSON)")
    print(json.dumps(formatted_result, indent=2))
    return


if __name__ == "__main__":
    asyncio.run(main())
