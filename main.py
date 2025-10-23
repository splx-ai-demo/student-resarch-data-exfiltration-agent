from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

from agents import Runner, SQLiteSession, set_trace_processors
from agents.mcp import MCPServerStdio
from langsmith.wrappers import OpenAIAgentsTracingProcessor

from agent.email_agent import create_email_agent, create_gmail_mcp_server
from agent.employee_agent import employee_agent
from agent.personal_assistant import create_personal_assistant
from agent.web_agent import web_scan_agent
from models import ChatRequest, ChatResponse

# --- Global State ---
app_state = {}

CONVERSATION_DB = "conversations.db"

# --- Lifespan Management (Startup & Shutdown) ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's lifespan.
    Handles startup and shutdown of the Gmail MCP server.
    """
    print("--- Application Startup ---")

    set_trace_processors([OpenAIAgentsTracingProcessor()])
    print("[Lifespan] OpenAI tracing disabled for Azure client.")

    # 1. Initialize the Gmail MCP Server
    print("[Lifespan] Initializing Gmail MCP Server...")
    gmail_server: MCPServerStdio = create_gmail_mcp_server()

    # 2. Start the MCP server (this runs `npx ...` in a subprocess)
    try:
        await gmail_server.__aenter__()
        print("[Lifespan] Gmail MCP Server process started.")
        app_state["gmail_server"] = gmail_server
    except Exception as e:
        print(f"[Lifespan] FATAL: Failed to start Gmail MCP Server: {e}")
        raise

    # 3. Create the Email Agent (which needs the running server)
    email_agent = create_email_agent(gmail_server)

    # 4. Create the Personal Assistant (which needs all sub-agents)
    # The other agents are simple and don't need startup logic.
    personal_assistant = create_personal_assistant(
        web_agent=web_scan_agent, sql_agent=employee_agent, mail_agent=email_agent
    )
    app_state["main_agent"] = personal_assistant

    print("--- Application Ready ---")

    # 'yield' passes control back to FastAPI to run the server
    yield

    # --- Application Shutdown ---
    print("--- Application Shutdown ---")

    # 1. Get the running server instance
    server_to_stop: MCPServerStdio = app_state.get("gmail_server")

    # 2. Shut it down
    if server_to_stop:
        print("[Lifespan] Shutting down Gmail MCP Server...")
        try:
            await server_to_stop.__aexit__(None, None, None)
            print("[Lifespan] Gmail MCP Server process stopped.")
        except Exception as e:
            print(f"[Lifespan] Error stopping Gmail MCP Server: {e}")


# --- FastAPI App ---
app = FastAPI(title="Vulnerable Agent Workflow API", lifespan=lifespan)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint.
    Maintains conversation history using the provided session_id.
    """
    print(f"\n--- New Request (Session: {request.session_id}) ---")
    print(f"User: {request.message}")

    # 1. Get the main agent from our app state
    agent = app_state.get("main_agent")
    if not agent:
        raise HTTPException(status_code=503, detail="Agent is not initialized.")

    # 2. Create/load the conversation session
    # This automatically handles loading and saving history
    session = SQLiteSession(session_id=request.session_id, db_path=CONVERSATION_DB)

    try:
        # 3. Run the agent
        # The Runner handles the entire multi-step agent loop
        result = await Runner.run(
            starting_agent=agent, input=request.message, session=session
        )

        reply = str(result.final_output)
        print(f"Agent: {reply}")

        # 4. Return the response
        return ChatResponse(reply=reply, session_id=request.session_id)

    except Exception as e:
        print(f"[Chat Endpoint] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"status": "Agent API is running."}


# --- Main execution ---
if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
