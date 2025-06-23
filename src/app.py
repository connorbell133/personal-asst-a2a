"""
This module contains the FastAPI application for the GitHub Helper project.

Args:
    None

Returns:
    app: The FastAPI application for the GitHub Helper project.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="GitHub Helper",
    description="A FastAPI application for GitHub integration and automation",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Return a welcome message indicating that the GitHub Helper application is running.

    Returns:
        dict: A JSON object with a greeting message.
    """
    return {"message": "Hello from GitHub Helper!"}


@app.get("/health")
async def health_check():
    """
    Return a JSON object indicating the application's health status.

    Returns:
        dict: A dictionary with the key "status" set to "healthy".
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
