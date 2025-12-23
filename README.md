# Student Data Exfiltration Agent

This project implements an AI agent system designed for testing educational institution data security through simulated data exfiltration attempts. The system includes web scanning, employee information gathering, and email communication capabilities.

## Project Overview

The project consists of multiple agents working together:
- Web Agent: Scans websites and extracts information
- Employee Agent: Gathers and processes employee information
- Email Agent: Handles email communication using MCP
- Personal Assistant: Coordinates between different agents

## Prerequisites

- Node.js and npm (for MCP server)
- A dedicated Google account for the email agent
- uv (for Python virtual environment and dependency management) installed
- LangSmith account for agent monitoring
- Tavily API key for web search capabilities
- Litellm API access for language model interactions

## Initial Setup

### 0. API Keys and Environment Setup
- Create a `.env` file in your project root with `.env.example` as a template:

1. LangSmith Setup:
   - Go to [LangSmith platform](https://smith.langchain.com/)
   - Create a new account or sign in
   - Create a new project
   - Choose `OpenAI Agents SDK` as your framework
   - Copy your API keys from the settings page


2. Tavily API Setup:
   - Go to [Tavily](https://tavily.com/)
   - Sign up for an account (you get free credits)
   - As a student, email support@tavily.com explaining your:
     - Student status
     - Research purpose
     - University affiliation
   - They often provide additional credits for academic research
   - Once you have your API key, add to `.env`:
  

3. Litellm API Setup:
   - Add the given credentials to your `.env` file:
     ```
     BASE_URL="http://your-litellm-instance-url/"
     API_KEY="your-litellm-api-key"
     MODEL="gpt-5-mini"
     ```
    - Available model IDs (use one of these for the `MODEL` value):
       - `gpt-5-mini`
       - `gpt-4o`
       - `eu.meta.llama3-2-3b-instruct-v1:0`
       - `eu.anthropic.claude-sonnet-4-5-20250929-v1:0`
       - `gemini/gemini-2.5-flash`
       - `gemini/gemini-2.5-pro`
       - `bedrock/amazon.nova-2-lite-v1:0`
       - `gpt-4o-mini`


## Initial Setup

### 1. Set up Python Virtual Environment

```bash
# Create a new virtual environment using uv
uv venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate

# Install project dependencies
uv sync
```

### 2. Database Setup

1. Create a SQLite database for the project
2. Run the database setup script:
```bash
python setup_database.py
```

### 3. Gmail MCP Server Setup

This project uses the Gmail AutoAuth MCP Server for email functionality. Follow these steps carefully:

#### Prerequisites Setup
1. Install Node.js and npm from [nodejs.org](https://nodejs.org)
2. Verify installation:
```bash
node -v
npm -v
```
3. Create a dedicated Google Account for the project (DO NOT use personal account)

#### Google Cloud Project Configuration
1. Log in to [Google Cloud Console](https://console.cloud.google.com) with your dedicated account
2. Create a new project:
   - Click `Select project` button → `NEW PROJECT`
   - Name it (e.g., "AI Agent Email Research")
   - Click `CREATE`

#### Enable Gmail API
1. In Google Cloud Console, search for `Gmail API`
2. Click `ENABLE` to activate the API

#### OAuth 2.0 Credentials Setup
1. Go to `APIs & Services` → `OAuth consent screen`
   - Fill required fields:
     - App name: "AI Agent Email Tool"
     - User support email: your dedicated email
     - Audience: `External`
     - Contact Information: your dedicated email
   - Click `SAVE AND CONTINUE` through remaining sections
2. Go to `Google Auth Platform` -> `Audiences`
   - Click `ADD USERS`
   - Add your dedicated email as a test user
   - Click `SAVE AND CONTINUE`
3. Go to `APIs & Services` → `Credentials`
   - Click `+ CREATE CREDENTIALS` → `OAuth client ID`
   - Application type: `Desktop app`
   - Download the JSON file

#### Local Setup
1. Rename downloaded JSON to `gcp-oauth.keys.json`
2. Create MCP directory and move file:
```bash
mkdir -p ~/.gmail-mcp
mv /path/to/your/gcp-oauth.keys.json ~/.gmail-mcp/
```

#### Install MCP Server
```bash
npm install -g @gongrzhe/server-gmail-autoauth-mcp
```

#### Authenticate (One-Time Setup)
1. Run authentication:
```bash
npx @gongrzhe/server-gmail-autoauth-mcp auth
```
2. Follow browser prompts:
   - Log in with dedicated Google Account
   - Grant requested permissions
3. Verify setup:
   - Check for `credentials.json` in `~/.gmail-mcp/`

## Running the Application

1. Ensure virtual environment is activated:
```bash
source venv/bin/activate 
```

2. Start the main application:
```bash
python main.py
```

### API example: chat endpoint

You can interact with the running agent via a simple HTTP POST to the `/chat` endpoint. Example using curl:

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
       -H "Content-Type: application/json" \
       -d '{
                "message": "Who are you?",
                "session_id": "test-123"
             }'
```

Fields explained:
- `message` (string): The user's input text or prompt you want the agent to respond to. This can be a question, instruction, or any text.
- `session_id` (string): An identifier for the conversation session. Use the same `session_id` for messages that belong to the same conversation so the agent can maintain context between requests.

Notes:
- Make sure the server is running on `127.0.0.1:8000` (adjust host/port if different)
- The endpoint expects JSON and returns a JSON response with the agent's reply


## Security Note

This tool is designed for educational and research purposes only. Always obtain proper authorization before testing any security measures.

