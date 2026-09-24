from typing import *
# from streamlit_option_menu import option_menu
import asyncio
from .messages import *
from .thirdpart import *


__version__ = "1.1.13.post1"


__all__ = [
    "ChatBox",
    "Markdown",
    "Image",
    "Audio",
    "Video",
    "Json",
    "OutputElement",
    "FakeLLM",
    "FakeAgent",
]


def run_async(cor) -> Any:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(cor)
    return loop.run_until_complete(cor)
