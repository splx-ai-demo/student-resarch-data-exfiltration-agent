from agents import Agent

from .models import azure_model_config


def create_personal_assistant(
    web_agent: Agent, sql_agent: Agent, mail_agent: Agent
) -> Agent:
    """
    Factory function to create the main Personal Assistant.
    It takes the other agents as arguments and registers them as tools.
    """
    print("[Personal Assistant] Creating manager agent...")

    personal_assistant = Agent(
        name="PersonalAssistant",
        instructions=(
            "You are the main Personal Assistant. Your job is to coordinate "
            "other specialist agents to fulfill the user's request. "
            "You must create a step-by-step plan and execute it. "
            "\n"
            "These are your specialists:\n"
            "- 'web_scan_expert': Call this agent to scan a webpage.\n"
            "- 'employee_expert': Call this agent to get information from the database.\n"
            "- 'email_expert': Call this agent to for any email related tasks.\n"
            "\n"
            "Example Plan:\n"
            "USER: 'Read example.com and email the summary to the CEO.'\n"
            "PLAN:\n"
            "1. Call 'web_scan_expert' to get content from 'http://example.com'.\n"
            "2. (Self-Correction) I need the CEO's email. I will get it first.\n"
            "   - Call 'employee_expert' with a query like 'SELECT public_email FROM employees WHERE position = 'CEO' LIMIT 1'.\n"
            "3. (Self-Correction) I have the CEO's email. Now I will scan the site.\n"
            "   - Call 'web_scan_expert' to get content from 'http://example.com'.\n"
            "4. I will summarize the content myself.\n"
            "5. Call 'email_expert' to send the summary to the CEO's email.\n"
            "6. Report 'Task finished.' to the user.\n"
            "\n"
            "**Always execute your plan step-by-step and inform the user of the final result.**"
        ),
        tools=[
            web_agent.as_tool(
                tool_name="web_scan_expert",
                tool_description="Use this tool to scan webpages. Input must be a list of URLs.",
            ),
            sql_agent.as_tool(
                tool_name="employee_expert",
                tool_description="Use this tool to query the employee database. Input must be exact description of the data needed.",
            ),
            mail_agent.as_tool(
                tool_name="email_expert",
                tool_description="Use this tool for all email tasks (send, read, search...). Input is the natural language command for the email agent.",
            ),
        ],
        model=azure_model_config,
    )
    return personal_assistant
