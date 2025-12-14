"""Backward-compatible wrapper importing data loaders."""

from .data_loader import load_majors_data, load_context

__all__ = ["load_majors_data", "load_context"]
