# utils/ai.py
import openai
import json

def process_prompt_via_openai(prompt: str, items: list, content_type: str) -> dict:
    """
    Uses OpenAI's GPT-4 to process a natural language prompt.
    Returns a JSON object with key 'actions' listing actions.
    Each action is a dict with 'id', 'action' (create, update, delete), and 'changes' (dict).
    """
    system_prompt = (
        "You are an expert WordPress content editor. "
        "Receive a natural language command and details about content items. "
        "Return a JSON object with a key 'actions' that is a list of actions. "
        "Each action must have 'id' (post id or 'new'), 'action' (create, update, delete), "
        "and 'changes' (a dictionary mapping field names to new values). Do not include extra text."
    )
    user_message = (
        f"User command: {prompt}\n"
        f"Content type: {content_type}\n"
        f"Number of items: {len(items)}.\n"
        "For each item, generate the necessary changes as a JSON object."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.3,
            max_tokens=800
        )
        ai_output = response.choices[0].message['content']
        plan = json.loads(ai_output)
        return plan
    except Exception as e:
        return {"actions": []}
