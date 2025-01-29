from core.Minecraft.environment import Environment
from core.Minecraft.movement import Movement
from core.Minecraft.chat import Chat

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.environment = Environment()
        self.movement = Movement(self.environment)
        self.chat = Chat(self.environment)
        
