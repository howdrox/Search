



## Fonctions principales

- **Game(height, width)** : Crée une instance du jeu avec une grille de taille `height` x `width`. C'est la fonction qui initialise le jeu. Dedans, `create_window()` sert à construire la fenêtre de l'interface graphique, `create_canvas()` à initialiser le canvas, `board.show_walls()` à mettre en place la grille de jeu, `create_entities()` à creer les personnages et finallement `self.root.mainloop()` à demarer la boucle pricipale de l'interface graphique.

## Classes

- **Game** : Une classe qui gère l'état général du jeu. Elle contient les fonctions suivantes :
  - **\_\_init\_\_(self, height, width)** : Constructeur de la classe `Game`.
  - **create_window(self)** : Crée la fenêtre de l'interface graphique.
  - **create_canvas(self)** : Crée le canvas de l'interface graphique.
  - **create_entities(self)** : Crée les personnages du jeu.
- **Person** : Une classe qui représente un personnage du jeu. Elle contient les fonctions suivantes :
  - **\_\_init\_\_(self, game, evil, spawn_coord)** : Constructeur de la classe `Person`. Concernant les entrées, `game` est l'instance de la classe `Game` qui gère le personnage, `evil` est un booléen qui indique si le personnage est un ennemi ou pas, `spawn_coord` est la position initiale du personnage sur la grille.
  - **show(self)** : Affiche le personnage sur le canvas.
  - **update(self)** : Met à jour la position du personnage sur le canvas.
  - **speed_set(self, k)** : Une fonction callback qui définit la vitesse de déplacement du personnage lorsqu'une touche est appuyée.
  - **speed_cancel(self, k)** : Une fonction callback qui met a zero la vitesse de déplacement du personnage lorsqu'une touche est relâchée.
  - **move(self)** : Met a jour la position du personnage dans la grille et sur le canvas.
  - **move_control(self)** : Fonction avec un timer qui contrôle le déplacement du personnage en appelant la fonction `move()` toutes les 1000/self.speed secondes.
  - **pathfinding(self)** : Calcule le chemin le plus court depuis l'ennemi jusqu'au jouer en utilisant l'algorithm A*.
- **Board** : La classe `Board` contient les informations relatives à la grille de jeu, c'est-à-dire la positions des murs. Elle gère également la vérification des mouvements autorisés pour les personnages.
  - **\_\_init\_\_(self, game)** : Constructeur de la classe `Board`. Prend en paramètre l'instance de la classe `Game`.
  - **create_walls(self)** : Crée une grille de jeu a partir d'un tableau numpy de dimensions (height, width) qui contient des 0 pour les espaces vides et des 1 pour les murs. 
  - **show_walls(self)** : Affiche les murs sur le canvas. Parcourt le tableau numpy contenant les informations sur la grille de jeu et dessine un rectangle de couleur si la case contient un mur.
  - **check_movement(self, j, i)** : Vérifie si le mouvement demandé est possible en vérifiant si la case où le personnage veut se deplacer n'est pas un mur et ne sort pas de la carte. Prend en paramètre les coordonnées de la case en question. Renvoie `True` si le mouvement est autorisé et `False` sinon.
