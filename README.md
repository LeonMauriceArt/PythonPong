# Jeu P.O.N.G

## Aperçu

Il s'agit d'une implémentation simple du jeu classique Pong en utilisant la bibliothèque Pygame en Python. 
Le jeu prend en charge de 2 à 4 joueurs et inclut des fonctionnalités telles que des powerups.

## Configuration

Avant d'exécuter le jeu, assurez-vous d'avoir la bibliothèque Pygame installée. 
Vous pouvez l'installer en utilisant la commande suivante :

```bash 
pip install pygame
```

## Utilisation

Pour exécuter le jeu, lancez le script depuis la ligne de commande avec un argument facultatif spécifiant le nombre de joueurs (2 à 4). Si aucun argument n'est fourni, la valeur par défaut est fixée à 2 joueurs. Si la valeur est superieur a 4, le nombre de joueur sera fixer a 4.

```bash
python pong_game.py [nombre_de_joueurs]
```

## Structure du Code

Le code est organisé en plusieurs fichiers :

    - config.py : Contient des constantes de configuration pour le jeu.

    - Player.py : Définit la classe Player et des fonctions pour gérer la logique liée aux joueurs.

    - Ball.py : Implémente la classe Ball et des fonctions pour gérer le mouvement de la balle et les collisions.

    - Wall.py : Définit la classe Wall, utilisee pour le powerup mur.

    - Powerup.py : Contient des fonctions et des classes pour gérer les powerups dans le jeu.

## Logique Principale

La fonction main initialise la fenêtre Pygame et configure l'environnement de jeu. 
Elle entre ensuite dans la boucle de jeu, où elle met à jour et rend continuellement l'état du jeu.

## Boucle de Jeu

La boucle de jeu itère continuellement, gérant les entrées des joueurs, mettant à jour les positions des joueurs et de la balle, détectant les collisions et gérant les powerups. 
La boucle se termine lorsqu'un joueur marque un point et que la fenêtre Pygame est fermée.

## Powerups

Le jeu inclut des powerups (config.POWERUP_ENABLE). Les powerups apparaissent à des intervalles aléatoires et disparaissent lorsqu'ils entrent en collision avec la raquette d'un joueur. Les effets effets sont les suivants :

    - REVERSE : Fait une feinte de la balle, qui change de direction.
    - WALL : Fait apparaitre un mur au centre de l'arene pendant un court instant.
    - CURSE : Maudit les joueurs pendant un instant, diminuant la taille de leurs racquettes.