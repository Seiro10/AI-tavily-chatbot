import os
from dotenv import load_dotenv
from typing import Annotated
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from app.models.tool_node import BasicToolNode
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

# Get API keys from environment
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Initialize Tavily Search Tool
tool = TavilySearchResults(api_key=tavily_api_key, max_results=2)
tools = [tool]

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize AI Model
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
llm_with_tools = llm.bind_tools(tools)

# Setup LangGraph
graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

tool_node = BasicToolNode(tools=[tool])

# Add nodes to LangGraph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

def route_tools(state: State):
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state: {state}")

    return "tools" if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0 else END

# Define Graph Routes
graph_builder.add_conditional_edges("chatbot", route_tools, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

# Compile Graph
graph = graph_builder.compile()

def process_user_message(user_input: str):
    events = graph.stream({"messages": [{"role": "user", "content": user_input}]})
    response = None
    for event in events:
        for value in event.values():
            response = value["messages"][-1].content
    return response
