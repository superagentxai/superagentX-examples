

# doctor appointment - Use case using SuperAgentX

SuperAgentX - A Lightweight Modular Autonomous True Multi Agent AI Framework.

# Doctor Appointment Booking App - Using SuperAgentX
The doctor appointment booking app is an application built using SuperAgentX framework. This user-friendly smart app helps outpatients identify the best-specialized doctor and book an appointment with the doctor simultaneously.
This interactive app allows users to ask questions in natural language, and it responds by providing information about the doctor's availability.

## Application Architecture
![Architecture](doctor_appointment/data/images/doctor_app_architecture.png)

## Installation
```bash
# Install required packages
pip install superagentx aiohttp fastapi rich websockets certifi

# Clone the repository
git clone git@github.com:superagentxai/superagentX-examples.git
cd superagentX-examples/superagentx_examples/doctor appointment
```

## How to Run - IO Console
```bash
# Run IO console pipe. 
python doctor_appointment/iopipe.py
```

## How to Run - WebSocket Client
```bash
# Run websocket pipe. This will give `ws://localhost:8765` URL. Hit URL in Websocket client
python doctor_appointment/wspipe.py
```


## Demo
![Architecture](doctor_appointment/data/images/SuperAgentX-Doctor-Appointment-Booking-App.png)