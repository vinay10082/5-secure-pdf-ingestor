import argparse
import logging
import sys

from pdf_ingestor import PDFIngestorError, SecurePDFIngestor
from pdf_ingestor.config import load_config


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Securely decrypt a password-protected PDF directly into memory "
        "(no intermediate disk writes).",
    )
    parser.add_argument("file", help="Path to the password-protected PDF file")
    parser.add_argument(
        "-p",
        "--password",
        help="Password for the PDF. Falls back to FALLBACK_DECRYPTION_PASSWORD "
        "from .env if omitted or incorrect.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional path to write the decrypted PDF. By default nothing is "
        "written to disk; pass this only if you explicitly want a decrypted copy.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose (debug) logging"
    )
    return parser


def main(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger("main")

    try:
        config = load_config()
    except ValueError as exc:
        logger.error("Invalid configuration: %s", exc)
        return 1

    ingestor = SecurePDFIngestor(config)

    try:
        buffer = ingestor.ingest(args.file, password=args.password)
    except FileNotFoundError as exc:
        logger.error(str(exc))
        return 1
    except PDFIngestorError as exc:
        logger.error("Ingestion failed: %s", exc)
        return 1

    size = buffer.getbuffer().nbytes
    print(f"Decrypted '{args.file}' into an in-memory buffer ({size} bytes).")

    if args.output:
        with open(args.output, "wb") as f:
            f.write(buffer.getvalue())
        print(f"Decrypted content written to '{args.output}' (explicit --output requested).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
