class PDFIngestorError(Exception):
    """Base exception for all PDF ingestion failures."""


class InvalidPasswordError(PDFIngestorError):
    """Raised when the PDF could not be decrypted with any available password."""


class BufferSizeExceededError(PDFIngestorError):
    """Raised when the input file or decrypted output exceeds the configured memory limit."""


class CorruptPDFError(PDFIngestorError):
    """Raised when the PDF structure cannot be parsed."""
