from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import random
import time
from typing import Dict

app = FastAPI(
    title="OpenGradient Demo",
    description="Simulated execution layer with GPU + TEE nodes",
    version="1.0.0"
)

# Enable CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class JobRequest(BaseModel):
    input: str

# Simulated GPU node
def gpu_node(task: str, node_name: str) -> str:
    time.sleep(1)  # simulate processing delay
    return f"GPU processed: {task} on {node_name}"

# Simulated TEE node
def tee_node(result: str) -> Dict[str, str | bool]:
    verification_hash: str = hashlib.sha256(result.encode()).hexdigest()
    return {
        "verified": True,
        "verification_hash": verification_hash
    }

# Distributed compute
def distributed_compute(task: str) -> str:
    gpu_nodes: list[str] = ["GPU-Node-1", "GPU-Node-2", "GPU-Node-3"]
    chosen_node: str = random.choice(gpu_nodes)
    return gpu_node(task, chosen_node)

# API Endpoints
@app.get("/")
def home() -> Dict[str, str]:
    return {
        "message": "Welcome to OpenGradient Demo 🚀",
        "info": "This simulates distributed GPU + TEE execution."
    }

@app.post("/submit-job")
def run_job(request: JobRequest) -> Dict[str, str | bool]:
    gpu_result: str = distributed_compute(request.input)
    verification: Dict[str, str | bool] = tee_node(gpu_result)
    return {
        "input": request.input,
        "result": gpu_result,
        "verified": verification["verified"],
        "verification_hash": verification["verification_hash"]
    }
