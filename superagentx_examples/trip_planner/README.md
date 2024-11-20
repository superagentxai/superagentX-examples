

# Trip Planner - Use case using SuperAgentX


SuperAgentX - A Lightweight Modular Autonomous True Multi Agent AI Framework.

## Introduction
This project demonstrates the use of the SuperAgentX framework to automate trip planning when you're deciding between 
multiple options. SuperAgentX coordinates autonomous AI agents, allowing them to work together to accomplish complex
tasks efficiently.

## Pre-requisites
- **Configure Environment:** -  Set up the environment variables for AWS Bedrock-Runtime and Serper
    - Always set your AWS credentials as environment variables.

          export AWS_ACCESS_KEY=<<`YOUR_ACCESS_KEY`>>
          export AWS_SECRET_KEY=<<`YOUR_ACCESS_SECRET_KEY`>>
          export AWS_REGION=<<`AWS_REGION`>>

    - Serper: `export SERPER_API_KEY="xxxxxxxxxxxxxxxxxxxxxx""`
- **Install Dependencies:**
    - `poetry install`
    - `playwright install`

**Note:** Configure the AWS Bedrock credentials for LLM Configuration.
## Run the Script

Run `python iopipe.py` and enter your idea when prompted. The script will use the SuperAgentX framework
to process your input and generate a landing page.

# Input - CLI Interface
Users interact with this system via a script `(iopipe.py)` that processes input data using AWS's Bedrock
(LLM) via an IO Console interface.

[//]: # (<img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/Screenshot%20from%202024-11-12%2022-36-29.png?raw=true">)

```log
(venv) ➜  trip_planner python3 iopipe.py
Warning: Synchronous WebCrawler is not available. Install crawl4ai[sync] for synchronous support. However, please note that the synchronous version will be deprecated soon.
─────────────────────────────────────────────────────────────────────── SuperAgentX trip_planner ───────────────────────────────────────────────────────────────────────

Enter your search here: Create a 5-day trip for a California trip
                                                  
INFO:superagentx.llm.types.base:Pipe Trip Planner Pipe starting...
(   ●  ) Searching...
(●     ) Searching...
(     ●) Searching...
WARNING:chromadb.segment.impl.vector.local_persistent_hnsw:Number of requested results 10 is greater than number of elements in index 1, updating n_results = 1
[LOG] 🚀 Crawl4AI 0.3.731
[LOG] 🌤️  Warming up the AsyncWebCrawler
[LOG] 🌞 AsyncWebCrawler is ready to crawl
```


# Locations
<table>
  <tr>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/mission-Santa-Barbara.jpg?raw=true"  width=600 height=200>
        <p>Mission Santa Barbara</p>
    </td>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/660332e04a42ee42011d9dbf_91.jpg?raw=true" width=600 height=200>
        <p>Hollywood Walk of Fame</p>
    </td>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/239684-Morro-Rock-San-Luis.jpg?raw=true" width=600 height=200>
        <p>Morro Rock</p>
    </td>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/aa972fdea46cfb31e340fa91dccf6836.jpg?raw=true" width=600 height=200>
        <p>McWay Falls</p>
    </td>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/Bixby-Bridge.jpg?raw=true" width=600 height=200>
        <p>Bixby Creek Bridge</p>
    </td>
  </tr>
  <tr>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/istockphoto-493630062-612x612.jpg?raw=true" width=600 height=200>
        <p>Pigeon Point Lighthouse</p>
    </td>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/monterey-aquarium-17.jpg?raw=true" width=600 height=200>
        <p>Monterey Bay Aquarium</p>
    </td>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/shutterstock_78199996__5184x3456____v1222x580__.jpg?raw=true" width=600 height=200>
        <p>Alcatraz Island</p>
    </td>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/Palace_of_Fine_Arts_(16794p).jpg?raw=true" width=600 height=200>
        <p>Palace of Fine Arts</p>
    </td>
    <td>
        <img src="https://github.com/superagentxai/superagentx/blob/images/docs/images/trip_planner_image/premium_photo-1661963640331-c867191b4641.jpeg?raw=true" width=600 height=200>
        <p>Golden Gate Bridge</p>
    </td>
  </tr>
 </table>

# Result

Upon executing the script, the SuperAgentX framework generates a detailed itinerary for a 5-day California coast trip,
covering notable locations:
```json
{
  "trip_details": {
    "destination": "California Coast",
    "duration": "5 days",
    "best_time_to_visit": {
      "months": [
        "February",
        "March",
        "April"
      ],
      "weather": "Mild coastal weather, potential for rain"
    }
  },
  "itinerary": {
    "day1": {
      "location": "San Francisco",
      "highlights": [
        "Golden Gate Bridge",
        "Palace of Fine Arts",
        "Alcatraz Island",
        "Fisherman's Wharf"
      ]
    },
    "day2": {
      "location": "Monterey and Big Sur",
      "highlights": [
        "Half Moon Bay",
        "Pigeon Point Lighthouse",
        "Cannery Row",
        "Monterey Bay Aquarium",
        "Bixby Creek Bridge",
        "Pfeiffer Beach",
        "McWay Falls"
      ]
    },
    "day3": {
      "location": "San Luis Obispo and Morro Bay",
      "highlights": [
        "Point Lobos",
        "Mission San Luis Obispo de Tolosa",
        "Morro Rock"
      ]
    },
    "day4": {
      "location": "Santa Barbara",
      "highlights": [
        "Mission Santa Barbara",
        "State Street"
      ]
    },
    "day5": {
      "location": "Los Angeles",
      "highlights": [
        "Hollywood Walk of Fame"
      ]
    }
  },
  "budget_considerations": {
    "general": "California is expensive",
    "specific_notes": [
      "High gas prices",
      "Costly accommodations",
      "Potential one-way car rental fees"
    ]
  },
  "vehicle_recommendation": "Mid-size SUV or compact convertible",
  "total_driving_distance": "450-500 miles"
}
```

### REST API Server
```console
# Development mode
fastapi dev trip_planner/restpipe.py

# Production mode
fastapi run trip_planner/restpipe.py

```

### Websocket Server
```console
python trip_planner/wspipe.py
```

## Example
### REST API
```python
# Example
import requests

response = requests.get(
    'http://localhost:8000/search',
    params={'query': 'Plan trip for california with 5 days'},
    headers={'api-token': 'your-auth-token'}
)
```
### WebSocket Client

```python
import websockets

async with websockets.connect(
    'ws://localhost:8765?token=your-auth-token'
) as websocket:
    await websocket.send('Plan trip for california with 5 days')
    response = await websocket.recv()
```

# Conclusion

This project showcases SuperAgentX’s capabilities in coordinating AI agents for trip planning. The generated itinerary
provides an efficient, organized approach to exploring California’s highlights, although users should budget for high
travel costs. The modular, automated nature of SuperAgentX makes it a versatile framework for similar applications
where multiple agent-based decisions are beneficial.
