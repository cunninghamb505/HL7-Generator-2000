"""TLS/SSL context builder for MLLP connections."""

from __future__ import annotations

import ssl
from pathlib import Path

from src.core.config import DestinationConfig


def build_ssl_context(config: DestinationConfig, server_side: bool = False) -> ssl.SSLContext | None:
    """Build an SSLContext from destination config, or return None if TLS is disabled."""
    if not config.tls_enabled:
        return None

    if server_side:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    else:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # Load certificate + private key if provided
    if config.tls_cert and config.tls_key:
        ctx.load_cert_chain(
            certfile=str(Path(config.tls_cert)),
            keyfile=str(Path(config.tls_key)),
        )
    elif config.tls_cert:
        ctx.load_cert_chain(certfile=str(Path(config.tls_cert)))

    # Load CA bundle for verification
    if config.tls_ca:
        ctx.load_verify_locations(cafile=str(Path(config.tls_ca)))
    elif not server_side:
        ctx.load_default_certs()

    if not config.tls_verify and not server_side:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    return ctx
