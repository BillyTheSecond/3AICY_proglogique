from pysat.solvers import Glucose3


k = 5
nbr = 12

REGIONS = [
    "Hauts-de-France",
    "Normandie",
    "Ile-de-France",
    "Grand Est",
    "Bretagne",
    "Pays de la Loire",
    "Centre-Val de Loire",
    "Bourgogne-Franche-Comte",
    "Nouvelle-Aquitaine",
    "Auvergne-Rhone-Alpes",
    "Occitanie",
    "PACA",
]

ADJACENCES = [
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 4),
    (1, 5),
    (2, 3),
    (2, 6),
    (2, 7),
    (3, 7),
    (4, 5),
    (5, 6),
    (5, 8),
    (6, 7),
    (6, 8),
    (6, 9),
    (6, 10),
    (7, 9),
    (8, 9),
    (8, 10),
    (9, 10),
    (9, 11),
    (10, 11),
    (1, 6),
]

# on les mets en couleur pour que ce soit plus joli dans le terminal

COULEURS = ["Rouge", "Vert", "Bleu", "Jaune", "Rose"]
COULEURS_TERMINAL = [
    "\033[31mRouge\033[0m",
    "\033[32mVert\033[0m",
    "\033[34mBleu\033[0m",
    "\033[33mJaune\033[0m",
    "\033[35mRose\033[0m"
]


def x(r, c, k=4):
    return r * k + c + 1


def au_moins_une_couleur(model):
    for r in range(nbr):
        liste = [x(r, i) for i in range(k)]
        # on ajoute la clause x1 OU X2 OU X3 ... OU Xn
        model.add_clause(liste)


def au_plus_une_couleur(model):
    for r in range(nbr):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                # ici on cherche à ne jamais avoir deux fois une couleur pour un x
                model.add_clause([-x(r, c1), -x(r, c2)])


def contraintes_adjacences(model, adjacences):
    for r1, r2 in adjacences:
        for c in range(k):
            # on cherche à ne pas avoir de couleurs qui se touchent
            # donc on va chercher les couples d'adjacence
            model.add_clause([-x(r1, c), -x(r2, c)])


def construire_le_modele():
    model = Glucose3()
    au_moins_une_couleur(model)
    au_plus_une_couleur(model)
    contraintes_adjacences(model, ADJACENCES)
    return model


def couleur_region(modele, region):
    for c in range(k):
        if x(region, c) in modele:
            return c
    return None


def afficher_solution(modele):
    for r in range(nbr):
        c = couleur_region(modele, r)
        print(REGIONS[r], ":", COULEURS_TERMINAL[c])


def main():
    model = construire_le_modele()
    # afficher le nombre de clauses
    print("Nombre de clauses :", model.nof_clauses())

    # résoudre le modèle
    if model.solve():
        modele = model.get_model()
        print("Solution trouvee :")
        afficher_solution(modele)
    else:
        print("Pas de solution.")


if __name__ == "__main__":
    main()



"""
J'ai tenté avec 5 couleurs, 4 couleurs puis 3.

Pour 3 couleurs, on obtient une résolution impossible"Pas de solution"

Donc 4 est la valeur minimale de k possible pour ce problème.


"""