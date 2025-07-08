"""
This module contains the logger for the project.

Args:
    None

Returns:
    logger: The logger for the project.
"""

import logging

# ---------- Logfire instrumentation ----------
# Logfire provides structured logging, tracing and metrics built on top of
# OpenTelemetry. We configure it once here so every import of this module
# automatically enables Logfire for the whole application.

# End-users can control where the data is sent by setting LOGFIRE_TOKEN (cloud)
# or LOGFIRE_SEND=false (disable). For local development, calling configure()
# without arguments is enough – data will be printed to stdout.

import logfire

# The Logfire SDK throws LogfireConfigError if no credentials are found and
# we're attempting to send data to the hosted service. We want the application
# to *keep running* in that situation and simply log locally instead.


# Avoid re-configuring Logfire if another part of the code already did so.
if not getattr(logfire, "_configured", False):  # type: ignore[attr-defined]
    logfire.configure(send_to_logfire="if-token-present")

# Attach Logfire as a standard logging handler so that any module still using
# the stdlib logging API automatically streams to Logfire.
root_logger = logging.getLogger()

if not any(isinstance(h, logfire.LogfireLoggingHandler) for h in root_logger.handlers):
    root_logger.addHandler(logfire.LogfireLoggingHandler())

# Ensure we capture verbose output for debugging OAuth/MCP issues.
root_logger.setLevel(logging.DEBUG)

# Convenience logger for modules to import.
logger = logging.getLogger("ai-asst")
