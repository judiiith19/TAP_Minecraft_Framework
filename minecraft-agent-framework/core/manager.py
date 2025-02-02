import os
import importlib
import mcpi.minecraft as minecraft
from core.base_agent import BaseAgent

class Manager:
    mc = minecraft.Minecraft.create()
    
    def __init__(self):
        self.agents = self.load_agents()

    def load_agents(self):
        agents = []
        base_path = os.path.dirname(os.path.abspath(__file__))  # Obtener la ruta base del archivo actual
        agents_path = os.path.join(base_path, "..", "agents")  # Ruta relativa a la carpeta agents
        for filename in os.listdir(agents_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"agents.{filename[:-3]}"  # Usar formato de módulo Python
                module = importlib.import_module(module_name)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, BaseAgent) and attribute is not BaseAgent:
                        agents.append(attribute(attribute_name))
        return agents

    
    def notify(self, event):
        if hasattr(event, 'message') and isinstance(event.message, str):
            message = event.message.lower()
            for agent in self.agents:
                if agent.name.lower() in message:  # Si el nombre del bot está en el mensaje
                    agent.update(event)  # Activar ese bot


    def run(self):
        try:
            print("Press Ctrl+C to stop it.")
            while True:
                chats = self.mc.events.pollChatPosts()
                for chat in chats:
                    self.notify(chat)
        except KeyboardInterrupt:
            print("Closing manager... Bye!")