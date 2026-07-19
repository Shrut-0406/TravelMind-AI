import os
import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



def generate_trip_plan(
    origin,
    destination,
    start_date,
    end_date,
    days,
    adults,
    children,
    budget,
    transportation,
    accommodation,
    interests,
    trip_goal
):


    prompt = f"""

        You are TravelMind AI, an expert personal travel planner.

        Create a realistic and personalized travel itinerary.


        Traveler Information:

        Starting location:
        {origin}

        Destination:
        {destination}

        Travel dates:
        {start_date} to {end_date}

        Trip duration:
        {days} days


        Travelers:

        Adults:
        {adults}

        Children:
        {children}



        Budget:

        Total budget:
        ${budget}



        Preferences:

        Transportation:
        {transportation}

        Accommodation preference:
        {accommodation}

        Interests:
        {", ".join(interests)}

        Trip goal:
        {trip_goal}



        Instructions:

        1. Create a day-by-day itinerary.

        2. Consider the traveler's starting location.

        3. Respect the budget.

        4. Recommend realistic travel times.

        5. Avoid scheduling too many activities in one day.

        6. Include:
        - Morning activity
        - Afternoon activity
        - Evening activity

        7. Include approximate costs.

        8. Include food recommendations.

        9. Suggest transportation details.

        10. Make recommendations suitable for the number of travelers.

        11. Carefully calculate the budget.
        The total estimated cost must not exceed the provided budget.

        12. Consider the number of travelers when calculating food and activity costs.

        13. If the budget is unrealistic, explain where adjustments are needed.

        14 . Do not recommend expensive options if they exceed the budget.

        15. Only recommend real and well-known attractions.
            Do not invent businesses, hotels, restaurants, or locations.

        16. Respect the user's accommodation preference.


        IMPORTANT:
            Return only the itinerary content.
            Do not include explanations about being an AI.
            Do not create fake attractions.
            If you are unsure about a location, suggest a popular alternative.
        

        Output format:

        Return ONLY valid JSON.

        Do not include markdown.
        Do not include ```.

        Use this exact structure:

        {{
            "summary": "short trip summary",

            "budget": {{
                "accommodation": number,
                "food": number,
                "transportation": number,
                "activities": number,
                "total": number
            }},

            "days": [
                {{
                    "date": "YYYY-MM-DD",
                    "morning": "activity description",
                    "afternoon": "activity description",
                    "evening": "activity description"
                }}
            ]
        }}

        Rules:

        - The number of days must match the trip duration.
        - Budget values must be numbers only.
        - Total must equal the sum of budget categories.
        - Dates must match the travel dates.

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

        temperature=0.4,

        max_tokens=3000

    )


    ai_text = response.choices[0].message.content

    trip_data = json.loads(ai_text)

    return trip_data