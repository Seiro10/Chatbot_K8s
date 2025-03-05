import os
from backend.models.tool_node import BasicToolNode
from google.cloud import secretmanager
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated\


# Function to get secrets from Google Secret Manager
def get_secret(secret_name):
    """Retrieve secret value from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    project_id = "chatbot-tavily"
    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    
    try:
        print(f"Fetching secret: {secret_name} from {secret_path}")
        response = client.access_secret_version(name=secret_path)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None

# Load API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Ensure API keys exist
if not openai_api_key or not tavily_api_key:
    raise ValueError("Missing API keys! Ensure they are in Secret Manager or environment variables.")

# Initialize Tavily Search Tool
tool = TavilySearchResults(api_key=tavily_api_key, max_results=2)
tools = [tool] 

# Define the chatbot state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize AI Model
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
llm_with_tools = llm.bind_tools(tools)

# Setup LangGraph
graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Initialize ToolNode
tool_node = BasicToolNode(tools=[tool])

# Nodes to LangGraph
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
    """Processes user messages and gets chatbot responses"""
    events = graph.stream({"messages": [{"role": "user", "content": user_input}]})
    response = None
    for event in events:
        for value in event.values():
            response = value["messages"][-1].content
    return response
