from fastapi import FastAPI

app = FastAPI(title="Campus PDF Q&A Bot")

@app.get("/")
def health():
    return {"status": "ok", "service": "campus-pdf-qa-bot"}
