"""Shared knowledge models for knowledge base and task lifecycle."""

from .base_model import RenderableModel
from .doc_model import Doc, Opts
from .task_model import Task, Iteration, CodeStats, TaskTestMetrics

# Registry mapping model type string to model class.
# Add all RenderableModel subclasses that can be root nodes in knowledge documents.
# These are used by render.py for polymorphic instantiation and rendering.
MODEL_REGISTRY = {
    "Doc": Doc,
    "Task": Task,
    "Iteration": Iteration,
}

__all__ = [
    "RenderableModel",
    "Doc",
    "Opts",
    "Task",
    "Iteration",
    "CodeStats",
    "TaskTestMetrics",
    "MODEL_REGISTRY",
]
