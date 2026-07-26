from flask import Blueprint, request, jsonify

from flask_login import login_required, current_user

from database.database import db
from database.models import Trip

from services.ai_service import client
from services.trip_builder import rebuild_trip_data
from services.trip_editor import apply_trip_changes

import json


chat = Blueprint(
    "chat",
    __name__
)


@chat.route("/chat/trip/<int:trip_id>", methods=["POST"])
@login_required
def trip_chat(trip_id):


    trip = Trip.query.get_or_404(
        trip_id
    )


    if trip.user_id != current_user.id:

        return jsonify({
            "error": "Unauthorized"
        }), 403


    data = request.json

    user_message = data.get(
        "message",
        ""
    )


    if not user_message:

        return jsonify({
            "error": "Message empty"
        }), 400


    prompt = f"""
You are TravelMind AI.

You are editing an existing travel itinerary.

Current Trip:

{json.dumps(trip.trip_plan, indent=2)}

User Request:

{user_message}


IMPORTANT RULES

1. NEVER rewrite the whole itinerary.

2. Return ONLY the fields that need changing.

3. Keep everything else exactly the same.

4. Preserve all existing activities,
restaurants,
dates,
weather,
routes,
budget,
packing list,
food,
tips,
etc.

5. Only modify information directly requested.

6. Return VALID JSON ONLY.

7. The trip contains a list called "days".

    The first object in the list is Day 1.
    The second object is Day 2.
    The third object is Day 3.

    Use EXACTLY the day number requested by the user.

    If the user says "Day 2", return:

    {{
    "days": {{
        "2": {{
        ...
        }}
    }}
    }}

    Never subtract 1.
    Never renumber the itinerary.
    Never guess a different day.

    

Examples

User:
Change Day 4 morning to hiking.

Return:

{{
    "days": {{
        "4": {{
            "morning": {{
                "activity":"Hiking at Johnston Canyon"
            }}
        }}
    }}
}}

User:
Increase hotel budget by $200.

Return:

{{
    "budget": {{
        "accommodation": 2200,
        "total": 5200
    }}
}}

User:
Make the trip cheaper.

You MAY modify several related budget fields.

Never regenerate the entire itinerary.
"""


    try:


        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You edit travel itineraries. Return JSON only."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.1,

            max_tokens=2000

        )


        ai_text = response.choices[0].message.content

        ai_text = ai_text.replace(
            "```json",
            ""
        )

        ai_text = ai_text.replace(
            "```",
            ""
        )

        ai_text = ai_text.strip()


        changes = json.loads(
            ai_text
        )

        print("AI returned:")
        print(json.dumps(changes, indent=2))


        updated_trip = apply_trip_changes(

            trip.trip_plan,

            changes

        )


        trip.trip_plan = updated_trip


        weather = rebuild_trip_data(
            trip
        )


        db.session.commit()


        return jsonify({

            "message":
            "Trip updated successfully!",

            "trip_plan":
            updated_trip

        })


    except Exception as e:

        print(
            "Chat error:",
            e
        )

        return jsonify({

            "error":
            "AI update failed"

        }), 500