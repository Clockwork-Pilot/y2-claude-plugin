"""Shared knowledge models for knowledge base and task lifecycle."""

from .base_model import RenderableModel
from .doc_model import Doc, Opts

# Registry mapping model type string to model class
MODEL_REGISTRY = {
    "Doc": Doc,
    # Add future models here:
    # "Task": Task,
    # "Iteration": Iteration,
}

__all__ = ["RenderableModel", "Doc", "Opts", "MODEL_REGISTRY"]
