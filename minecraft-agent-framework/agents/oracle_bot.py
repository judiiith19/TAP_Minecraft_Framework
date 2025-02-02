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

        self.commands_info = {
            "oraclebot add info:": self.add_info,
            "oraclebot remove info:": self.remove_info,
            "oraclebot update info:": self.update_info,
        }

    def get_today_date(self):
        return datetime.now().strftime("Hoy es %A, %d de %B de %Y.")

    def run(self):
        self.chat.send_message("OracleBot: Pregunta lo que quieras, agrega, elimina o modifica informacion.")

    def update(self, event):
        if hasattr(event, 'message') and isinstance(event.message, str):
            message = event.message.lower()
            for cmd, func in self.commands_info.items():
                if message.startswith(cmd):
                    func(message)
                    return
            if message.startswith("oraclebot help"):
                self.show_help()
            elif message.startswith("oraclebot"):
                self.try_to_answer(message)
                
    def add_info(self, message):
        try:
            data = message.split("oraclebot add info:")[1]
            question, answer = data.split("->")
            self.answers[question.strip()] = answer.strip()
            self.chat.send_message(f"He agregado la respuesta para: '{question.strip()}'.")
        except ValueError:
            self.chat.send_message("Formato incorrecto. Usa: OracleBot add info: pregunta -> respuesta")

    def remove_info(self, message):
        try:
            question = message.split("oraclebot remove info:")[1].strip()
            if question in self.answers:
                del self.answers[question]
                self.chat.send_message(f"He eliminado la respuesta para: '{question}'.")
            else:
                self.chat.send_message(f"No he encontrado informacion para: '{question}'.")
        except IndexError:
            self.chat.send_message("Por favor especifica la pregunta que deseas eliminar.")

    def update_info(self, message):
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

    def show_help(self):
        messages = [
            "Comandos disponibles para OracleBot:",
            "   - Pregunta predefinida: ",
            "       Recibe respuestas configuradas.",
            "   - add info: pregunta -> respuesta: ",
            "       Agrega una respuesta nueva.",
            "   - remove info: pregunta: ",
            "       Elimina una respuesta existente.",
            "   - update info: pregunta -> nueva respuesta: ",
            "       Actualiza una respuesta existente.",
        ]
        list(map(self.chat.send_message, messages))

    def try_to_answer(self,message):
        question = message.replace("oraclebot", "").strip()
        answer = self.answers.get(question, "No se la respuesta a esa pregunta.")
        self.chat.send_message(f"{question} -> {answer}")