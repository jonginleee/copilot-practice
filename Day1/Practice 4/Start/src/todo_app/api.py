from __future__ import annotations

from typing import List

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

from .todo_service import TodoService, todo_to_dict

app = FastAPI(title="Todo API")
service = TodoService()


class CreateTodoRequest(BaseModel):
    title: str = Field(min_length=1)


class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool


@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def add_todo(payload: CreateTodoRequest) -> TodoResponse:
    try:
        todo = service.add(payload.title)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return TodoResponse(**todo_to_dict(todo))


@app.get("/todos", response_model=List[TodoResponse])
def list_todos() -> List[TodoResponse]:
    return [TodoResponse(**todo_to_dict(todo)) for todo in service.list()]


@app.patch("/todos/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo(todo_id: int) -> TodoResponse:
    try:
        todo = service.toggle(todo_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="todo not found") from exc
    return TodoResponse(**todo_to_dict(todo))


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_todo(todo_id: int) -> Response:
    try:
        service.delete(todo_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="todo not found") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
