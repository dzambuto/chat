from chat import Chat
from magic import Magic
from playsound import playsound

# Dizionario magico (emoji e comandi unificati)
MAGIC_DICT = {
    ":smile:": "😃",
    ":heart:": "❤️",
    ":meow": lambda: "🐱 Miao!",
    ":jump": lambda: print("*salta in aria!*"),
}

# Istanza della classe Magic
magic_processor = Magic(MAGIC_DICT)

# Nome utente
username = input("Inserisci il tuo nome: ")

# Crea un'istanza della chat con Magic
chat = Chat(username, magic=magic_processor)

# Funzione per gestire i messaggi ricevuti
def on_message(message):
    """Callback per la ricezione dei messaggi (decodificati)."""
    if message:  # Mostra solo messaggi non vuoti
        chat.show_message(message, color="green")
    playsound("notification.mp3")  # Riproduce un suono quando arriva un messaggio

# Imposta il callback per i messaggi ricevuti
chat.receive(on_message)

chat.show_message("Chat MQTT avviata! Scrivi un messaggio e premi INVIO.", color="blue")
chat.show_message("(Premi CTRL+C per uscire)\n", color="yellow")

try:
    # Gestione dell'input e dell'output
    with chat.display():
        while True:
            # Leggi l'input dall'utente
            raw_message = chat.get_input()
            chat.send(f"{username}: {raw_message}")
except KeyboardInterrupt:
    chat.show_message("Chat terminata. Arrivederci!", color="red")
    chat.disconnect()
