from fastapi import FastAPI, Request
from calendar_helper import get_calendar_service
from agent import BookingAgent

app = FastAPI()
service = get_calendar_service()
agent = BookingAgent(service)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    reply = agent.respond(user_message)
    return {"response": reply}
