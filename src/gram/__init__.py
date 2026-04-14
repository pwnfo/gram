import importlib.metadata as md

__author__ = "Ryan R. <pwnfo@proton.me>"
__description__ = "Simple and efficient data encoding/decoding utility."
__url__ = "https://github.com/pwnfo/gram"
try:
    __version__ = md.version("gram-encoder")
except:
    __version__ = "0.0.0-dev"
