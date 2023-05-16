# Search - A game of shortest path

## Pour lancer le jeu et jouer

Pour lancer le jeu, il suffit de lancer le fichier `main.py` dans le dossier `src`.
  
  ```python main.py```

Utiliser un clavier AZERTY pour jouer.

Le joueur 1 utilise les touches `zqsd` pour bouger et `a` pour tirer.

Le joueur 2 utilies les flèches pour bouger et `p` pour tirer.

## Description du jeu

Les joueurs 1 et 2 peuvent se promener dans un labirynthe et tirer des projectiles. Deux enemies aveugles sont egalement génerer, ils utilisent les ondes ultrasonnores pour detecter les joueurs et les poursuivre (ces ondes sont fortement atténués donc ont une portée limitée). Le but du jeu est de survivre le plus longtemps possible. Des portails apparaisent aleatoirement sur la carte mais méfie toi, ils peuvent t'aider a échapper où te bloquer dans un coin.

## Dépendences

- tkinter
- numpy
- pillow

Pour telecharger ces dépendences, il suffit d'executer la commande suivante dans un terminal :

```pip install <nom de la dépendence>```
