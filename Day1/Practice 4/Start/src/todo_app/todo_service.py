from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class Todo:
    id: int
    title: str
    done: bool = False


class TodoService:
    """In-memory todo service."""

    def __init__(self) -> None:
        self._todos: Dict[int, Todo] = {}
        self._next_id = 1

    def add(self, title: str) -> Todo:
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")

        todo = Todo(id=self._next_id, title=title)
        self._todos[todo.id] = todo
        self._next_id += 1
        return todo

    def list(self) -> List[Todo]:
        return sorted(self._todos.values(), key=lambda item: item.id)

    def toggle(self, todo_id: int) -> Todo:
        todo = self._todos.get(todo_id)
        if todo is None:
            raise KeyError("todo not found")

        todo.done = not todo.done
        return todo

    def delete(self, todo_id: int) -> None:
        if todo_id not in self._todos:
            raise KeyError("todo not found")
        del self._todos[todo_id]


def todo_to_dict(todo: Todo) -> dict:
    return asdict(todo)
