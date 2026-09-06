import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        log_level="info",
        timeout_keep_alive=5
    )
