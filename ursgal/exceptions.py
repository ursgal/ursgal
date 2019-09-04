#!/usr/bin/env python3


class UrsgalError(Exception):
    """Base class for all ursgal errors"""

    pass


class EmptyCsvUrsgalError(UrsgalError):
    """Input CSV to ursgal node is empty"""

    pass
