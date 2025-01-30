from core.Minecraft.environment import Environment

class Chat:
    def __init__(self, environment: Environment):
        self.env = environment
        self.simulated_messages = []  # Lista de mensajes simulados

    def send_message(self, message):
        """Enviar mensaje por el chat."""
        self.env.post_to_chat(message)