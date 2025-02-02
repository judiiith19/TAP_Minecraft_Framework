from datetime import datetime
import unittest
import sys
import os

# Añadir el directorio raíz al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock, patch
from core.Minecraft.environment import Environment
from core.Minecraft.chat import Chat
from core.Minecraft.movement import Movement
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

class TestMovement(unittest.TestCase):
    def setUp(self):
        self.env = MagicMock()
        self.movement = Movement(self.env)
    
    def test_move_to(self):
        self.movement.env.mc.player.setTilePos = MagicMock()
        self.movement.move_to(10, 20, 30)
        self.movement.env.mc.player.setTilePos.assert_called_with(10, 20, 30)
    
class TestOracleBot(unittest.TestCase):
    @patch("core.Minecraft.environment.minecraft.Minecraft.create", return_value=MagicMock())
    def setUp(self, mock_minecraft):
        self.env = MagicMock()
        self.chat = MagicMock()
        
        self.oracle_bot = OracleBot("OracleBot")

        self.oracle_bot.environment = self.env
        self.oracle_bot.chat = self.chat
    
    def test_update(self):
        event = MagicMock()
        event.message = "OracleBot que dia es hoy?"
        self.oracle_bot.update(event)
        self.oracle_bot.chat.send_message.assert_called()

    def test_get_today_date(self):
        expected_date = datetime.now().strftime("Hoy es %A, %d de %B de %Y.")
        self.assertEqual(self.oracle_bot.get_today_date(), expected_date)
    
    def test_add_info(self):
        message = "oraclebot add info: el fuego quema? -> no"
        self.oracle_bot.add_info(message)
        self.assertEqual(self.oracle_bot.answers["el fuego quema?"], "no")

    def test_update_info(self):
        self.oracle_bot.answers["el fuego quema?"] = "no"
        message = "oraclebot update info: el fuego quema? -> si"
        self.oracle_bot.update_info(message)
        self.assertEqual(self.oracle_bot.answers["el fuego quema?"], "si")
    
    def test_remove_info(self):
        self.oracle_bot.answers["el fuego quema?"] = "si"
        message = "oraclebot remove info: el fuego quema?"
        self.oracle_bot.remove_info(message)
        self.assertNotIn("prueba", self.oracle_bot.answers)
    
    def test_try_to_answer_known(self):
        self.oracle_bot.answers["el fuego quema?"] = "si"
        self.oracle_bot.try_to_answer("oraclebot el fuego quema?")
        self.oracle_bot.chat.send_message.assert_called_with("el fuego quema? -> si")
    
    def test_try_to_answer_unknown(self):
        self.oracle_bot.try_to_answer("oraclebot pregunta desconocida")
        self.oracle_bot.chat.send_message.assert_called_with("pregunta desconocida -> No se la respuesta a esa pregunta.")
    
    def test_show_help(self):
        self.oracle_bot.show_help()
        self.oracle_bot.chat.send_message.assert_called()

class TestTNTBot(unittest.TestCase):
    @patch("core.Minecraft.environment.minecraft.Minecraft.create", return_value=MagicMock())
    def setUp(self, mock_minecraft):
        self.env = MagicMock()
        self.chat = MagicMock()
        
        self.tnt_bot = TNTBot("TNTBot")

        self.tnt_bot.environment = self.env
        self.tnt_bot.chat = self.chat
    
    def test_add_tnt(self):
        self.tnt_bot.environment.get_player_position.return_value = MagicMock(x=0, y=0, z=0)
        self.tnt_bot.add_tnt()
        self.tnt_bot.environment.set_block.assert_called()
    
    def test_fire_tnt(self):
        self.tnt_bot.environment.get_player_position.return_value = MagicMock(x=0, y=0, z=0)
        self.tnt_bot.environment.get_block.return_value = 46  # TNT block ID
        self.tnt_bot.fire_tnt()
        self.tnt_bot.environment.set_block.assert_called()

class TestInsultBot(unittest.TestCase):
    @patch("core.Minecraft.environment.minecraft.Minecraft.create", return_value=MagicMock())
    def setUp(self, mock_minecraft):
        self.env = MagicMock()
        self.chat = MagicMock()
        
        self.insult_bot = InsultBot("InsultBot")

        self.insult_bot.environment = self.env
        self.insult_bot.chat = self.chat
    
    def test_insult(self):
        event = MagicMock()
        event.message = "InsultBot insult player123"
        self.insult_bot.update(event)
        self.insult_bot.chat.send_message.assert_called()
    
if __name__ == "__main__":
    unittest.main()
