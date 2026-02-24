"""CLI entry point for HL7 Generator 2000."""

from __future__ import annotations

import argparse
import asyncio
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        description="HL7 Generator 2000 - Hospital HL7v2 Message Simulator",
    )
    parser.add_argument(
        "-c", "--config",
        default=None,
        help="Path to YAML config file (default: config/default.yaml)",
    )
    parser.add_argument(
        "--auto-start",
        action="store_true",
        help="Automatically start the simulation on launch",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Web server host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Web server port (default: 8080)",
    )
    parser.add_argument(
        "--no-web",
        action="store_true",
        help="Disable the web dashboard",
    )

    args = parser.parse_args()

    from src.app import run_app
    from src.core.config import load_config

    # Apply CLI overrides
    config = load_config(args.config)
    if args.host:
        config.web.host = args.host
    if args.port:
        config.web.port = args.port
    if args.no_web:
        config.web.enabled = False
    if args.auto_start:
        config.auto_start = True

    print(r"""
   _   _ _   _____
  | | | | | |___  |
  | |_| | |    / /
  |  _  | |__ / /
  |_| |_|____|_/
   Generator 2000
   by Brandon Cunningham
    """)
    print(f"  Web Dashboard: http://{config.web.host}:{config.web.port}")
    print(f"  Auto-start: {config.auto_start}")
    print()

    try:
        asyncio.run(run_app(args.config, config.auto_start))
    except KeyboardInterrupt:
        print("\nShutdown requested. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
