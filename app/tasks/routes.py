from fastapi import APIRouter

router = APIRouter(tags=["tasks"])

@router.get("/tasks")
async def get_tasks():
    return ["siktir", "sikim"]

@router.get("/tasks/{task_id}")
async def get_tasks(task_id: int):
    return ["siktir", "sikim"]