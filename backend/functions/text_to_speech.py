import requests
from decouple import config

ELEVEN_LABS_API_KEY = config('ELEVEN_LABS_API_KEY')

# Eleven Labs
# Convert Text to Speech


def convert_text_to_speech(message_text):

    # Define Data (Body)
    body = {
        "text": message_text,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
        }
    }

    # Define Voice
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"

    # Constructing Headers and Endpoint
    headers = {"x-api-key": ELEVEN_LABS_API_KEY,
               "Content-Type": "application/json", "accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return

    # Handle Response
    if response.status_code == 200:
        return response.content
    else:
        print("------response None---->", response.status_code, response.text)
        return
