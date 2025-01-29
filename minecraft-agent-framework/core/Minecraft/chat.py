from core.Minecraft.environment import Environment

class Chat:
    def __init__(self, environment: Environment):
        self.env = environment
        self.simulated_messages = []  # Lista de mensajes simulados

    def send_message(self, message):
        """Send a message to the chat."""
        self.env.post_to_chat(message)
    
    def simulate_message(self, message):
        """Add a simulated message to the chat."""
        self.simulated_messages.append(message)

    def read_messages(self):
        """Retrieve simulated messages."""
        messages = self.simulated_messages[:]
        self.simulated_messages = []  # Limpia los mensajes después de leer
        return messages