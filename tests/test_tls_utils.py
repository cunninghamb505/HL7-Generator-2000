"""Tests for TLS utility functions."""

import ssl

from src.core.config import DestinationConfig
from src.transport.tls_utils import build_ssl_context


def test_build_ssl_context_disabled():
    config = DestinationConfig(tls_enabled=False)
    ctx = build_ssl_context(config)
    assert ctx is None


def test_build_ssl_context_client():
    config = DestinationConfig(tls_enabled=True, tls_verify=False)
    ctx = build_ssl_context(config, server_side=False)
    assert ctx is not None
    assert isinstance(ctx, ssl.SSLContext)
    assert ctx.check_hostname is False
    assert ctx.verify_mode == ssl.CERT_NONE


def test_build_ssl_context_server():
    config = DestinationConfig(tls_enabled=True)
    ctx = build_ssl_context(config, server_side=True)
    assert ctx is not None
    assert isinstance(ctx, ssl.SSLContext)


def test_mllp_client_tls_property():
    from src.transport.mllp_client import MLLPClient

    client_no_tls = MLLPClient()
    assert client_no_tls.tls_enabled is False

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    client_tls = MLLPClient(ssl_context=ctx)
    assert client_tls.tls_enabled is True


def test_mllp_server_tls_property():
    from src.transport.mllp_server import MLLPServer

    server_no_tls = MLLPServer()
    assert server_no_tls.tls_enabled is False

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_tls = MLLPServer(ssl_context=ctx)
    assert server_tls.tls_enabled is True


def test_destination_config_tls_fields():
    config = DestinationConfig(
        name="test",
        type="mllp",
        tls_enabled=True,
        tls_cert="/path/to/cert.pem",
        tls_key="/path/to/key.pem",
        tls_ca="/path/to/ca.pem",
        tls_verify=True,
    )
    assert config.tls_enabled is True
    assert config.tls_cert == "/path/to/cert.pem"
    assert config.tls_key == "/path/to/key.pem"
    assert config.tls_ca == "/path/to/ca.pem"
    assert config.tls_verify is True
