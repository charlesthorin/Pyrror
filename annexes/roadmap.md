Étape 1 : Le miroir local (La mécanique vidéo)

Objectif : Prouver que tu sais capturer et afficher une vidéo, tout ça sur un seul et même PC. On oublie le réseau pour l'instant.

    Action : Crée un script Python qui capture ton écran en boucle, compresse l'image (pour simuler ce qu'on fera plus tard pour le réseau), la décompresse, et l'affiche en temps réel dans une fenêtre PySide.

    Outils à explorer :

        La librairie mss pour capturer l'écran rapidement.

        cv2 (OpenCV) pour encoder l'image en JPEG (compression).

        PySide6 avec un QLabel et un QTimer pour rafraîchir l'image dans l'interface.

Étape 2 : Le coup de fil (La mécanique réseau)

Objectif : Faire communiquer tes deux PC sous Mint de la manière la plus basique possible.

    Action : Oublie la vidéo. Crée un script "Envoyeur" sur ton portable et un script "Receveur" sur ton fixe. Essaie d'envoyer un simple message texte ("Test 123") en UDP de l'un à l'autre. Une fois que ça marche, essaie d'envoyer un seul fichier image (une photo statique).

    Outils à explorer : * Le module natif socket en Python.

        Comprendre la différence entre l'adresse IP locale (ex: 192.168.1.X) et le port (ex: 5005).

Étape 3 : La fusion (Le streaming réel)

Objectif : Connecter l'Étape 1 et l'Étape 2.

    Action : Tu prends ton script de l'Étape 1. Au lieu d'afficher l'image localement, tu utilises le code de l'Étape 2 pour expédier les images compressées (le flux vidéo) via le réseau. Le PC fixe écoute, reçoit les paquets, les reconstitue et les affiche dans PySide.

    À ce stade : Félicitations, tu viens de coder un logiciel de "Screen Mirroring" (clonage d'écran) fonctionnel !

Étape 4 : L'illusion (Le moniteur virtuel)

Objectif : Reproduire la fonctionnalité spécifique de "Mirror Hall" : faire croire à ton PC portable qu'un deuxième écran physique est branché, pour étendre le bureau au lieu de le cloner.

    Action : Il va falloir manipuler le système d'affichage de Linux Mint (X11) pour générer une sortie vidéo fantôme. Une fois cet écran virtuel créé, tu diras à ton script de l'Étape 3 de capturer uniquement la zone correspondant à ce faux écran.

    Outils à explorer : * La commande Linux xrandr (pour voir et manipuler les écrans).

        Le paquet xserver-xorg-video-dummy (une astuce classique sous Linux pour forcer des affichages virtuels).