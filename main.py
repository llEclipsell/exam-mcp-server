import hashlib
import os

from fastapi import FastAPI, Request
from fastmcp import FastMCP, Context


# ============================================================
# CONFIGURATION
# ============================================================

REGISTERED_EMAIL = "24f2001120@ds.study.iitm.ac.in"


# ============================================================
# MCP SERVER
# ============================================================

mcp = FastMCP(
    name="Exam Challenge MCP Server"
)


@mcp.tool()
async def solve_challenge(
    ctx: Context,
) -> str:
    """
    Solve the current exam challenge.

    The challenge is intentionally NOT accepted as a tool
    argument. It is read from the HTTP request headers.
    """

    # --------------------------------------------------------
    # Get the underlying HTTP request.
    # --------------------------------------------------------

    request: Request = ctx.request_context.request


    # --------------------------------------------------------
    # Read the challenge header.
    # --------------------------------------------------------

    challenge = request.headers.get(
        "x-exam-challenge"
    )


    if not challenge:
        raise ValueError(
            "Missing X-Exam-Challenge header."
        )


    # --------------------------------------------------------
    # Normalize registered email exactly as specified.
    # --------------------------------------------------------

    normalized_email = (
        REGISTERED_EMAIL
        .strip()
        .lower()
    )


    # --------------------------------------------------------
    # Compute:
    #
    # SHA-256("${challenge}:${normalizedEmail}")
    #
    # Then return first 16 lowercase hex characters.
    # --------------------------------------------------------

    payload = (
        f"{challenge}:{normalized_email}"
    )


    digest = hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()


    return digest[:16]


# ============================================================
# ASGI APP
# ============================================================

app = mcp.http_app(
    path="/mcp"
)


# ============================================================
# OPTIONAL HEALTH ENDPOINT
# ============================================================

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Exam Challenge MCP Server",
        "mcp_endpoint": "/mcp",
    }