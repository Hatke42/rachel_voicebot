# uvicorn main:app
# uvicorn main:app --reload

# Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# custom function Imports
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

# intiate app
app = FastAPI()

# CORS - Origins
origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:4174",
    "http://127.0.0.1:3000",
]

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# check Health


@ app.get("/health")
async def check_health():
    return {"message": "healthy"}


@ app.get("/reset")
async def reset():
    reset_messages()
    return {"message": "healthy"}


# @ app.get("/post-audio-get")
# async def get_audio():

@ app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    # Get saved audio
    # audio_input = open('voice.mp3', 'rb')

    # Save file from Frontend
    with open(file.filename, 'wb') as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, 'rb')

    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guard : Ensure message decoded
    if not message_decoded:
        raise HTTPException(status_code=500, detail="Failed to decode audio")

    # Get ChatGpt Response
    chat_response = get_chat_response(message_decoded)
    print("chat_response :---> ", chat_response)

    # Guard : Ensure chat response
    if not chat_response:
        raise HTTPException(
            status_code=500, detail="Failed to get chat response")

    # store messages
    store_messages(message_decoded, chat_response)

    # Convert ChatGpt Response to Audio
    audio_output = convert_text_to_speech(chat_response)

    # Guard : Ensure chat reponse converted to audio
    if not audio_output:
        raise HTTPException(
            status_code=500, detail="Failed to convert chat response to audio")

    # create a generator that yields chunks of data
    def iterfile():
        yield audio_output
    # Return audio file
    # return StreamingResponse(iterfile(), media_type="audio/mpeg")
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
