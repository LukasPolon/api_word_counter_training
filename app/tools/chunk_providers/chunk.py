from dataclasses import dataclass


@dataclass(slots=True)
class Chunk:
    """Data chunk;
    consists of fields:
    data: required, holds raw, unprocessed data line
        from file, URL, or string argument
    data_preprocessed: optional; modified version of raw data
    """

    data: str
    data_preprocessed: list[str] | None = None
