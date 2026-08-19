import os
import json
import logging
from groq import Groq
from typing import List, Dict

logger = logging.getLogger(__name__)

def get_groq_client():
    """Retrieve or initialize the Groq client with the current API key."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logger.warning("GROQ_API_KEY is not set in environment variables.")
    return Groq(api_key=api_key)

# Maximum number of retry attempts when JSON parsing fails
MAX_RETRIES = 2

# ──────────────────────────────────────────────
# Refined System Prompt (Phase 5 — Prompt Tuning)
# ──────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are an expert Zomato restaurant recommendation assistant.\n\n"
    "## Your Task\n"
    "Given a user's soft preferences and a pre-filtered list of candidate restaurants, "
    "rank and return the **top 3-5** restaurants that best match their preferences.\n\n"
    "## Ranking Criteria (in priority order)\n"
    "1. **Preference Alignment** — How well does the restaurant match the user's stated mood, vibe, "
    "or dietary requirements?\n"
    "2. **Cuisine Match** — Does the restaurant serve the type of food the user is craving?\n"
    "3. **Rating & Reviews** — Higher-rated restaurants should be preferred when other factors are equal.\n"
    "4. **Value for Money** — Consider the cost relative to the user's budget tier.\n\n"
    "## Anti-Hallucination Rules\n"
    "- You MUST ONLY recommend restaurants from the provided list. NEVER invent restaurants.\n"
    "- You MUST use the exact 'id', 'name', 'rating', 'cost_for_two', 'cuisines', 'location', "
    "'budget_tier', and 'features' values from the input data. Do NOT fabricate or modify these values.\n"
    "- If fewer than 3 restaurants are a good fit, return only those that genuinely match.\n\n"
    "## Explanation Guidelines\n"
    "For each recommendation, write a 2-3 sentence 'explanation' that:\n"
    "  - References the user's specific words/preferences.\n"
    "  - Connects them to concrete restaurant attributes (cuisine type, price point, ambiance from features).\n"
    "  - Feels natural and conversational, not generic.\n\n"
    "## Required Output Format\n"
    "Return ONLY a valid JSON object — no markdown, no commentary, no extra text.\n"
    "The JSON must have a single key 'recommendations' containing an array of objects.\n"
    "Each object MUST have exactly these keys:\n"
    "  id, name, location, budget_tier, rating, cost_for_two, cuisines, features, explanation\n\n"
    "Example:\n"
    '{"recommendations": [{"id": 1, "name": "...", "location": "...", "budget_tier": "...", '
    '"rating": 4.2, "cost_for_two": 800, "cuisines": "...", "features": "...", '
    '"explanation": "..."}]}'
)


def _build_user_prompt(user_preferences: str, restaurants: List[Dict]) -> str:
    """Build the user prompt with preferences and restaurant data."""
    return (
        f"## User Preferences\n{user_preferences}\n\n"
        f"## Candidate Restaurants (JSON)\n{json.dumps(restaurants, indent=2)}\n\n"
        "Please rank and return the top recommendations as a JSON object with a 'recommendations' array."
    )


def _parse_llm_response(content: str) -> List[Dict]:
    """Parse the LLM response, stripping any markdown code-fence wrappers."""
    text = content.strip()

    # Strip markdown code fences
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()
    data = json.loads(text)
    return data.get("recommendations", [])


def get_ai_recommendations(user_preferences: str, restaurants: List[Dict]) -> List[Dict]:
    """
    Send the pre-filtered restaurant list and user preferences to the LLM
    and return ranked recommendations with explanations.

    Includes retry-once logic: if the first attempt fails to parse as valid
    JSON, one additional call is made before returning an empty fallback.
    """
    if not restaurants:
        return []

    user_prompt = _build_user_prompt(user_preferences, restaurants)
    client = get_groq_client()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                model="llama-3.1-8b-instant",
                temperature=0.4,         # Lower temperature for more consistent output
                max_tokens=2048,
            )
            content = response.choices[0].message.content
            recommendations = _parse_llm_response(content)

            if recommendations:
                logger.info("LLM returned %d recommendations on attempt %d", len(recommendations), attempt)
                return recommendations

            logger.warning("LLM returned empty recommendations on attempt %d", attempt)

        except json.JSONDecodeError as e:
            logger.warning("JSON parse error on attempt %d: %s", attempt, e)
            if attempt < MAX_RETRIES:
                continue  # Retry
        except Exception as e:
            logger.error("Error calling Groq API on attempt %d: %s", attempt, e)
            break  # Don't retry on non-parse errors

    return []
