from core.base_agent import BaseAgent
from core.action import Action
from core.event_observer import EventObserver
import mcpi.block as block
import time
import math

class TNTBot(BaseAgent, Action, EventObserver):
    def run(self):
        self.chat.send_message("TNTBot: Escribe comandos para interactuar conmigo.")

    def update(self, event):
        if hasattr(event, 'message') and isinstance(event.message, str):
            message = event.message.lower()

            commands = {
                "tntbot add tnt": lambda: self.add_tnt(),
                "tntbot fire tnt": lambda: self.fire_tnt(),
                "tntbot help": lambda: self.show_help(),
            }

            for cmd, func in commands.items():
                if message.startswith(cmd):
                    func()
                    return
                
            if message.startswith("tntbot line tnt"):
                try:
                    length = int(message.split("line tnt ")[1])
                    self.line_tnt(length)
                    return
                except (IndexError, ValueError):
                    self.chat.send_message("Por favor especifica la longitud de la fila. Ejemplo: TNTBot line TNT 5")
                    return
            
    def add_tnt(self):
        pos = self.environment.get_player_position()
        tnt_pos = (pos.x + 1, pos.y, pos.z)
        self.environment.set_block(tnt_pos[0], tnt_pos[1], tnt_pos[2], block.TNT.id)
        self.chat.send_message("He colocado un bloque de TNT al lado del jugador.")
    
    def fire_tnt(self):
        pos = self.environment.get_player_position()
        for x in range(-3, 4):
            for y in range(-3, 4):
                for z in range(-3, 4):
                    if math.sqrt(x**2 + y**2 + z**2) <= 3:
                        if self.environment.get_block(pos.x + x, pos.y + y, pos.z + z) == block.TNT.id:
                            self.environment.set_block(pos.x + x, pos.y + y + 1, pos.z + z, block.FIRE.id)
                            self.chat.send_message(f"He detonado un bloque de TNT en ({pos.x + x}, {pos.y + y}, {pos.z + z}).")
                            return
        self.chat.send_message("No he encontrado TNT cercano para detonar.")
    
    def line_tnt(self, length):
        pos = self.environment.get_player_position()
        for i in range(length):
            self.environment.set_block(pos.x + i, pos.y, pos.z, block.TNT.id)
        self.chat.send_message(f"He colocado una fila de {length} bloques de TNT.")
        for i in range(5, 0, -1):
            self.chat.send_message(f"Detonando en {i} segundos...")
            time.sleep(1)
        for i in range(length):
            self.environment.set_block(pos.x + i, pos.y + 1, pos.z, block.FIRE.id)
        self.chat.send_message("Fila de TNT detonada.")
        
    def show_help(self):
        messages = [
            "Comandos disponibles para TNTBot:",
            "   - add tnt: ",
            "       Coloca un bloque de TNT junto al jugador.",
            "   - fire tnt: ",
            "       Detona el TNT mas cercano en un radio de 3 bloques.",
            "   - line tnt [longitud]: ",
            "       Coloca y detona una fila de TNT de la longitud especificada.",
        ]
        list(map(self.chat.send_message, messages))