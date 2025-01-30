from core.base_agent import BaseAgent
from core.action import Action
from core.event_observer import EventObserver
from datetime import datetime
import random

class OracleBot(BaseAgent, Action, EventObserver):
    def __init__(self, name):
        super().__init__(name)
        self.answers = {
            "que dia es hoy?": self.get_today_date(),
            "cual es el mejor bloque?": "El mejor bloque es el diamante, por supuesto!"
        }

    def get_today_date(self):
        return datetime.now().strftime("Hoy es %A, %d de %B de %Y.")

    def run(self):
        self.chat.send_message("OracleBot: Pregunta lo que quieras, agrega, elimina o modifica informacion.")

    def update(self, event):
        if hasattr(event, 'message') and isinstance(event.message, str):
            message = event.message.lower()

            if message.startswith("oraclebot add info:"):
                try:
                    data = message.split("oraclebot add info:")[1]
                    question, answer = data.split("->")
                    self.answers[question.strip()] = answer.strip()
                    self.chat.send_message(f"He agregado la respuesta para: '{question.strip()}'.")
                except ValueError:
                    self.chat.send_message("Formato incorrecto. Usa: OracleBot add info: pregunta -> respuesta")

            elif message.startswith("oraclebot remove info:"):
                try:
                    question = message.split("oraclebot remove info:")[1].strip()
                    if question in self.answers:
                        del self.answers[question]
                        self.chat.send_message(f"He eliminado la respuesta para: '{question}'.")
                    else:
                        self.chat.send_message(f"No he encontrado informacion para: '{question}'.")
                except IndexError:
                    self.chat.send_message("Por favor especifica la pregunta que deseas eliminar.")

            elif message.startswith("oraclebot update info:"):
                try:
                    data = message.split("oraclebot update info:")[1]
                    question, new_answer = data.split("->")
                    if question.strip() in self.answers:
                        self.answers[question.strip()] = new_answer.strip()
                        self.chat.send_message(f"He actualizado la respuesta para: '{question.strip()}'.")
                    else:
                        self.chat.send_message(f"No he encontrado informacion para: '{question.strip()}'.")
                except ValueError:
                    self.chat.send_message("Formato incorrecto. Usa: OracleBot update info: pregunta -> nueva respuesta")

            elif message.startswith("oraclebot help"):
                self.show_help()

            elif message.startswith("oraclebot"):
                question = message.replace("oraclebot", "").strip()
                answer = self.answers.get(question, "No se la respuesta a esa pregunta.")
                self.chat.send_message(f"{question} -> {answer}")

            

    def show_help(self):
        self.chat.send_message("Comandos disponibles para OracleBot:")
        self.chat.send_message("- Pregunta predefinida: Recibe respuestas configuradas.")
        self.chat.send_message("- add info: pregunta -> respuesta: Agrega una respuesta nueva.")
        self.chat.send_message("- remove info: pregunta: Elimina una respuesta existente.")
        self.chat.send_message("- update info: pregunta -> nueva respuesta: Actualiza una respuesta existente.")