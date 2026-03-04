class ConversationMemory:
    def __init__(self, max_turns=5):
        self.max_turns = max_turns
        self.history = []

    def add_user_message(self, message):
        self.history.append({"role": "user", "content": message})
        self._trim()

    def add_ai_message(self, message):
        self.history.append({"role": "assistant", "content": message})
        self._trim()

    def get_messages(self):
        return self.history

    def _trim(self):
        # Giữ lại max_turns * 2 messages (user + assistant)
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]