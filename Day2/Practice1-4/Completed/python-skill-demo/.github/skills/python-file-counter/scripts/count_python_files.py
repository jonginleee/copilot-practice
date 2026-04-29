from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileStats:
    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0


EXCLUDED_DIR_NAMES = {
    ".git",
    ".github",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIR_NAMES for part in path.parts)


def collect_python_files(root: Path) -> list[Path]:
    python_files: list[Path] = []
    for path in root.rglob("*.py"):
        if should_skip(path.relative_to(root)):
            continue
        python_files.append(path)
    return sorted(python_files)


def get_file_stats(path: Path) -> FileStats:
    stats = FileStats()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stats.total_lines += 1
            stripped = line.strip()
            if not stripped:
                stats.blank_lines += 1
            elif stripped.startswith("#"):
                stats.comment_lines += 1
    return stats


def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == ".github":
            return parent.parent
    raise RuntimeError("Could not determine project root from skill script location")


def main() -> None:
    project_root = find_project_root()
    python_files = collect_python_files(project_root)

    aggregate = FileStats()
    for path in python_files:
        file_stats = get_file_stats(path)
        aggregate.total_lines += file_stats.total_lines
        aggregate.blank_lines += file_stats.blank_lines
        aggregate.comment_lines += file_stats.comment_lines

    print(f"Project root: {project_root}")
    print(f"Python files: {len(python_files)}")
    print(f"Total lines: {aggregate.total_lines}")
    print(f"Blank lines: {aggregate.blank_lines}")
    print(f"Comment lines: {aggregate.comment_lines}")


if __name__ == "__main__":
    main()