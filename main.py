import hashlib

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
    Return the first 16 lowercase hex characters of:

    SHA-256("${challenge}:${normalizedEmail}")

    The challenge is read from the HTTP request header,
    not from the tool arguments.
    """

    # Get the underlying HTTP request.
    request = ctx.request_context.request

    # Read the challenge sent by the grader.
    challenge = request.headers.get(
        "x-exam-challenge"
    )

    if not challenge:
        raise ValueError(
            "Missing X-Exam-Challenge header."
        )

    # Normalize registered exam email.
    normalized_email = (
        REGISTERED_EMAIL
        .strip()
        .lower()
    )

    # Construct exact string:
    # challenge:normalizedEmail
    payload = (
        f"{challenge}:{normalized_email}"
    )

    # SHA-256 and first 16 lowercase hex characters.
    digest = hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()

    return digest[:16]


# ============================================================
# MCP STREAMABLE HTTP APPLICATION
# ============================================================

app = mcp.http_app(
    path="/mcp"
)