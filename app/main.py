from fastapi import FastAPI, HTTPException
import requests
import os


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI, testing private subnet"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/fetch-private-data")
async def fetch_private_data():
    try:
        # Make request to the private API
        response = requests.get("http://fastapi-private-nlb-ba4365383cb6e7ff.elb.us-east-1.amazonaws.com:8000/health")
        response.raise_for_status()  # Raise exception for non-200 status codes
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 