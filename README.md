# 🏠TAP_minecraft_agent_framework
![Codecov](https://codecov.io/gh/judiiith19/TAP_minecraft_agent_framework/branch/main/graph/badge.svg)

# 📚 Descripción

Este framework permite la creación y ejecución de agentes en un servidor de Minecraft. Los agentes pueden moverse, interactuar con el entorno, construir y destruir bloques, y comunicarse a través del chat del juego.
Incluye varios agentes predefinidos, como:

🤬 InsultBot: Insulta jugadores en el chat.

🔮 OracleBot: Responde preguntas con respuestas predefinidas.

💣 TNTBot: Coloca y detona TNT en el juego.

El framework permitie a los usuarios crear sus propios agentes personalizados.

# ⚙️ Instalación

1️⃣ Requisitos
1. Minecraft 1.12
   
2. Servidor Adventures in Minecraft:👉 [GitHub - Adventures in Minecraft] (https://github.com/AdventuresInMinecraft)

3. Python 3.8 o superior

4. Librerías necesarias (se instalan con pip)
       - mcpi
       - coverage

2️⃣ Entorno Virtual

1. Crear el entorno.

   Windows (cmd/powershell)
   
       python -m venv minecraft-env

   Linux/Mac (bash)
   
       python3 -m venv minecraft-env
  
2. Activar el entorno.

   Windows (cmd/powershell)
   
       minecraft-env\Scripts\activate

   Linux/Mac (bash)
   
       source minecraft-env/bin/activate

Sabrás que está activado porque verás (minecraft-env) al inicio de la línea de comandos.

# 🚀 Uso del framework

Para iniciar el framework y ejecutar los agentes:
  
    python minecraft-agent-framework/main.py

Los agentes responderán automáticamente a eventos en el chat del juego.

# 🛠️ Cómo crear un nuevo agente

Puedes añadir un nuevo bot creando un archivo en la carpeta agents/.

Ejemplo: Crear un agente "HelloBot"

    ""Imports necessarios""
    from core.base_agent import BaseAgent
    from core.event_observer import EventObserver

    class HelloBot(BaseAgent, EventObserver):
        ""Asignar un nombre al agente""
        def __init__(self, name="HelloBot"):
            super().__init__(name)
    
        ""Iniciar el agente""
        def run(self):
            self.chat.send_message("HelloBot listo para saludar!")
  
        ""Se activa el agente para ejecutar""
        def update(self, event):
            if hasattr(event, 'message') and isinstance(event.message, str):
                message = event.message.lower()
                if "hello" in message:
                    self.chat.send_message("¡Hola, aventurero de Minecraft!")

Guarda el archivo y ejecuta main.py!

# ✅ Pruebas y cobertura de código

Este proyecto incluye pruebas unitarias y usa GitHub Actions + Codecov para medir la cobertura de código.

Al realizar un pull/push se ejecutan los test automáticamente.

Tambien se pueden ejecutar los tests manualmente:

    coverage run -m unittest discover tests
    coverage report -m

Para ver un reporte en HTML:
  
    coverage html
  
Esto generara la carpeta htmlcov/. Para ver los resultados simplemente tienes que abrir index.html 🚀

# 📌 Autor

Proyecto desarrollado por @judiiith19.
