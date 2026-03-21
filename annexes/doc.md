1. Le Gardiennage du Système (Wrapper)

Le point d'entrée n'est plus l'interface graphique, mais main.py. Son rôle est purement protecteur : il configure l'écran virtuel avec Linux via xrandr, puis il lance l'interface graphique (app.py) comme un programme indépendant (sous-processus). Le bloc try...finally garantit que même si l'interface graphique fait un crash critique (Segfault) ou est tuée de force, le programme gardien survivra juste assez longtemps pour éteindre l'écran virtuel proprement.
2. L'Interface Graphique et l'Isolation (Threads)

Lorsque app.py démarre, il crée la fenêtre (le QWidget) et ses boutons. Pour éviter que la capture vidéo ou le téléchargement réseau ne gèle la fenêtre, la classe Sharing (qui gère le réseau) est poussée dans un thread secondaire (QThread). À partir de ce moment, l'interface graphique et le réseau vivent leur vie en parallèle. Ils ne communiquent qu'à l'aide de "Signaux", un système natif à Qt qui permet de passer des variables d'un thread à l'autre en toute sécurité.
3. La Gestion des Sockets (Réseau et Ports)

La classe Sharing utilise deux optimisations vitales pour éviter les plantages lors des relances :

    SO_REUSEADDR : Demande au système d'exploitation de libérer immédiatement le port réseau (12345) à la fermeture de l'application ou lors d'un crash. Sans cela, relancer l'application afficherait une erreur "Port already in use".

    TCP_NODELAY : Désactive le regroupement de paquets de TCP. Les données sont envoyées instantanément sur le réseau pour minimiser la latence du flux vidéo.

4. Le Cycle de Capture (Mode Stream)

Lorsque le serveur démarre, la classe Capture prend un cliché brut de l'écran ciblé grâce à mss et le transforme en tableau numérique (numpy). Ce tableau est ensuite compressé au format JPEG (qualité 50%) via OpenCV pour réduire drastiquement son poids réseau. Pour éviter que le réseau ne s'engorge et ne crée un décalage de plusieurs secondes, une vérification du temps est effectuée à chaque boucle : si l'image a été traitée en moins de 33 ms, le thread s'endort brièvement pour forcer un maximum de 30 images par seconde.
5. Le Protocole d'Envoi et Réception (Header + Payload)

Le réseau TCP est un flux continu : il ne sait pas où commence et où s'arrête une image. Le code utilise donc une logique stricte en deux temps :

    L'en-tête (Header) : Le serveur envoie d'abord la taille exacte de l'image compressée (encodée sur 8 octets).

    Le corps (Payload) : Le serveur envoie ensuite les octets de l'image.
    Côté client (Mode Mirror), le code bloque jusqu'à recevoir exactement 8 octets pour connaître la taille de la prochaine image. Ensuite, il lit le flux réseau jusqu'à accumuler le nombre exact d'octets annoncé, garantissant qu'aucune image ne sera coupée ou mélangée.

6. L'Affichage (Mode Mirror)

Une fois l'image entière reconstituée sous forme d'octets bruts côté client, le worker réseau l'envoie à l'interface graphique via le signal image_received.emit(). L'interface graphique (app.py) attrape ces octets, les convertit en image compatible avec l'écran (QPixmap), redimensionne l'image pour l'adapter à la fenêtre tout en gardant les proportions, et l'applique au QLabel pour l'afficher à l'utilisateur.
