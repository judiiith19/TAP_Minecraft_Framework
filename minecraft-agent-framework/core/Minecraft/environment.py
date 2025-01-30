import mcpi.minecraft as minecraft

class Environment:
    def __init__(self):
        self.mc = minecraft.Minecraft.create()
    
    def post_to_chat(self, message):
        """Enviar mensaje por el chat."""
        self.mc.postToChat(message)

    def get_player_position(self):
        """Obtener la posicion actual del jugador."""
        return self.mc.player.getTilePos()

    def set_block(self, x, y, z, block_type):
        """Colocar un bloque en una posicion especifica."""
        self.mc.setBlock(x, y, z, block_type)

    def get_block(self, x, y, z):
        """Obtener el tipo de un bloque en un posicion especifica."""
        return self.mc.getBlock(x, y, z)