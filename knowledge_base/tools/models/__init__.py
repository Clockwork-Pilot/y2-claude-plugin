"""Models for knowledge base tools."""

from .doc_model import Doc

# Registry mapping model type string to model class
MODEL_REGISTRY = {
    "Doc": Doc,
    # Add future models here:
    # "Task": Task,
}

__all__ = ["Doc", "MODEL_REGISTRY"]
