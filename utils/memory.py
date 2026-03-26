chat_history = []

def add_to_memory(query, response):
    chat_history.append((query, response))

def get_memory():
    return chat_history[-3:]