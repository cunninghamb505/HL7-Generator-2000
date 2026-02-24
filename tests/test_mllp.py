"""Tests for MLLP protocol framing."""

from src.transport.mllp_protocol import extract_messages, unwrap_mllp, wrap_mllp


def test_wrap_mllp():
    msg = "MSH|^~\\&|test"
    wrapped = wrap_mllp(msg)
    assert wrapped == b"\x0bMSH|^~\\&|test\x1c\x0d"


def test_unwrap_mllp():
    data = b"\x0bMSH|^~\\&|test\x1c\x0d"
    result = unwrap_mllp(data)
    assert result == "MSH|^~\\&|test"


def test_unwrap_no_framing():
    data = b"MSH|^~\\&|test"
    result = unwrap_mllp(data)
    assert result == "MSH|^~\\&|test"


def test_extract_single_message():
    msg = "MSH|^~\\&|test"
    data = b"\x0b" + msg.encode() + b"\x1c\x0d"
    messages, remaining = extract_messages(data)
    assert len(messages) == 1
    assert messages[0] == msg
    assert remaining == b""


def test_extract_multiple_messages():
    msg1 = "MSH|^~\\&|msg1"
    msg2 = "MSH|^~\\&|msg2"
    data = (
        b"\x0b" + msg1.encode() + b"\x1c\x0d"
        + b"\x0b" + msg2.encode() + b"\x1c\x0d"
    )
    messages, remaining = extract_messages(data)
    assert len(messages) == 2
    assert messages[0] == msg1
    assert messages[1] == msg2


def test_extract_partial_message():
    msg = "MSH|^~\\&|partial"
    data = b"\x0b" + msg.encode()  # No end block
    messages, remaining = extract_messages(data)
    assert len(messages) == 0
    assert len(remaining) > 0
