import mcpi.minecraft as minecraft

class Environment:
    def __init__(self):
        self.mc = minecraft.Minecraft.create()
    
    def post_to_chat(self, message):
        """Post a message to the chat."""
        self.mc.postToChat(message)

    def get_player_position(self):
        """Get the player's current position."""
        return self.mc.player.getTilePos()

    def set_block(self, x, y, z, block_type):
        """Place a block at the specified position."""
        self.mc.setBlock(x, y, z, block_type)

    def get_block(self, x, y, z):
        """Get the block type at the specified position."""
        return self.mc.getBlock(x, y, z)