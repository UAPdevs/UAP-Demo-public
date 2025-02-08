from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import requests
import os
import logging
import traceback

# Configure logging (before creating the app instance)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)  # Get a logger instance

app = FastAPI()

@app.middleware("http")  # Custom middleware for exception handling
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        tb_str = traceback.format_exc()  # Get the full traceback
        logger.error(f"Internal Server Error: {e}\n{tb_str}") # Log the error AND the traceback
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"}) # Return a generic 500


@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI, testing private subnet 3"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/fetch-private")
async def fetch_private_data():
    try:
        response = requests.get("http://fastapi-private-nlb-ba4365383cb6e7ff.elb.us-east-1.amazonaws.com:8000/")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json() # Return the JSON response from the private API
    except requests.exceptions.RequestException as e:  # Catch network errors
        logger.error(f"Error fetching data from private API: {e}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}") # Return a 500 with details
    except Exception as e: # Catch other exceptions during processing
        tb_str = traceback.format_exc() # Capture traceback
        logger.error(f"An unexpected error occurred: {e}\n{tb_str}") # Log error and traceback
        raise HTTPException(status_code=500, detail="An unexpected error occurred.") # Return 500


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)