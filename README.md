# Password Protected File Ingestor

## Description
A secure ingestion pipeline designed to decrypt protected PDF files directly into volatile memory.

## Architecture Overview
Cryptographic decryption via `pikepdf`, buffering output securely into an `io.BytesIO` stream to prevent disk writes.

## Prerequisites
* Python 3.11+
* `pikepdf`
* `python-dotenv`

## Environment Variables
Configured via `.env` (see `.env.example`):
* `MAX_MEMORY_BUFFER_SIZE_MB` – maximum allowed size, in MB, for both the input PDF and the decrypted in-memory buffer.
* `FALLBACK_DECRYPTION_PASSWORD` – optional password tried automatically if no password is supplied, or the supplied one fails.

## Installation
```
pip install -r requirements.txt
cp .env.example .env   # then edit values as needed
```

## Quick Start & Usage
`main.py` is the entry point. Pass a protected file path and password to decrypt it directly into an in-memory buffer:

```
python main.py path/to/protected.pdf -p yourpassword
```

Options:
* `-p, --password` – password for the PDF (falls back to `FALLBACK_DECRYPTION_PASSWORD` if omitted or incorrect)
* `-o, --output` – optional path to explicitly write the decrypted PDF to disk (by default nothing is written)
* `-v, --verbose` – enable verbose (debug) logging

The decrypted content is only ever materialized in memory (`io.BytesIO`) unless `--output` is explicitly passed.

Programmatic usage:
```python
from pdf_ingestor import SecurePDFIngestor

ingestor = SecurePDFIngestor()
buffer = ingestor.ingest("path/to/protected.pdf", password="yourpassword")
# buffer is an io.BytesIO containing the decrypted PDF bytes
```
