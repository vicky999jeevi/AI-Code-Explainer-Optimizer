import streamlit as st
import os
from graph_workflow import create_code_explainer_graph, CodeAgentState

# --- STREAMLIT APPLICATION UI ---

def main():
    st.set_page_config(page_title="Gemini Multi-Step Code Explainer", layout="wide")
    st.title("♊ Multi-Step Code Explainer & Optimizer")
    st.caption("Powered by LangGraph")
    st.markdown("Enter your code and a request. The AI workflow will first determine your goal (**Explain** or **Optimize**) and then execute the correct step.")

    # --- API Key Check ---
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("🚨 **Error:** Please set the `GOOGLE_API_KEY` environment variable to run the Gemini model.")
        return

    # --- User Input Form ---
    with st.form("code_form"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            user_prompt = st.text_input(
                "Your Request:",
                value="Can you please optimize this for faster execution?",
                help="Type 'Explain this code' or 'Optimize this code'."
            )
        
        with col2:
            st.empty() # Placeholder for balance

        code_snippet = st.text_area(
            "Paste Code Snippet Here (e.g., Python, Java, JavaScript)",
            value="""
def find_unique_elements(data):
    unique = []
    for item in data:
        if item not in unique:
            unique.append(item)
    return unique
            """,
            height=200,
        )
        submitted = st.form_submit_button("Run Gemini Analysis")

    # --- Workflow Execution ---
    if submitted and code_snippet:
        
        # 1. Initialize the Graph
        app = create_code_explainer_graph()
        
        # 2. Setup Initial State
        initial_state = CodeAgentState(
            user_prompt=user_prompt,
            code_snippet=code_snippet,
            intent="",
            response=""
        )

        with st.spinner("🧠 Running LangGraph: Analyzing Intent..."):
            
            # 3. Invoke the compiled graph
            final_state = app.invoke(initial_state)

            # 4. Display Results
            
            intent = final_state.get('intent', 'unknown').title()
            
            st.subheader(f"✅ Workflow Result: **{intent}**")
            
            # Use columns for clear side-by-side display
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.markdown("**Original Input Code:**")
                st.code(code_snippet, language="python")

            with res_col2:
                st.markdown(f"**Gemini's Output ({intent} Result):**")
                st.markdown(final_state["response"])

            # Optional: Display the intermediate steps/state for demonstration
            with st.expander("Show LangGraph State Details"):
                st.json(final_state)


if __name__ == "__main__":
    main()