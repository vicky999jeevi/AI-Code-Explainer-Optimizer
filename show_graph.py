from graph_workflow import create_code_explainer_graph

# Create the compiled graph
graph = create_code_explainer_graph()

# Save LangGraph visualization
graph.get_graph().print_ascii()   # 👈 prints ASCII diagram in terminal
