from core.base_agent import BaseAgent
from core.action import Action
from core.event_observer import EventObserver
import random

class InsultBot(BaseAgent, Action, EventObserver):
    def __init__(self, name):
        super().__init__(name)
        self.insults = [
            "imbecil",
            "espavila, atontada!",
            "que te iba a decir... a si, gilipollas!",
            "mi primo de 3 años juega mejor que tu!"
        ]

    def run(self):
        self.chat.send_message("InsultBot: Menciona a alguien para que lo insulte.")

    def update(self, event):
        if hasattr(event, 'message') and isinstance(event.message, str):
            message = event.message.lower()

            if message.startswith("insultbot insult"):
                self.handle_insult(message)
            elif message.startswith("insultbot help"):
                self.show_help()
    def handle_insult(self, message):
        try:
            player_name = message.split("insult ")[1].strip()
            insult = random.choice(self.insults)
            self.chat.send_message(f"{player_name}, {insult}")
        except IndexError:
            self.chat.send_message("Por favor especifica el nombre de un jugador. Ejemplo: InsultBot insult player_1234")
    def show_help(self):
        messages = [
            "Comandos disponibles para InsultBot:",
            "   - insult [player_name]: ",
            "       Insulta al jugador especificado."
        ]
        list(map(self.chat.send_message, messages))
