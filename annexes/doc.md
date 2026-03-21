1. Sécurisation globale du système (Le Wrapper)

Le fichier main.py est l'unique point d'entrée de l'application. Son seul rôle est de lancer l'interface utilisateur graphique (app.py) dans un processus totalement isolé. Grâce à la structure d'exécution employée, peu importe la façon dont l'application graphique se termine — que ce soit une fermeture normale, une erreur fatale C++ (Segfault) ou une interruption forcée — le script reprendra toujours la main à la fin pour exécuter une commande système forçant l'extinction du port HDMI-0. Cela garantit qu'aucun écran virtuel ne restera actif sur le système d'exploitation.
2. Création de l'écran virtuel à la demande

Contrairement aux versions précédentes, l'écran virtuel n'est plus généré au démarrage de l'application. La classe VirtualDisplayManager est bien initialisée lors de la création de l'interface, mais ses méthodes ne sont appelées que lors d'actions précises :

    L'écran virtuel est créé et allumé uniquement lorsque l'utilisateur clique sur le bouton "Stream". Cela évite la création d'écrans fantômes sur la machine client (le PC portable).

    Lors de la fermeture de la fenêtre graphique via la croix rouge, l'événement closeEvent est intercepté pour éteindre proprement l'écran avant que la mémoire ne soit libérée.
    (Note : Si xrandr refuse toujours de s'activer à cause d'un blocage matériel du pilote NVIDIA sur les ports déconnectés, les erreurs sont désormais ignorées pour empêcher le crash de l'interface, nécessitant alors l'utilisation d'un dongle HDMI ou d'une configuration xorg.conf spécifique).

3. Isolation des processus lourds (Threading)

L'interface graphique principale (MyWidget) gère uniquement l'affichage et les clics. Pour éviter que l'application ne freeze lors des boucles réseau, l'intégralité du code de la classe Sharing est transférée dans un fil d'exécution secondaire (QThread). Ce transfert garantit que l'interface reste fluide et réactive, même pendant la capture ou le téléchargement intensif de données. La communication entre ce fil d'exécution réseau et l'interface graphique est strictement régie par un signal Qt asynchrone (image_received).
4. Capture et compression de l'écran

La classe Capture est instanciée uniquement dans le fil d'exécution secondaire. Elle cible l'index 2 du gestionnaire d'écrans (mss), ce qui correspond au deuxième écran logique détecté par le système (l'écran virtuel nouvellement créé, l'écran physique principal étant à l'index 1). L'image brute extraite de la carte graphique est ensuite convertie en matrice numérique puis compressée au format JPEG, avec une qualité réduite à 50%. Cette compression drastique est vitale pour la transmission réseau.
5. Transmission réseau temps réel (Stream)

Le flux réseau est établi sur une connexion TCP. Pour maximiser la fluidité de la vidéo :

    La propriété SO_REUSEADDR est appliquée au serveur pour s'assurer que le port d'écoute soit libéré instantanément par le système d'exploitation à la fermeture de l'application.

    La propriété TCP_NODELAY est activée pour forcer l'envoi immédiat des paquets réseau, interdisant au système de mettre les octets en attente.

    Une limitation temporelle calcule le temps de traitement de chaque image et met le fil d'exécution en pause quelques millisecondes si nécessaire, stabilisant le flux à un maximum de 30 images par seconde.
    Chaque image envoyée est précédée d'un en-tête strict de 8 octets indiquant son poids exact.

6. Réception et reconstruction de l'image (Mirror)

Le client fonctionne en boucle bloquante. Il attend d'abord de recevoir exactement 8 octets pour extraire la taille de l'image entrante. Ensuite, il lit le flux réseau par blocs successifs jusqu'à atteindre exactement cette taille. Une fois la séquence d'octets complète et intègre, elle est émise vers l'interface graphique. L'interface convertit ces données brutes en un objet visuel (QPixmap), recalcule ses dimensions pour s'adapter dynamiquement à la taille actuelle de la fenêtre tout en lissant les pixels, puis l'affiche.
