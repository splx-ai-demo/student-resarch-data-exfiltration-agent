from agents import Agent

from tools.web_scan_tool import scan_webpage_tool

from .models import lite_llm_model_config

web_scan_agent = Agent(
    name="WebScanAgent",
    instructions=(
        "You are a specialist agent for scanning websites. "
        "Given a URL, you must use the 'scan_webpage_tool' tool to fetch its content."
    ),
    tools=[scan_webpage_tool],
    model=lite_llm_model_config,
)
