from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os

from src.python.utils.config import settings
from src.python.core.bot import FacebookBot

app = FastAPI(title="Facebook Bot Gateway")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files (Output)
if not settings.OUTPUT_DIR.exists():
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/output", StaticFiles(directory=settings.OUTPUT_DIR), name="output")

# --- Models ---
class TaskRequest(BaseModel):
    profile_id: str = "default"
    task_type: str  # e.g., "like_post", "like_page", "full_flow"
    
    # Parameters for specific tasks
    fanpage_link: Optional[str] = None
    post_links: Optional[List[str]] = []
    num_posts: Optional[int] = 2

# --- Endpoints ---
@app.get("/health")
def health_check():
    """
    Health check endpoint to verify backend status.
    Returns:
        dict: Status message.
    """
    return {"status": "ok", "mode": "refactored"}

@app.post("/run-bot")
def run_bot(req: TaskRequest):
    """
    Triggers the Facebook Bot with the specified task.
    
    Args:
        req (TaskRequest): The task configuration payload.
        
    Returns:
        dict: Success message and task details.
    """
    try:
        # Initialize Bot
        bot = FacebookBot(profile_id=req.profile_id)
        
        # Prepare params
        params = {
            "fanpage_link": req.fanpage_link,
            "post_links": req.post_links,
            "num_posts": req.num_posts,
            "url": req.fanpage_link or (req.post_links[0] if req.post_links else None),
            "close_after": True
        }
        
        # Run Task
        bot.run_task(req.task_type, params)
        
        return {
            "status": "success",
            "message": f"Task '{req.task_type}' completed successfully.",
            "profile": req.profile_id
        }
        
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7000)