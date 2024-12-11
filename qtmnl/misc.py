import codecs

import mnllib

CODEC_ERROR_HANDLER_KEEP_LITERAL = "qtmnl:keepliteral"


def keepliteral_errors(error: UnicodeError) -> tuple[str | bytes, int]:
    if isinstance(error, UnicodeEncodeError):
        return bytes([ord(x) for x in error.object[error.start : error.end]]), error.end
    if isinstance(error, UnicodeDecodeError):
        return (
            "".join([chr(x) for x in error.object[error.start : error.end]]),
            error.end,
        )
    if isinstance(error, UnicodeTranslateError):
        return error.object[error.start : error.end], error.end
    raise error


codecs.register_error(CODEC_ERROR_HANDLER_KEEP_LITERAL, keepliteral_errors)


def decompile_text(value: bytes) -> str:
    return (
        repr(value.decode(mnllib.MNL_ENCODING, errors="backslashreplace"))
        .replace("\xff", "\\xff")
        .replace("\\xff\\x00", "\n")
    )[1:-1]


def compile_text(value: str) -> bytes:
    return (
        value.replace("\n", "\\xff\\x00")
        .encode("raw_unicode_escape")
        .decode("unicode_escape")
        .encode(mnllib.MNL_ENCODING, errors=CODEC_ERROR_HANDLER_KEEP_LITERAL)
    )
