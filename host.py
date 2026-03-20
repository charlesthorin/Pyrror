import socket

# Paramètres de connexion
HOST = ""  # L'adresse locale (localhost)
PORT = 12345  # Un port au choix (au-dessus de 1024)

print(f"Démarrage du serveur sur {HOST}:{PORT}...")

# 1. On crée le socket "serveur" avec la syntaxe 'with' (fermeture automatique)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serveur:
    serveur.bind((HOST, PORT))  # On l'attache à l'adresse et au port
    serveur.listen()  # Il commence à écouter

    print("En attente d'un client...")

    # 2. Le programme se bloque ici jusqu'à ce qu'un client arrive
    connexion, adresse = serveur.accept()

    # 'with' gère aussi la fermeture propre du socket 'connexion' avec ce client
    with connexion:
        print(f"Un client s'est connecté depuis {adresse}")

        # 3. Boucle infinie pour écouter les messages
        while True:
            # Le programme se bloque ici en attendant un message (max 1024 octets)
            donnees = connexion.recv(1024)

            # Condition de sécurité : Si on reçoit b'', le client est parti
            if not donnees:
                print("Le client a coupé la connexion.")
                break

            # On traduit les données (octets) en texte (string)
            message = donnees.decode("utf-8").strip()
            print(f"Message reçu : {message}")

            # Condition d'arrêt logique : Le message est "stop"
            if message.lower() == "stop":
                print("Mot de passe 'stop' détecté ! Arrêt du script.")
                break  # On sort de la boucle, le 'with' va fermer la connexion
