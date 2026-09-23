import io
import logging
import os
from typing import List, Optional

import pikepdf

from .config import Config, load_config
from .exceptions import BufferSizeExceededError, CorruptPDFError, InvalidPasswordError

logger = logging.getLogger(__name__)


class SecurePDFIngestor:
    """Decrypts password-protected PDFs directly into an in-memory buffer.

    The decrypted content never touches disk: pikepdf writes the decrypted
    document straight into an io.BytesIO stream.
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or load_config()

    def _max_bytes(self) -> int:
        return int(self.config.max_memory_buffer_size_mb * 1024 * 1024)

    def _check_size(self, size_bytes: int, stage: str) -> None:
        max_bytes = self._max_bytes()
        if size_bytes > max_bytes:
            raise BufferSizeExceededError(
                f"{stage} size ({size_bytes} bytes) exceeds the configured limit of "
                f"{max_bytes} bytes ({self.config.max_memory_buffer_size_mb} MB)"
            )

    def _candidate_passwords(self, password: Optional[str]) -> List[str]:
        candidates: List[str] = []
        if password:
            candidates.append(password)
        candidates.append("")  # unencrypted PDFs / empty user password
        if self.config.fallback_decryption_password:
            candidates.append(self.config.fallback_decryption_password)
        return candidates

    def ingest(self, file_path: str, password: Optional[str] = None) -> io.BytesIO:
        """Decrypt `file_path` and return its contents as an in-memory BytesIO stream."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No such file: {file_path}")

        input_size = os.path.getsize(file_path)
        self._check_size(input_size, "Input file")

        pdf = None
        last_error: Optional[Exception] = None
        for candidate in self._candidate_passwords(password):
            try:
                pdf = pikepdf.open(file_path, password=candidate)
                break
            except pikepdf.PasswordError as exc:
                last_error = exc
                continue
            except pikepdf.PdfError as exc:
                raise CorruptPDFError(f"Failed to parse PDF '{file_path}': {exc}") from exc

        if pdf is None:
            raise InvalidPasswordError(
                f"Could not decrypt '{file_path}' with the supplied password or the "
                "configured fallback password"
            ) from last_error

        buffer = io.BytesIO()
        try:
            pdf.save(buffer)
        finally:
            pdf.close()

        output_size = buffer.getbuffer().nbytes
        self._check_size(output_size, "Decrypted output")

        buffer.seek(0)
        logger.info("Successfully ingested '%s' (%d bytes) into memory", file_path, output_size)
        return buffer
