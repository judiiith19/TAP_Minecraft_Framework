from core.base_agent import BaseAgent
from core.action import Action
from core.event_observer import EventObserver
import mcpi.block as block
import time
import math

class TNTBot(BaseAgent, Action, EventObserver):
    def run(self):
        self.chat.send_message("TNTBot: Escribe comandos para interactuar conmigo :)")

    def update(self, event):
        if hasattr(event, 'message') and isinstance(event.message, str):
            message = event.message.lower()

            if "add tnt" in message:
                self.add_tnt()
            elif "fire tnt" in message:
                self.fire_tnt()
            elif "line tnt" in message:
                try:
                    # Obtener la longitud de la fila de TNT del mensaje
                    length = int(message.split("line tnt ")[1])
                    self.line_tnt(length)
                except (IndexError, ValueError):
                    self.chat.send_message("Por favor especifica la longitud de la fila. Ejemplo: TNTBot line TNT 5")
            elif message.startswith("tntbot help"):
                self.show_help()
            
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
        self.chat.send_message(f"He colocado una fila de {length} bloques de TNT. Detonandola en 5 segundos...")
        time.sleep(5)
        for i in range(length):
            self.environment.set_block(pos.x + i, pos.y + 1, pos.z, block.FIRE.id)
        self.chat.send_message("Fila de TNT detonada.")
    
    def show_help(self):
        self.chat.send_message("Comandos disponibles para TNTBot:")
        self.chat.send_message("- add tnt: Añade un bloque de TNT junto al jugador.")
        self.chat.send_message("- fire tnt: Detona el TNT mas cercano en un radio de 3 bloques.")
        self.chat.send_message("- line tnt [longitud]: Coloca y detona una fila de TNT de la longitud especificada.")