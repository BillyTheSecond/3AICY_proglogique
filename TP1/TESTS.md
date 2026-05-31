# Tests TP1

J'ai lancé les tests avec :

```bash
python3 TP1/DavisPutman.py
```

## Exemples du code

```text
exo 2 : False avec 4 appels à DP en 4.5e-05 s
exo 3 : True avec 6 appels à DP en 0.000113 s
exo 4 : True avec 9 appels à DP en 0.00038 s

exo 2 : False avec 5 appels à DPLL en 1.9e-05 s
exo 3 : True avec 8 appels à DPLL en 3.5e-05 s
exo 4 : True avec 9 appels à DPLL en 8.1e-05 s
```

## Modele trouve

Pour l'exo 3, DPLL trouve par exemple ce modele :

```text
[-1, 2, -3, 4, 5]
```

Ce qui veut dire :
- a faux
- b vrai
- c faux
- d vrai
- p vrai

## Tous les modeles

J'ai testé sur une petite formule pour ne pas afficher trop de choses :

```text
[[1, 2], [-1, 2]]
```

Resultat :

```text
[[1, 2], [-1, 2]]
```

Donc la variable 2 doit etre vraie, et la variable 1 peut etre vraie ou fausse.

## Fichiers uf50

J'ai testé sur 3 fichiers `uf50`.

```text
uf50-01.cnf avec DP : True avec 514 appels à DP en 0.623343 s
uf50-01.cnf avec DPLL : True avec 550 appels à DPLL en 0.04015 s

uf50-02.cnf avec DP : True avec 637 appels à DP en 0.850464 s
uf50-02.cnf avec DPLL : True avec 770 appels à DPLL en 0.044141 s

uf50-03.cnf avec DP : True avec 251 appels à DP en 0.367996 s
uf50-03.cnf avec DPLL : True avec 272 appels à DPLL en 0.020556 s
```

Les fichiers sont satisfiables, donc `True` c'est normal.
