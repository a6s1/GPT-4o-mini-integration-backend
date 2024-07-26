from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = "your_openai_api_key"  # Replace with your OpenAI API key

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("text")
    if not user_message:
        return {"error": "No message provided"}

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",  # Replace with the appropriate model identifier
        messages=[{"role": "user", "content": user_message}],
        stream=True
    )

    result = ""
    async for chunk in response:
        delta_content = chunk.choices[0].delta.get("content")
        if delta_content:
            result += delta_content

    return {"response": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
