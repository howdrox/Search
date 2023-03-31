## Fonctionnalités principales

- **Game(height, width)** : Crée une instance du jeu avec une grille de taille `height` x `width`. C'est la fonction principale, elle sert à initialiser la fenêtre de l'interface graphique (`create_window()`), le canvas (`create_canvas()`), la grille de jeu (`board.show_walls()`), les personnages (`create_entities()`) et à lancer la boucle d'événements de l'interface graphique (`self.root.mainloop()`).

## Classes

- **Game** : Une classe qui gère l'état général du jeu. Elle contient les fonctions suivantes :
  - **\_\_init\_\_(self, height, width)** : Constructeur de la classe `Game`.
  - **create_window(self)** : Crée la fenêtre de l'interface graphique.
  - **create_canvas(self)** : Crée le canvas de l'interface graphique.
  - **create_entities(self)** : Crée les personnages du jeu.
- **Person** : Une classe qui représente un personnage du jeu. Elle contient les fonctions suivantes :
  - **\_\_init\_\_(self, game, evil, spawn_coord)** : Constructeur de la classe `Person`. `game` est l'instance de la classe `Game` qui gère le personnage, `evil` est un booléen qui indique si le personnage est un ennemi ou pas, `spawn_coord` est la position initiale du personnage sur la grille.
  - **show(self)** : Affiche le personnage sur le canvas.
  - **update(self)** : Met à jour la position du personnage sur le canvas.
  - **speed_set(self, k)** : Définit la vitesse de déplacement du personnage en fonction de la touche  appuyée.
  - **speed_cancel(self, k)** : Annule la vitesse de déplacement du personnage en fonction de la touche relâchée.
  - **move(self)** : Déplace le personnage sur la grille et sur le canvas.
  - **move_control(self)** : Contrôle le déplacement du personnage en appelant la fonction `move()` toutes les 1000/self.speed secondes.
  - **pathfinding(self)** : Calcule le chemin le plus court vers le joueur (si le personnage est un ennemi) en utilisant l'algorithme A*.
- **Board** : La classe Board contient les informations relatives à la grille de jeu, c'est-à-dire les murs et les espaces vides. Elle gère également la vérification des mouvements autorisés pour les personnages.
  - **\_\_init\_\_(self, game)** : Constructeur de la classe Board. Prend en paramètre l'instance de la classe Game à laquelle est associée la grille de jeu. Crée une grille de jeu en utilisant un tableau de numpy de dimensions (height, width) qui contient des 0 pour les espaces vides et des 1 pour les murs.
  - **show_walls(self)** : Affiche les murs sur la grille de jeu. Parcourt le tableau numpy contenant les informations sur la grille de jeu et dessine un rectangle noir sur la case correspondante si la case contient un mur.
  - **check_movement(self, j, i)** : Vérifie si le mouvement demandé est autorisé en vérifiant si la case correspondante dans la grille de jeu contient un mur ou non. Prend en paramètre les coordonnées de la case dans laquelle le personnage souhaite se déplacer. Renvoie True si le mouvement est autorisé et False sinon.
