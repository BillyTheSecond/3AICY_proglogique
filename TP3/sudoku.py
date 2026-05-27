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

# je n'ai pas encore terminé









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
