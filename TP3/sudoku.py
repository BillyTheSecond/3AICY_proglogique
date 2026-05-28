from pysat.solvers import Glucose3


def x(i, j, k):
    return (i - 1) * 81 + (j - 1) * 9 + k


def au_moins_une(model):
    for i in range(1, 10):
        for j in range(1, 10):
            # on ajoute la clause x(1, 1, 1) OU x(1, 1, 2) OU ... OU x(1, 1, 9)
            # pour que chaque case ait au moins une valeur
            model.add_clause([x(i, j, k) for k in range(1, 10)])


def au_plus_une(model):
    for i in range(1, 10):
        for j in range(1, 10):
            for k1 in range(1, 10):
                for k2 in range(k1 + 1, 10):
                    # on interdit d'avoir deux valeurs differentes dans la meme case
                    model.add_clause([-x(i, j, k1), -x(i, j, k2)])


def contraintes_lignes(model):
    for i in range(1, 10):
        for k in range(1, 10):
            for j1 in range(1, 10):
                for j2 in range(j1 + 1, 10):
                    # sur une meme ligne, le chiffre k ne peut pas etre dans deux colonnes
                    model.add_clause([-x(i, j1, k), -x(i, j2, k)])


def contraintes_colonnes(model):
    for j in range(1, 10):
        for k in range(1, 10):
            for i1 in range(1, 10):
                for i2 in range(i1 + 1, 10):
                    # pareil que les lignes mais dans une colonne
                    model.add_clause([-x(i1, j, k), -x(i2, j, k)])


def contraintes_blocs(model):
    for debut_i in [1, 4, 7]:
        for debut_j in [1, 4, 7]:
            for k in range(1, 10):
                cases = []
                for i in range(debut_i, debut_i + 3):
                    for j in range(debut_j, debut_j + 3):
                        cases.append((i, j))

                for c1 in range(len(cases)):
                    for c2 in range(c1 + 1, len(cases)):
                        i1, j1 = cases[c1]
                        i2, j2 = cases[c2]
                        # dans un bloc 3x3, on ne veut pas deux fois le même chiffre
                        model.add_clause([-x(i1, j1, k), -x(i2, j2, k)])


def build_sudoku_solver():
    solver = Glucose3()
    au_moins_une(solver)
    au_plus_une(solver)
    contraintes_lignes(solver)
    contraintes_colonnes(solver)
    contraintes_blocs(solver)
    return solver


def display_solution(model):
    grille = [[0 for _ in range(9)] for _ in range(9)]
    modele = model.get_model()

    for i in range(1, 10):
        for j in range(1, 10):
            for k in range(1, 10):
                if modele[x(i, j, k) - 1] > 0:
                    grille[i - 1][j - 1] = k

    for ligne in grille:
        print(" ".join(str(k) for k in ligne))


def add_indices(model, indices):
    for i, j, k in indices:
        # un indice est juste une clause avec une seule variable positive
        model.add_clause([x(i, j, k)])


INDICES = [
    (1, 2, 3),
    (1, 4, 7),
    (2, 3, 2),
    (2, 7, 6),
    (3, 1, 8),
    (3, 5, 1),
    (3, 6, 3),
    (3, 9, 5),
    (4, 2, 6),
    (4, 5, 7),
    (4, 6, 4),
    (4, 7, 5),
    (5, 1, 4),
    (5, 4, 9),
    (6, 4, 8),
    (6, 9, 7),
    (7, 6, 9),
    (8, 1, 3),
    (8, 5, 4),
    (8, 6, 5),
    (8, 9, 1),
    (9, 2, 8),
    (9, 8, 3),
]









if __name__ == "__main__":
    print("x(1, 1, 1) =", x(1, 1, 1))
    print("x(9, 9, 9) =", x(9, 9, 9))

    model = Glucose3()
    au_moins_une(model)
    print("Nombre de clauses apres au_moins_une :", model.nof_clauses())

    au_plus_une(model)
    print("Nombre de clauses apres au_plus_une :", model.nof_clauses())

    contraintes_lignes(model)
    print("Nombre de clauses apres contraintes_lignes :", model.nof_clauses())

    contraintes_colonnes(model)
    print("Nombre de clauses apres contraintes_colonnes :", model.nof_clauses())

    contraintes_blocs(model)
    print("Nombre de clauses apres contraintes_blocs :", model.nof_clauses())

    print()
    print("Resolution du sudoku donne :")
    sudoku = build_sudoku_solver()
    print("Nombre de clauses sans les indices :", sudoku.nof_clauses())
    add_indices(sudoku, INDICES)
    print("Nombre d'indices ajoutes :", len(INDICES))
    print("Nombre de clauses avec les indices :", sudoku.nof_clauses() + len(INDICES))

    if sudoku.solve():
        display_solution(sudoku)
    else:
        print("Pas de solution.")
