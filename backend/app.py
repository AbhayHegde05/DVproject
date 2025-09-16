from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import datasets, insights, recommend

app = FastAPI(title="Karnataka Environmental API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(datasets.router)
app.include_router(insights.router)
app.include_router(recommend.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Karnataka Environmental API running"}
