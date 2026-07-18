import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



def generate_trip_plan(
    destination,
    start_date,
    end_date,
    days,
    budget
):


    prompt = f"""
You are an expert travel planner.

Create a realistic travel itinerary.

Trip details:

Destination:
{destination}

Start date:
{start_date}

End date:
{end_date}

Duration:
{days} days

Budget:
${budget}


Requirements:

- Create a day-by-day itinerary
- Include attractions and activities
- Keep the budget realistic
- Avoid overpacking each day
- Include food suggestions
- Include transportation suggestions
- Make it suitable for a real traveler


Format:

Day 1:
Morning:
Afternoon:
Evening:

Day 2:
Morning:
Afternoon:
Evening:

Continue until the last day.
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": "You are a professional AI travel planner."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.7,

        max_tokens=3000

    )


    return response.choices[0].message.content