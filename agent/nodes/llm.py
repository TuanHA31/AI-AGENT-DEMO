def llm_node(state, llm):

    response = llm.chat(state["messages"])

    state["answer"] = response

    return state