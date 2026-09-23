# Password Protected File Ingestor

## Description
A secure ingestion pipeline designed to decrypt protected PDF files directly into volatile memory.

## Architecture Overview
Cryptographic decryption via `pikepdf`, buffering output securely into an `io.BytesIO` stream to prevent disk writes.

## Prerequisites
* Python 3.11+
* `pikepdf`

## Environment Variables
* `MAX_MEMORY_BUFFER_SIZE_MB`
* `FALLBACK_DECRYPTION_PASSWORD`

## Quick Start & Usage
Pass a protected file path and password to the ingestor to receive a readable byte stream object.

## Testing & CI
Includes mock encrypted PDFs to validate decryption failure handling, buffer overflow protections, and successful memory reads.
