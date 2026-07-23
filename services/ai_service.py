import os
import json

from dotenv import load_dotenv
from groq import Groq


import time
from groq import RateLimitError

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
    trip_goal,
    budget_analysis,
    traveler_type,
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

        Traveler type:
        {traveler_type}


        Budget Analysis:

        Estimated realistic costs:

        {budget_analysis}


        IMPORTANT:

        Use this analysis when creating the budget.

        Do not exceed the user's budget.

        If the budget is low:
        - suggest cheaper activities
        - avoid luxury accommodation
        - prioritize free attractions



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

        14. Do not recommend expensive options if they exceed the budget.

        15. Only recommend real and well-known attractions.
            Do not invent businesses, hotels, restaurants, or locations.

        16. Respect the user's accommodation preference.

        17. Provide weather-related advice based on destination and dates.

        18. Create a practical packing checklist.

        19. Recommend realistic local foods or dishes.

        20. Include important safety considerations.

        21. Include useful travel tips.

        22. Adapt activities based on traveler type.

        23. The provided Budget Analysis is the source of truth.

        24. Do NOT create your own budget calculations.

        25. Use the estimated costs from Budget Analysis.

        26. The budget total must exactly match the provided estimated total.

        27. Adjust activities and recommendations based on the available budget.



        MAP LOCATION REQUIREMENTS:

        28. Every activity MUST include a real physical location.

        29. Separate the location name from the activity description.

        30. The "place" field must ONLY contain the location name.

        31. The "activity" field must ONLY contain what the traveler does.

        32. Never combine the location and activity together.




        33. Now on the final trip dont assume that they will want to go back to home, so keep in mind that all trips will be one way trips and the last day will be the last location of the trip, so dont suggest that they will go back to home.

        34. Also double check if all the locations are real and exist in the city your visiting.

        35. And if you are suggesting a restaurant, cafe or anything that is not very polular, instead just provide the address. (ex. location : 24 banff anvenu; Activity: Eat the famous poutine at sparky's diner). Please make sure to provide the address of the location


        Examples:


        Correct:

        {{
            "place": "Johnston Canyon, Banff, Alberta, Canada",
            "activity": "Hike the Lower and Upper Falls trail"
        }}


        Incorrect:

        {{
            "place": "Visit Johnston Canyon and hike the falls"
        }}


        IMPORTANT:

        Return only the itinerary content.

        Do not include explanations about being an AI.

        Do not create fake attractions.

        If unsure about a location, suggest a popular alternative.



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
                "total": number,
                "per_person": number
            }},

            "weather_tips": [
                "weather advice item 1"
            ],

            "packing_list": [
                "packing item 1"
            ],

            "local_food": [
                "recommended food item 1"
            ],

            "safety_tips": [
                "safety advice item 1"
            ],

            "travel_tips": [
                "travel advice item 1"
            ],


            "days": [

                {{
                    "date": "YYYY-MM-DD",

                    "morning": {{
                        "place": "real location name, province/state, country",
                        "activity": "activity description"
                    }},

                    "afternoon": {{
                        "place": "real location name, province/state, country",
                        "activity": "activity description"
                    }},

                    "evening": {{
                        "place": "real location name, province/state, country",
                        "activity": "activity description"
                    }}
                }}

            ]

        }}



        Rules:

        - Number of days must match trip duration.

        - Budget values must be numbers only.

        - Total must equal the sum of budget categories.

        - Dates must match travel dates.

        - Every morning, afternoon, and evening must contain:
            - place
            - activity

        - Place names must be real locations.

        - Do not invent attractions, restaurants, or hotels.

        """



    try:

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

            temperature=0.2,

            max_tokens=3500

        )


    except RateLimitError:

        print("Groq rate limit reached. Waiting...")

        time.sleep(30)


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

            temperature=0.2,

            max_tokens=3500

        )


    ai_text = response.choices[0].message.content


    ai_text = ai_text.replace("```json", "")
    ai_text = ai_text.replace("```", "")

    ai_text = ai_text.strip()


    try:

        trip_data = json.loads(ai_text)

    except json.JSONDecodeError:

        print("AI JSON ERROR:")
        print(ai_text)

        raise Exception(
            "AI returned invalid JSON format"
        )


    return trip_data