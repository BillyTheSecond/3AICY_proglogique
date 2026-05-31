import time

# return True if the list of integers contains a integer and its opposite
# ex.is_tautologie([1,2,3,-1,5]) return True because it contains 1 and -1
# OPTIMISATION: On peut faire un set de la clause pour une recherche en O(1) au lieu de O(n)
# Les tests d'appartenance dans les sets sont bien plus rapides que dans les listes
def is_tautologie(clause:list)->bool:
    clause_set = set(clause)
    for i in clause:
        op_i = -i
        if op_i in clause_set: return True
    return False

# OPTIMISATION : RAS
def regle_1(clauses:list)->list:
    """Règle 1 : oter tautologie -> clause contenant l et non l"""
    l2 = []
    for c in clauses:
        if not is_tautologie(c): l2.append(c)
    if verbose: 
        if not clauses == l2: 
            print("règle 1 activée")
    return l2

l1 = [[1,2],[1,4,-1], [8,1,6,4,9,1,-6], [-2, 4], [1]]

################################################

def ote_val_from_clauses(clauses:list, value:int)->list:
    liste2 = []
    for c in clauses:
        c2 = [i for i in c if i != value] 
        liste2.append(c2)
    return liste2

def ote_clauses_with_val(clauses:list, value:int)->list:
    liste2 = []
    for c in clauses:
        if not value in c: 
            liste2.append(c)
    return liste2


def regle_2(clauses:list)->list:
    """Règle 2 : clause contient 1 seul littéral -> enlever les clauses le contenant, et enlever l'apparition de son inverse ailleurs"""
    for c in clauses:
        if len(c) == 1:
            value = c[0]
            clauses2 = ote_clauses_with_val(clauses, value)
            clauses3 = ote_val_from_clauses(clauses2, -value)
            if verbose: print("regle 2 activee, retrait de ", value)
            return clauses3
    return clauses

l2 = [[1],[1,2], [1,6,4], [-2, 4], [-1,7]]

################################################

# OPTIMISATION : Je ne vois rien n'à optimiser
# ici, un set serait contre productif.
def exist_in_clauses(value:int, clauses:list)->bool:
    """retourne vrai si la valeur value existe dans au moins une clause"""
    for c in clauses:
        if value in c: return True
    return False




# OPTIMISATION : on détecte tous les littéraux purs en une seule fois.
# ça évite de rescanner les clauses pour chaque littéral et permet de
# supprimer plusieurs clauses satisfaites d'un coup.
def multiple_lit(clauses:list)->list:
    """retourne tous les littéraux purs présents dans les clauses"""
    positifs = set()
    negatifs = set()

    for c in clauses:
        for lit in c:
            if lit > 0:
                positifs.add(lit)
            else:
                negatifs.add(-lit)
 

    pure_pos = positifs - negatifs 
    pure_neg = negatifs - positifs
    return [*pure_pos, *(-lit for lit in pure_neg)]

def single_lit(clauses:list)->int:
    """retourne un literal qui apparait dans des clauses mais dont l'opposé n'apparait jamais"""

    for c in clauses:
        for i in c: 
            if not exist_in_clauses(-i, clauses): return i
    return 0


# O ptimisation : au lieu de retirer un seul littéral pur, on retire tous les
#   littéraux purs présents dans la formule. On accélère ainsi la propagation
#   et on réduit le nombre d'appels récursifs.

def regle_3(clauses:list)->list:
    """Règle 3 : élimination des littéraux purs.

    """
    # on modifie cette section pour tout faire d'une traite au lieu de faire un seul retrait à la fois
    purs = multiple_lit(clauses)
    # ----
    if purs:
        purs_set = set(purs)
        clauses2 = [c for c in clauses if not any(lit in purs_set for lit in c)]
        if verbose: print("regle 3 activee, retrait des littéraux purs ", purs)
        return clauses2
    return clauses

l3 = [[1,2], [1,6,4], [-2, 4]]

################################################

# OPTIMISATION : On peut faire un set des clauses et des clauses2
def bigger_clauses(clauses: list) -> list:
    """Retourne les clauses qui contiennent strictement une autre clause."""
    clauses2 = []

    # on parcourt toutes les paires de clauses et on ajoute à clauses2 celles qui contiennent strictement une autre clause
    for c in clauses:
        c_set = set(c)

        # on parcourt toutes les clauses pour vérifier si c en contient une autre
        for c2 in clauses:
            c2_set = set(c2)

            # si c2 est strictement contenu dans c
            if c != c2 and len(c) > len(c2):
                if c2_set <= c_set:
                    # on l'ajoute à clauses2 et on stoppe
                    clauses2.append(c)
                    break

    return clauses2




# NOTE :  Il y aurait un bug si on a 2 fois al même clause - "bigger_clauses"

def regle_4(clauses:list)->list:
    """Règle 4 : si une  clause est contenue dans d'autres -> enlever les autres"""
    clauses2 = bigger_clauses(clauses)
    clauses3 = [c for c in clauses if c not in clauses2]
    if verbose: 
        if clauses2!=[]:print("regle 4 activee, retrait des clause qui contiennent ", clauses2)
    return clauses3

"""
Que fais cette fonction regle_4 :
- on parcourt toutes les paires de clauses et on ajoute à clauses2 celles qui contiennent strictement une autre clause
- on retourne les clauses qui ne sont pas dans clauses2 (clauses3)
Il n'y a pas grad chose à optimiser ici, c'est plsu dans bigger_clauses

"""


l4 = [[1,2], [1,6,4], [1,2, 4], [1,6]]

################################################

def get_not_single(clauses:list)->int:
    """retourne un littéral l dont son inverse apparaît également.

    Optimisation : on choisit le littéral le plus fréquent parmi ceux qui ont
    leur opposé. Cela donne souvent une coupure plus forte dans la règle 5.
    """
    frequences = {}
    for c in clauses:
        for lit in set(c):
            frequences[lit] = frequences.get(lit, 0) + 1

    meilleur_lit = 0
    meilleur_score = -1
    for lit, nb in frequences.items():
        if -lit in frequences:
            score = nb + frequences[-lit]
            if score > meilleur_score:
                meilleur_score = score
                meilleur_lit = lit

    return meilleur_lit


def regle_5(clauses:list)->list:
    """Règle 5 : Créer des mondes -> choisir un littéral l dont son inverse apparaît également 
    -> créer 2 formules,
    - F1) contenant les clauses de F sauf celles contenant l
         et où les apparitions de ¬l sont ôtées
    - F2) contenant les clauses de F sauf celles contenant ¬l
      et où les apparitions de l sont ôtées
    """
    l = get_not_single(clauses)
    if l != 0:
        clauses21 = ote_clauses_with_val(clauses, l)
        clauses31 = ote_val_from_clauses(clauses21, -l)
        clauses22 = ote_clauses_with_val(clauses, -l)
        clauses32 = ote_val_from_clauses(clauses22, l)
        if verbose: print("regle 5 activee, creation de deux mondes à partir de ", l," et de ", -l )
        return (clauses31, clauses32)
        
l5 = [[1,2], [1,6,4], [-1,2, 4], [5,6], [4,5,-1]]

################################################

def formules_egales(f1:list, f2:list)->bool:
    """retourne vrai si les formules f1 et f2 sont identiques"""
    ##TODO: utiliser des sorted set pour une "vraie" comparaison
    if len(f1) != len(f2): return False
    for c in f1:
        if c not in f2: return False
    return True

cpt = 0
verbose = False
def DP(clauses:list)->bool:
    """retourne vrai si le DPLL est fini"""
    global cpt
    cpt +=1
    clr1 = regle_1(clauses)
    if len(clr1) == 0: 
        return True
    if [] in clr1: 
        return False
    clr2 = regle_2(clr1)
    if len(clr2) == 0: 
        return True
    if [] in clr2: 
        return False
    if not formules_egales(clr1, clr2): return DP(clr2)
    clr3 = regle_3(clr2)
    if len(clr3) == 0: 
        return True
    if [] in clr3:  
        return False
    if not formules_egales(clr2, clr3): return DP(clr3)
    clr4 = regle_4(clr3)
    if len(clr4) == 0:  
        return True
    if [] in clr4: 
        return False
    if not formules_egales(clr3, clr4): return DP(clr4)
    clr51,clr52 = regle_5(clr4)
    mondes_unis = DP(clr51) or DP(clr52)
    return mondes_unis


def variables_de_formule(clauses:list)->list:
    variables = set()
    for c in clauses:
        for lit in c:
            variables.add(abs(lit))
    return sorted(variables)


def simplifie_par_litteral(clauses:list, literal:int)->list:
    """on suppose literal vrai et on simplifie la formule"""
    clauses2 = []
    for c in clauses:
        if literal in c:
            continue
        c2 = [i for i in c if i != -literal]
        clauses2.append(c2)
    return clauses2


def premier_unitaire(clauses:list)->int:
    for c in clauses:
        if len(c) == 1:
            return c[0]
    return 0


def premier_pur(clauses:list)->int:
    purs = multiple_lit(clauses)
    if purs:
        return purs[0]
    return 0


def choix_dpll(clauses:list)->int:
    """choix du literal pour couper en deux cas"""
    l = get_not_single(clauses)
    if l != 0:
        return l
    for c in clauses:
        if len(c) > 0:
            return c[0]
    return 0


cpt_dpll = 0


def DPLL(clauses:list)->bool:
    """version DPLL, un peu plus directe que DP"""
    global cpt_dpll
    cpt_dpll += 1

    if [] in clauses:
        return False
    if len(clauses) == 0:
        return True

    l = premier_unitaire(clauses)
    if l != 0:
        return DPLL(simplifie_par_litteral(clauses, l))

    l = premier_pur(clauses)
    if l != 0:
        return DPLL(simplifie_par_litteral(clauses, l))

    l = choix_dpll(clauses)
    return DPLL(simplifie_par_litteral(clauses, l)) or DPLL(simplifie_par_litteral(clauses, -l))


def ajoute_au_modele(modele:dict, literal:int):
    variable = abs(literal)
    valeur = literal > 0
    if variable in modele and modele[variable] != valeur:
        return None
    modele2 = modele.copy()
    modele2[variable] = valeur
    return modele2


def modele_en_liste(modele:dict)->list:
    resultat = []
    for variable in sorted(modele):
        if modele[variable]:
            resultat.append(variable)
        else:
            resultat.append(-variable)
    return resultat


def DPLL_modele_rec(clauses:list, modele:dict):
    if [] in clauses:
        return None
    if len(clauses) == 0:
        return modele

    l = premier_unitaire(clauses)
    if l != 0:
        modele2 = ajoute_au_modele(modele, l)
        if modele2 is None:
            return None
        return DPLL_modele_rec(simplifie_par_litteral(clauses, l), modele2)

    l = premier_pur(clauses)
    if l != 0:
        modele2 = ajoute_au_modele(modele, l)
        if modele2 is None:
            return None
        return DPLL_modele_rec(simplifie_par_litteral(clauses, l), modele2)

    l = choix_dpll(clauses)

    modele_positif = ajoute_au_modele(modele, l)
    if modele_positif is not None:
        resultat = DPLL_modele_rec(simplifie_par_litteral(clauses, l), modele_positif)
        if resultat is not None:
            return resultat

    modele_negatif = ajoute_au_modele(modele, -l)
    if modele_negatif is not None:
        return DPLL_modele_rec(simplifie_par_litteral(clauses, -l), modele_negatif)

    return None


def DPLL_modele(clauses:list)->list:
    resultat = DPLL_modele_rec(clauses, {})
    if resultat is None:
        return []
    return modele_en_liste(resultat)


def complete_modele(modele:dict, variables:list)->list:
    """si une variable n'est pas decidée, on met les deux cas possibles"""
    if len(variables) == 0:
        return [modele]

    variable = variables[0]
    reste = variables[1:]

    if variable in modele:
        return complete_modele(modele, reste)

    modele_vrai = modele.copy()
    modele_vrai[variable] = True
    modele_faux = modele.copy()
    modele_faux[variable] = False
    return complete_modele(modele_vrai, reste) + complete_modele(modele_faux, reste)


def tous_les_modeles_rec(clauses:list, modele:dict, variables:list)->list:
    if [] in clauses:
        return []
    if len(clauses) == 0:
        modeles_complets = complete_modele(modele, variables)
        return [modele_en_liste(m) for m in modeles_complets]

    l = premier_unitaire(clauses)
    if l != 0:
        modele2 = ajoute_au_modele(modele, l)
        if modele2 is None:
            return []
        return tous_les_modeles_rec(simplifie_par_litteral(clauses, l), modele2, variables)

    l = choix_dpll(clauses)
    modeles = []

    modele_positif = ajoute_au_modele(modele, l)
    if modele_positif is not None:
        modeles += tous_les_modeles_rec(simplifie_par_litteral(clauses, l), modele_positif, variables)

    modele_negatif = ajoute_au_modele(modele, -l)
    if modele_negatif is not None:
        modeles += tous_les_modeles_rec(simplifie_par_litteral(clauses, -l), modele_negatif, variables)

    return modeles


def tous_les_modeles(clauses:list)->list:
    variables = variables_de_formule(clauses)
    return tous_les_modeles_rec(clauses, {}, variables)


def lire_cnf(fichier):
    """
    Lit un fichier CNF en format DIMACS et retourne une liste de listes représentant les clauses.

    :param fichier: Le chemin du fichier CNF à lire au format DIMACS comme : 
    p cnf 3 4
    -1 2 0
    -2 3 0
    1 0
    -3 0
    :return: Une liste de listes où chaque sous-liste représente une clause. comme : 
    [[-1,2], [-2,3], [1], [3]]
    """
    clauses = []

    with open(fichier, 'r') as f:
        for ligne in f:
            if ligne.startswith("%"):break
            # Ignorer les lignes de commentaires et le préambule
            if ligne.startswith('c') or ligne.startswith('p'):
                continue
            
            # Diviser la ligne en entiers
            literals = list(map(int, ligne.split()))
            
            # Retirer le 0 de fin de clause
            if literals[-1] == 0:
                literals.pop()
            
            # Ajouter la clause à la liste des clauses
            if literals:
                clauses.append(literals)

    return clauses


exo4 = [[1, -2, 3, -4, -5, -6], [2, 3], [2, 3, 4, 7, 6], [2, -4, 7, -5], [2, -3, 8, -6], [2, -4, 5, -8], [-2, -3], [-2, -3, -4], [-2, 3, 4], [-2, -4, 7], [-2, -7, 5], [-8, -6], [8, 6], [-8, 6]]

# p = 1
# q = 2
# r = 3
# s = 4
# t = 5
# exo2 = [[p, q], [-p, r], [-q, r, s], [-r], [-s], [-t] ]
exo2 = [[1, 2], [-1, 3], [-2, 3, 4], [-3], [-4], [-5] ]

a = 1
b = 2
c = 3
d = 4
p = 5
exo3 = [[a,b], [-a, c], [-b, d], [-c, p], [-d, p], [-p, -c]]


def __main__():
    global cpt, cpt_dpll

    print("Tests sur les exemples du code")

    for nom, formule in [("exo 2", exo2), ("exo 3", exo3), ("exo 4", exo4)]:
        cpt = 0
        debut = time.perf_counter()
        resultat = DP(formule)
        duree = time.perf_counter() - debut
        print(nom, ": ", resultat, " avec ", cpt, " appels à DP en ", round(duree, 6), "s")

    for nom, formule in [("exo 2", exo2), ("exo 3", exo3), ("exo 4", exo4)]:
        cpt_dpll = 0
        debut = time.perf_counter()
        resultat = DPLL(formule)
        duree = time.perf_counter() - debut
        print(nom, ": ", resultat, " avec ", cpt_dpll, " appels à DPLL en ", round(duree, 6), "s")

    print()
    print("Exemple de modele")
    print("modele exo 3 :", DPLL_modele(exo3))

    print()
    print("Tous les modeles d'une petite formule")
    petite_formule = [[1, 2], [-1, 2]]
    print(petite_formule, ":", tous_les_modeles(petite_formule))

    print()
    print("Tests sur les fichiers uf50 presents")
    for nom_fichier in ["uf50-01.cnf", "uf50-02.cnf", "uf50-03.cnf"]:
        clauses = lire_cnf("TP1/uf50/" + nom_fichier)

        cpt = 0
        debut = time.perf_counter()
        resultat = DP(clauses)
        duree = time.perf_counter() - debut
        print(nom_fichier, "avec DP : ", resultat, " avec ", cpt, " appels à DP en ", round(duree, 6), "s")

        cpt_dpll = 0
        debut = time.perf_counter()
        resultat = DPLL(clauses)
        duree = time.perf_counter() - debut
        print(nom_fichier, "avec DPLL : ", resultat, " avec ", cpt_dpll, " appels à DPLL en ", round(duree, 6), "s")

    print()
    print("Tests uuf50 et uuf150")
    print("Je n'ai pas les fichiers dans le dossier, donc le code est pret mais je ne peux pas les lancer.")

if __name__ == "__main__":
    start_time = time.time()
    __main__()
    end_time = time.time()
    print(f"Temps total d'exécution: {end_time - start_time} secondes")
