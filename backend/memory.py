chat_history = []


def add_user_message(message):
    chat_history.append({
        "role": "user",
        "content": message
    })


def add_assistant_message(message):
    chat_history.append({
        "role": "assistant",
        "content": message
    })


def get_history():

    history = ""

    for msg in chat_history[-10:]:

        history += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    return history