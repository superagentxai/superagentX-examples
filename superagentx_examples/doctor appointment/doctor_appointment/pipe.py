from superagentx.agent import Agent
from superagentx.agentxpipe import AgentXPipe
from superagentx.engine import Engine
from superagentx.llm import LLMClient
from superagentx.memory import Memory
from superagentx.prompt import PromptTemplate

from superagentx.handler import AIHandler  # Some default handlers from SuperAgentX framework

# Import handlers
from superagentx_handlers.sql import SQLHandler


async def get_doctor_appointment_pipe() -> AgentXPipe:
    # LLM Configuration
    llm_config = {
        "model": 'anthropic.claude-3-5-haiku-20241022-v1:0',
        "llm_type": 'bedrock'
    }

    llm_client = LLMClient(llm_config=llm_config)

    # Enable Memory
    memory = Memory(
        memory_config={
            "llm_client": llm_client,
            "db_path": "doctor_appointment/data/memory.db"
        }
    )

    # Handler (Tools)
    database = "doctor_appointment/data/hospital_data.sqlite3"
    sqlite_handler = SQLHandler(
        database_type="sqlite",
        database=database
    )

    # Set System Prompt to provide instructions for the LLM
    doctor_find_prompt = """
    You are an expert in SQL and SQLite. Your task is to analyze and fetch the data from the hospital database.

    The schema of the database is as follows:

    1. Table: doctor_availability
       - Id (TEXT, PRIMARY KEY)
       - name (TEXT)
       - available_days (TEXT)
       - available_time_slots (TEXT)
       - specialization (TEXT)

    Specializations are : 
    Orthopedic Specialist, General Practitioner, Cardiologist, Internal Medicine Specialist, Allergist.

    Sample format:

    Id: <doctor_id here>
    name: <doctor_name here>
    available_days: <available_days here>
    available_time_slots: <available_time_slots here>
    specialization: <specialization here>

    Your task is to:
    1. Fetch the schedule of doctors based on their specialization from the Table.
    2. Ensure that the query is optimized and uses the schema correctly.
    3. Handle scenarios where no appointments exist for a specific doctor or specialization.

    Do not make assumptions about additional columns or tables unless explicitly stated.
     If further clarification is needed, include comments in the query.
    """

    appointment_gen_prompt = """
    You are a SQLite and SQL expert. Fetch the following details from the hospital_data.sqlite3
    You are a professional appointment letter writer.

    **IMPORTANT**:
    You should only generate appointment letter if user asks you to generate.
    Eg Input : "Make an appointment letter for the doctor"

    Your task is to generate a concise and professional appointment letter for a patient based on the provided context.
     The letter must include the following details:
    - Doctor's name
    - Doctor's ID
    - Patient ID
    - Token number
    - Appointment day
    - Appointment time
    - Specialization

    **IMPORTANT INSTRUCTIONS**:
    1. The letter should be concise, limited to **100-150 words**.
    2. Write the output as a **single continuous block of text** without unnecessary newlines (`\n`) or
     special characters.
    3. Avoid structured formats like JSON, YAML, or bullet points.
    4. Ensure the letter is polite, professional, and easy to understand.
    5. Do not include headings, subheadings, or lists unless explicitly required.

    **Sample Format**:
    ---
    Dear Patient, Your orthopedic consultation has been confirmed. 
    Below are the details: Doctor: Dr.Muller (Doctor ID: D90143). Patient ID: PI2385. Token Number: 1123. Date: Monday. 
    Time: 11:00 AM. Please arrive 15 minutes early for registration and bring any relevant medical records. 
    Should you need to reschedule, contact us at least 24 hours in advance. 
    Thank you for choosing our healthcare services. Warm regards, [Your Organization Name]
    ---

    DO NOT include additional instructions unless explicitly required.
    DO NOT include [Patient Name]

    The output should be in the paragraph format
    """

    # Prompt Template

    prompt_template_find = PromptTemplate(
        system_message=doctor_find_prompt
    )

    prompt_template_book = PromptTemplate(
        system_message=appointment_gen_prompt
    )

    doctor_find_engine = Engine(
        handler=sqlite_handler,
        llm=llm_client,
        prompt_template=prompt_template_find
    )

    appointment_gen_handler = AIHandler(
        llm=llm_client,
        role='Professional Appointment Letter Writer',
        story_content='Expert at creating formal, paragraph-style appointment letters.',
    )

    appointment_gen_engine = Engine(
        handler=appointment_gen_handler,
        llm=llm_client,
        prompt_template=prompt_template_book
    )

    doctor_find_agent = Agent(
        name="Doctor Availability Agent",
        role="You're an expert to find doctor's availability",
        goal="Find doctor availability in a json data",
        llm=llm_client,
        prompt_template=prompt_template_find,
        engines=[[doctor_find_engine]],
        max_retry=2
    )

    letter_gen_agent = Agent(
        name="Appointment Letter Agent",
        role='Generate formal, paragraph-style appointment letters.',
        goal='Write a detailed patient appointment letter in natural human-readable text. Avoid JSON format',
        llm=llm_client,
        prompt_template=prompt_template_book,
        engines=[[appointment_gen_engine]],
        max_retry=2
    )

    # Create Pipe - Interface
    # Pipe Interface to send it to public accessible interface (Cli Console / WebSocket / Restful API)
    pipe = AgentXPipe(
        agents=[doctor_find_agent, letter_gen_agent],  # letter_gen_agent
        memory=memory
    )
    return pipe
