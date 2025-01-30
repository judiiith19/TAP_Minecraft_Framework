from core.Minecraft.environment import Environment

class Movement:
    def __init__(self, environment: Environment):
        self.env = environment

    def move_to(self, x, y, z):
        """Mover al jugador a una posicion especifica."""
        self.env.post_to_chat(f"Moviendose a ({x}, {y}, {z})")
        # Placeholder for movement logic
        current_pos = self.env.get_player_position()
        self.env.post_to_chat(f"Moviendose de ({current_pos.x}, {current_pos.y}, {current_pos.z}) a ({x}, {y}, {z})")
        self.env.mc.player.setTilePos(x, y, z)