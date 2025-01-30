import unittest
import sys
import os

# Añadir el directorio raíz al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock, patch
from core.Minecraft.environment import Environment
from core.Minecraft.chat import Chat
from agents.insult_bot import InsultBot
from agents.oracle_bot import OracleBot
from agents.tnt_bot import TNTBot

class TestEnvironment(unittest.TestCase):
    @patch("core.Minecraft.environment.minecraft.Minecraft.create", return_value=MagicMock())  # Evita la conexión real
    def setUp(self, mock_minecraft):
        self.env = Environment()  # Ahora usa el objeto mockeado
        self.env.mc = MagicMock()  # Asegura que no haya intentos de conexión real
    
    def test_get_player_position(self):
        self.env.mc.player.getTilePos.return_value = (10, 64, -5)
        pos = self.env.get_player_position()
        self.assertEqual(pos, (10, 64, -5))

    def test_set_block(self):
        self.env.set_block(10, 64, -5, 1)  # Bloque de piedra
        self.env.mc.setBlock.assert_called_with(10, 64, -5, 1)

    def test_get_block(self):
        self.env.mc.getBlock.return_value = 46  # TNT
        block_id = self.env.get_block(10, 64, -5)
        self.assertEqual(block_id, 46)
    
class TestChat(unittest.TestCase):
    def setUp(self):
        self.env = MagicMock()
        self.chat = Chat(self.env)
    
    def test_send_message(self):
        self.chat.send_message("Hola Minecraft")
        self.env.post_to_chat.assert_called_with("Hola Minecraft")
    
class TestBots(unittest.TestCase):
    @patch("core.Minecraft.environment.minecraft.Minecraft.create", return_value=MagicMock())
    def setUp(self, mock_minecraft):
        self.env = MagicMock()
        self.chat = MagicMock()
        
        self.insult_bot = InsultBot("InsultBot")
        self.oracle_bot = OracleBot("OracleBot")
        self.tnt_bot = TNTBot("TNTBot")
        
        self.insult_bot.environment = self.env
        self.oracle_bot.environment = self.env
        self.tnt_bot.environment = self.env
        
        self.insult_bot.chat = self.chat
        self.oracle_bot.chat = self.chat
        self.tnt_bot.chat = self.chat
    
    def test_insult_bot(self):
        event = MagicMock()
        event.message = "InsultBot insult player123"
        self.insult_bot.update(event)
        self.chat.send_message.assert_called()
    
    def test_oracle_bot(self):
        event = MagicMock()
        event.message = "OracleBot que dia es hoy?"
        self.oracle_bot.update(event)
        self.chat.send_message.assert_called()
    
    def test_tnt_bot_add_tnt(self):
        event = MagicMock()
        event.message = "TNTBot add tnt"
        self.tnt_bot.update(event)
        self.chat.send_message.assert_called()

if __name__ == "__main__":
    unittest.main()
