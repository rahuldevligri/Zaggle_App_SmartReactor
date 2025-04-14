import re
from tenacity import retry, stop_after_attempt, wait_exponential
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_review_embedding(review_text):
    try:
        response = openai.embeddings.create(
            input=review_text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except openai.APIError as e:
        print(f"🚨 OpenAI API Error: {str(e)}")
        raise

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generate_response(review_text, rating, faq_answer=None, product=None):
    products = {
        'SAVE': {
            'email': 'care@zaggle.in',
            'phone': '18605001231',
            'display_name': 'SAVE',
            'greeting': 'Hi there,'
        },
        'Propel': {
            'email': 'team@zaggle.in',
            'phone': '18605003748',
            'display_name': 'Propel',
            'greeting': 'Hello,'
        },
        'EMS': {
            'email': 'care@zaggle.in',
            'phone': '+91 7396680101',
            'display_name': 'EMS',
            'greeting': 'Dear Valued User,'
        },
        'default': {
            'email': 'care@zaggle.in',
            'phone': '18605001231',
            'display_name': 'Zaggle',
            'greeting': 'Hello,'
        }
    }

    # Detect product: prefer explicit input, fallback to detection, else default
    normalized_product = product.strip().capitalize() if product else None
    if normalized_product in products:
        detected_product = normalized_product
    elif 'save' in review_text.lower():
        detected_product = 'SAVE'
    else:
        detected_product = 'default'

    product_info = products[detected_product]

    try:
        prompt = f"""You are a warm, friendly, and empathetic customer support specialist at {product_info['display_name']}. A user has just left the following app review:

Review: "{review_text}"
Rating: {rating}/5
FAQ Context: {faq_answer or 'No additional context'}

Write a short, precise response — strictly within 4 lines (excluding contact info) — that feels supportive and human — like chatting with a caring friend. Make it casual, natural, and kind. Here’s how to craft it:

- If rating < 4: start with a warm, genuine apology and thank them for their honesty
- Acknowledge their main complaints with empathy
- Suggest 2–3 helpful workarounds or tips
- Mention that updates or improvements are in progress
- Only include contact info and sign-off once at the end
- Format exactly like this:

{product_info['greeting']}

[Response body]

---
Contact us:
✉️ : {product_info['email']}
📞 : {product_info['phone']}

Warm regards,  
{product_info['display_name']} Team
"""

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly and empathetic support expert who responds to users like a helpful buddy. Your tone is casual, clear, and warm."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=350
        )

        response_text = response.choices[0].message.content.strip()

        # Ensure greeting is present once at the top
        if not response_text.startswith(product_info['greeting']):
            response_text = f"{product_info['greeting']}\n\n{response_text}"

        # Remove any existing contact section and signature before adding our version
        response_text = re.sub(
            r"---\s*Contact us:.*?(?:Warm regards,)?\s*.*?Team",
            "",
            response_text,
            flags=re.IGNORECASE | re.DOTALL
        )

        # Clean up duplicate sign-offs and whitespace
        team_signature_pattern = rf"(Warm regards,.*?$)|({re.escape(product_info['display_name'])} Team\s*)"
        response_text = re.sub(team_signature_pattern, "", response_text, flags=re.IGNORECASE | re.DOTALL | re.MULTILINE)

        # Final append of contact + signature
        response_text = response_text.strip() + f"""\n\n---
Contact us:
✉️ : {product_info['email']}
📞 : {product_info['phone']}

Warm regards,  
{product_info['display_name']} Team"""

        return response_text

    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return f"""{product_info['greeting']}

We really appreciate you taking the time to share your thoughts. We're here to help however we can! 😊

---
Contact us:
✉️ : {product_info['email']}
📞 : {product_info['phone']}

Warm regards,  
{product_info['display_name']} Team"""
