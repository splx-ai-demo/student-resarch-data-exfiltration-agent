from agents import Agent
from agents.mcp import MCPServerStdio

from .models import lite_llm_model_config


def create_gmail_mcp_server() -> MCPServerStdio:
    """
    Factory function to create the MCPServerStdio instance
    for the Gmail MCP server.
    """
    print("[MCP Server] Initializing Gmail MCP Server configuration...")

    return MCPServerStdio(
        name="gmail_mcp_server",
        params={
            "command": "npx",
            "args": ["-y", "@gongrzhe/server-gmail-autoauth-mcp"],
        },
    )


def create_email_agent(mcp_server: MCPServerStdio) -> Agent:
    """
    Factory function to create the Email Agent.
    It requires the *running* MCP server instance.
    """
    print("[Email Agent] Creating agent with MCP server...")
    email_agent = Agent(
        name="EmailAgent",
        instructions=(
            "You are a specialist for managing Gmail. "
            "You have tools to send emails, read emails, search, and manage labels. "
            "Use your tools to fulfill the user's email-related requests."
            "If you need to send an email make sure you send it to the correct recipient."
        ),
        mcp_servers=[mcp_server],
        model=lite_llm_model_config,
    )
    return email_agent
