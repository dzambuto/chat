class Magic:
    """Classe per gestire la sostituzione di stringhe con emoji e l'esecuzione di comandi."""

    def __init__(self, magic_dict):
        """
        Inizializza la classe con un dizionario magico.

        Args:
            magic_dict (dict): Un dizionario che mappa chiavi a stringhe (emoji/testo) o funzioni (comandi).
        """
        self.magic_dict = magic_dict

    def process(self, message):
        """
        Processa il messaggio per sostituire stringhe e/o eseguire comandi.

        Args:
            message (str): Il messaggio da processare.

        Returns:
            str: Il messaggio processato con le stringhe sostituite e i comandi concatenati.
        """
        result = []
        words = message.split()  # Suddivide il messaggio in parole
        for word in words:
            if word in self.magic_dict:
                action = self.magic_dict[word]
                if callable(action):  # Se è una funzione
                    command_result = action()
                    if command_result:  # Se la funzione restituisce un testo
                        result.append(command_result)
                else:  # Se è un'emoji o un testo
                    result.append(action)
            else:
                result.append(word)
        return " ".join(result)  # Ricostruisce il messaggio processato
