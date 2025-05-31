"""Top-level package for comfy_handyutils."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """Cyclica Bin"""
__email__ = "akza07@outlook.com"
__version__ = "0.0.1"

from .src.comfy_handyutils.nodes import NODE_CLASS_MAPPINGS
from .src.comfy_handyutils.nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
