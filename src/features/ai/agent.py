from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from .tools import get_flight_market_data, get_demand_stats
import os


def get_ai_agent():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    tools = [get_flight_market_data, get_demand_stats]

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent