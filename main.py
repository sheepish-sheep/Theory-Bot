from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from theory_generator import generate_unhinged_theory, generate_franchise_theory
from utils import call_llm_api
import os
from datetime import datetime

app = FastAPI(title="Theory Bot API")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class TheoryRequest(BaseModel):
    mode: str
    text: str = ""
    franchise_name: str = None

@app.get("/health")
async def health_check():
    """Health check endpoint to verify server and LLM API connection."""
    try:
        # Quick LLM API check with a simple prompt
        test_response = call_llm_api("Say 'LLM is healthy'")
        llm_status = "connected" if "healthy" in test_response.lower() else "responding but unexpected output"
    except Exception as e:
        llm_status = f"error: {str(e)}"
    
    return {
        "status": "online",
        "llm_api": llm_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/generate-theory")
async def generate_theory(request: TheoryRequest):
    try:
        if request.mode == "unhinged":
            if not request.text:
                raise HTTPException(status_code=400, detail="Text input is required for unhinged mode")
            
            # Trim input text if it's too long
            input_text = request.text[:500] if len(request.text) > 500 else request.text
            theory = generate_unhinged_theory(input_text)
            
            # Check if the response indicates an error
            if theory.startswith("Error:"):
                raise HTTPException(status_code=500, detail=theory)
                
            return {"theory": theory}

        elif request.mode == "franchise":
            if not request.franchise_name:
                raise HTTPException(status_code=400, detail="Franchise name is required for franchise mode")
            
            # Trim input text and franchise name if they're too long
            franchise = request.franchise_name[:100]
            input_text = request.text[:300] if request.text and len(request.text) > 300 else request.text
            
            theory = generate_franchise_theory(franchise, input_text)
            
            # Check if the response indicates an error
            if theory.startswith("Error:"):
                raise HTTPException(status_code=500, detail=theory)
                
            return {"theory": theory}

        else:
            raise HTTPException(status_code=400, detail="Invalid mode. Use 'unhinged' or 'franchise'")

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating theory: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
