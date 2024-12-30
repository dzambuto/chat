import paho.mqtt.client as mqtt
import uuid
import os
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import PromptSession


class Chat:
    """Classe per gestire la chat tramite MQTT e la stampa dei messaggi."""

    # Attributi fissi
    BROKER = "broker.hivemq.com"
    PORT = 1883
    TOPIC = os.getenv("MQTT_TOPIC", "default_topic")

    def __init__(self, username, magic=None):
        """
        Inizializza il client MQTT, l'interfaccia di stampa e l'elaborazione magica.

        Args:
            username (str): Il nome dell'utente.
            magic (Magic, optional): Istanza della classe Magic per elaborare i messaggi.
        """
        # Configurazione del client MQTT
        self.username = username
        self.client_id = str(uuid.uuid4())  # ID univoco del client
        self.client = mqtt.Client()
        self.client.connect(self.BROKER, self.PORT, 60)
        self.client.subscribe(self.TOPIC)
        self.client.loop_start()

        # Configurazione della gestione messaggi
        self.session = PromptSession()
        self.message_callback = None  # Callback per i messaggi ricevuti
        self.magic = magic  # Istanza della classe Magic

    def receive(self, callback):
        """
        Imposta la funzione di callback per i messaggi ricevuti.

        Args:
            callback (callable): Funzione chiamata quando arriva un messaggio.
        """
        self.message_callback = callback
        self.client.on_message = self._on_message

    def _on_message(self, client, userdata, msg):
        """
        Gestisce i messaggi MQTT e chiama il callback utente con il messaggio decodificato.
        Ignora i messaggi inviati dal proprio client.
        """
        message = msg.payload.decode()
        if not message.startswith(self.client_id):  # Ignora i propri messaggi
            message = message.split(" ", 1)[1] if " " in message else message
            if self.magic:
                message = self.magic.process(message)  # Elabora il messaggio con Magic
            if self.message_callback:
                self.message_callback(message)

    def send(self, message):
        """
        Invia un messaggio al topic configurato.

        Args:
            message (str): Messaggio da inviare.
        """
        if self.magic:
            message = self.magic.process(message)  # Elabora il messaggio con Magic
        full_message = f"{self.client_id} {message}"  # Aggiunge l'ID come prefisso
        self.client.publish(self.TOPIC, full_message)

    def disconnect(self):
        """Disconnette il client MQTT."""
        self.client.loop_stop()
        self.client.disconnect()

    # Gestione della stampa e input
    def show_message(self, message, color="green"):
        """
        Mostra un messaggio sullo schermo.

        Args:
            message (str): Il messaggio da stampare.
            color (str): Colore del messaggio (ad esempio "blue", "green", "yellow", "red").
        """
        print_formatted_text(HTML(f'<ansi{color}>{message}</ansi{color}>'))

    def get_input(self):
        """
        Richiede l'input dell'utente.

        Returns:
            str: Il messaggio inserito dall'utente.
        """
        return self.session.prompt(HTML(f'<ansiyellow>{self.username}:</ansiyellow> '))

    def display(self):
        """
        Restituisce un contesto per garantire che i messaggi e l'input
        vengano visualizzati correttamente.

        Returns:
            patch_stdout: Un contesto per la gestione sicura dell'output.
        """
        return patch_stdout()
