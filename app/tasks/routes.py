from fastapi import APIRouter, Path, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List
from app.tasks.schemas import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from app.tasks.models import TaskModel
from app.users.models import UserModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.jwt_auth import get_authenticated_user

router = APIRouter(tags=["tasks"])


# GET ALL TASKS
@router.get("/tasks", response_model=List[TaskResponseSchema])
async def get_tasks(
    completed: bool = Query(None, description="filters based on is_complete field"),
    limit: int = Query(10, gt=0, le=15),
    offset: int = Query(
        0, ge=0, description="the starting point for retreving the data batch"
    ),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    q = db.query(TaskModel).filter_by(user_id=user.id)
    if completed is not None:
        q = q.filter_by(is_complete=completed)
    return q.limit(limit).offset(offset).all()


# GET SINGLE TASK
@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def get_task_by_id(
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    result = db.query(TaskModel).filter_by(id=task_id, user_id=user.id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


# UPDATE TASK
@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task_by_id(
    request: TaskUpdateSchema,
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task_obj = db.query(TaskModel).filter_by(id=task_id, user_id=user.id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj, field, value)
    db.commit()
    db.refresh(task_obj)
    return task_obj


# DELETE TASK
@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task_by_id(
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task_obj = db.query(TaskModel).filter_by(id=task_id, user_id=user.id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()


# CREATE TASK
@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task(
    request: TaskCreateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    data = request.model_dump()
    data.update({"user_id": user.id})
    task_obj = TaskModel(**data)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


# {
#     page:
#     total_page:
#     current_page:
#     next_page:
#     prev_page:
#     results: []
# }
