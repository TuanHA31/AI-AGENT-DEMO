def build_prompt_node(state):

    # lấy lịch sử hội thoại từ state
    history = state.get("messages", [])

    messages = [
        {
            "role": "system",
            "content": "Answer only based on provided context"
        }
    ]

    # thêm lịch sử chat
    messages.extend(history)

    # thêm câu hỏi mới + context
    messages.append({
        "role": "user",
        "content": f"""
Context:
{state.get('context', '')}

Question:
{state.get('question', '')}
"""
    })

    state["messages"] = messages

    return state