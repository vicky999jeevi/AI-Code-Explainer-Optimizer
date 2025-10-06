# graph_workflow.py

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()


# --- 1. DEFINE THE GRAPH STATE ---

class CodeAgentState(TypedDict):
    """Represents the state of our graph, passed between nodes."""
    user_prompt: str
    code_snippet: str
    intent: str
    response: str

# Initialize the Gemini LLM
# The model will automatically pick up the GOOGLE_API_KEY from environment variables
try:
    # Use gemini-2.5-flash for its speed and strong reasoning capabilities
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
except Exception:
    llm = None 
    print("Warning: GOOGLE_API_KEY not found. LLM nodes will return an error.")

# --- 2. DEFINE THE NODES (FUNCTIONS) ---

def analyze_intent(state: CodeAgentState) -> dict:
    """Node 1: Analyzes the user's prompt to determine their intent (explain or optimize)."""
    if not llm: return {"intent": "error"}

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert code analysis agent. Given a user's prompt, determine if they want to 'explain' or 'optimize' the provided code. Respond with ONLY a single word in lowercase: 'explain' or 'optimize'."),
        ("human", "Prompt: {user_prompt}\nCode:\n{code_snippet}")
    ])
    chain = prompt | llm
    
    intent = chain.invoke({"user_prompt": state["user_prompt"], "code_snippet": state["code_snippet"]}).content.strip().lower()
    
    return {"intent": intent}

def explain_code(state: CodeAgentState) -> dict:
    """Node 2: Generates a detailed explanation of the code snippet."""
    if not llm: return {"response": "Error: Gemini API Key not configured."}

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful programming tutor powered by Gemini. Explain the following code snippet in a simple, easy-to-understand way, line by line. Provide a concise summary at the end."),
        ("human", "Code:\n{code_snippet}")
    ])
    chain = prompt | llm
    
    explanation = chain.invoke({"code_snippet": state["code_snippet"]}).content
    
    return {"response": explanation}

def optimize_code(state: CodeAgentState) -> dict:
    """Node 3: Generates an optimized version of the code snippet."""
    if not llm: return {"response": "Error: Gemini API Key not configured."}

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert software engineer powered by Gemini. Refactor the following code to make it more efficient, readable, and idiomatic (pythonic, etc.). Provide the refactored code (in a code block) and a brief explanation of the changes."),
        ("human", "Code:\n{code_snippet}")
    ])
    chain = prompt | llm
    
    optimized_code = chain.invoke({"code_snippet": state["code_snippet"]}).content
    
    return {"response": optimized_code}

# --- 3. CONDITIONAL ROUTING LOGIC ---

def route_intent(state: CodeAgentState) -> Literal["explain_code", "optimize_code"]:
    """Conditional router based on intent field in the state."""
    intent = state["intent"].strip().lower()
    
    if intent == "explain":
        return "explain_code"
    elif intent == "optimize":
        return "optimize_code"
    else:
        # Fallback for unclear or error intent
        return "explain_code"

# --- 4. GRAPH COMPILATION FUNCTION ---

def create_code_explainer_graph():
    """Builds and compiles the LangGraph workflow."""
    workflow = StateGraph(CodeAgentState)

    # Add nodes
    workflow.add_node("analyze_intent", analyze_intent)
    workflow.add_node("explain_code", explain_code)
    workflow.add_node("optimize_code", optimize_code)

    # Set the entry point
    workflow.set_entry_point("analyze_intent")

    # Add conditional edge from the intent analysis node
    workflow.add_conditional_edges(
        "analyze_intent",
        route_intent,
        {
            "explain_code": "explain_code",
            "optimize_code": "optimize_code",
        }
    )

    # Add edges to the END node
    workflow.add_edge("explain_code", END)
    workflow.add_edge("optimize_code", END)

    # Compile the graph
    return workflow.compile()

