def memory_node(state):

    state["messages"].append({
        "role": "user",
        "content": state["question"]
    })

    state["messages"].append({
        "role": "assistant",
        "content": state["answer"]
    })

    return state