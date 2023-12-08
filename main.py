# ----------------- TP3 -----------------
# Auteur : Arnaud MOURGUES
# Date : 08/12/2023
# ----------------------------------------
from mip import *

# CONTRAINTES GENERALES
largeur_bande = [245, 283, 255, 271, 292]
largeur_differentes_bandes = [
    [90, 80, 65, 63, 57],
    [110, 92, 80, 74, 70, 65],
    [110, 100, 80, 65, 45],
    [85, 80, 75, 70, 60]]
prix_vente = [
    [15, 12, 10, 9, 7],
    [100, 80, 70, 65, 60],
    [15, 14, 13, 16, 14]
]
contraintes_prix_vente = [
    "Chaque mètre de papier consommé coûte 20 euros",
    "Chaque mètre de papier consommé coûte 120 euros",
    "Chaque mètre de papier consommé coûte 27 euros",
    "Chaque mètre carré de chute correspond à une perte de 2 euros",
    "Chaque mètre carré de chute correspond à une perte de 11 euros",
    "Chaque mètre carré de chute correspond à une perte de 3 euros"
]
contraintes_a_considerer = [
    [0, 2, 4],
    [1, 2, 4],
    [0, 3, 4],
    [1, 3, 4],
    [0, 2, 5],
    [1, 2, 5],
    [0, 3, 5]
]
contraintes = [
    "Longueur total de papier maximale disponible = 1000m",
    "Ne pas produire plus de 400m de chaque bande (A,B,C,D,E,(F)) -> m += A <= 400, m += B <= 400, m += C <= 400, m += D <= 400, m += E <= 400, m += F <= 400",
    "Aucune bande ne peut repréesenter plus de 50% de la longueur de bandes totales produites",
    "Il faut produire assez de chaque bande pour honorer les commandes : A :200m, B :150m, C :215m, D :180m, E :150m (F :100m).",
    "La quantité totale produite de bande A additionnée à celle de la bande C ne doit pas dépasser 750m.",
    "Il faut au moins produire 100m de plus de la bande A que de la bande C"
]


def tp3(num_etudiant):
    # On affiche les informations de l'étudiant
    mes_contraintes = contraintes_a_considerer[num_etudiant % 7]
    prix_vente_etudiant = prix_vente[num_etudiant % 3]
    print("Mon numéro étudiant est : " + str(num_etudiant))
    print("Largeur total de papier disponible correspondant : " + str(largeur_bande[num_etudiant % 5]))
    print("Largeur des bandes correspondantes: " + str(largeur_differentes_bandes[num_etudiant % 4]))
    print("Prix de vente au mètre de chacune des bandes: " + str(prix_vente[num_etudiant % 3]))
    print("Contraintes sur ces bandes: " + str(contraintes_prix_vente[num_etudiant % 6]))
    print("\n Contraintes à considérer: ")
    for i in mes_contraintes:
        print(contraintes[i])

    # La fonction qui va trouver la découpe consiste à trouver l'association de bandes (de liste_bandes) qui est
    # inférieure ou égale au paramètre largeur.
    bandes_finales = []
    largeur_bande_etudiant = largeur_differentes_bandes[num_etudiant % 4]
    # on ne peut pas jeter plus de la plus petite bande de papier, car sinon on pourrait l'ajouter dans une découpe
    # papier_waste_max sera notre condition d'arrêt, si on ne peut pas découper plus petit que la plus petite bande,
    # on arrête
    papier_waste_max = largeur_bande_etudiant[0]
    for i in range(0, len(largeur_bande_etudiant)):
        if largeur_bande_etudiant[i] < papier_waste_max:
            papier_waste_max = largeur_bande_etudiant[i]
    # nom_liste est la liste des noms des bandes, pour afficher les découpes possibles
    nom_liste = ["A", "B", "C", "D", "E", "F"]

    def trouver_decoupe(liste_bandes, largeur, bande_courante, lettre_liste):
        # si on ne peut pas découper plus, on arrête de boucler
        if largeur < papier_waste_max and largeur >= 0:
            # si on a une découpe possible, donc > 0, on l'ajoute à la liste des découpe possible
            bandes_finales.append(bande_courante)
            return
        elif largeur > 0 and len(liste_bandes) > 0 and largeur >= papier_waste_max:
            for z in range(0, len(liste_bandes)):
                trouver_decoupe(liste_bandes[z:], largeur - liste_bandes[z], bande_courante + str(lettre_liste[z]), lettre_liste[z:])

    trouver_decoupe(largeur_differentes_bandes[num_etudiant % 4], largeur_bande[num_etudiant % 5], "", nom_liste)
    # liste_finale = transformer_liste_en_string(bandes_finales)
    print("\nListe des bandes à considérer : " + str(bandes_finales))
    print("Nombre de découpe possible : " + str(len(bandes_finales)))

    # On commence la modélisation du problème
    # On crée le modèle
    m = Model("TP3 - Découpe de papier", sense=MAXIMIZE)

    # On crée une fonction qui détermine le prix de vente d'une bande
    def prix_vente_bande(bande):
        prix = 0
        for z in range(0, len(bande)):
            # le prix correspond au prix de vente de la bande au mètre * la largeur de la bande (en cm) / 100 (1m=100cm)
            if bande[z] == "A":
                prix += prix_vente_etudiant[0] * largeur_bande_etudiant[0] / 100
            elif bande[z] == "B":
                prix += prix_vente_etudiant[1] * largeur_bande_etudiant[1] / 100
            elif bande[z] == "C":
                prix += prix_vente_etudiant[2] * largeur_bande_etudiant[2] / 100
            elif bande[z] == "D":
                prix += prix_vente_etudiant[3] * largeur_bande_etudiant[3] / 100
            elif bande[z] == "E":
                prix += prix_vente_etudiant[4] * largeur_bande_etudiant[4] / 100
            elif bande[z] == "F":
                try:
                    prix += prix_vente_etudiant[5] * largeur_bande_etudiant[5] / 100
                except IndexError:
                    pass
        return prix

    # On crée les variables
    index = [i for i in range(0, len(bandes_finales))]
    varname = bandes_finales
    var = [m.add_var(v) for v in varname]

    # On crée la fonction objectif
    m.objective = xsum(var[i] * prix_vente_bande(bandes_finales[i]) for i in index)

    # On crée les contraintes
    # Pour le numéro étudiant 22307975, on a les contraintes 0, 2 et 4

    # On fait une fonction qui calcul la taille d'une bande
    def calcul_taille_bande(bande):
        taille = 0
        for z in range(0, len(bande)):
            if bande[z] == "A":
                taille += largeur_differentes_bandes[num_etudiant % 4][0]
            elif bande[z] == "B":
                taille += largeur_differentes_bandes[num_etudiant % 4][1]
            elif bande[z] == "C":
                taille += largeur_differentes_bandes[num_etudiant % 4][2]
            elif bande[z] == "D":
                taille += largeur_differentes_bandes[num_etudiant % 4][3]
            elif bande[z] == "E":
                taille += largeur_differentes_bandes[num_etudiant % 4][4]
            elif bande[z] == "F":
                try:
                    taille += largeur_differentes_bandes[num_etudiant % 4][5]
                except IndexError:
                    pass
        return taille

    # contraite 0
    m += xsum(var[i] * calcul_taille_bande(bandes_finales[i]) for i in index) <= 100000

    # contrainte 2
    # on récupère toutes les bandes contenant du A, B, C, D, E, ou F
    bandes_finales_int = []
    bandes_intermediaires = []
    i = 0
    j = 0
    for lettres in nom_liste:
        for bandes in bandes_finales:
            if lettres in bandes:
                bandes_intermediaires.append(j)
            j += 1
        bandes_finales_int.append(bandes_intermediaires)
        bandes_intermediaires = []
        j = 0
        i += 1
    # on supprime la case de la bande F si elle est vide
    if len(bandes_finales_int[5]) == 0:
        bandes_finales_int.pop(5)

    # on crée une fonction pour compter les occurences d'une lettre dans une string
    def count_letter(letter, string):
        count = 0
        for z in string:
            if letter in z:
                count += 1
        return count

    count = 0
    # on ajoute les contraintes
    for i in bandes_finales_int:
        m += xsum(var[j] * count_letter(nom_liste[count], bandes_finales[j]) for j in i) <= 0.5 * xsum(var[j] for j in index)
        count += 1

    # contrainte 4
    m += xsum(var[i] * count_letter("A", bandes_finales[i]) for i in bandes_finales_int[0]) - xsum(var[i] * count_letter("C", bandes_finales[i]) for i in bandes_finales_int[2]) >= 100

    # On lance l'optimisation
    m.optimize()

    # On affiche le résultat
    if m.status == OptimizationStatus.OPTIMAL:
        # affichage du resultat
        for i in index:
            print(varname[i] + " = " + str(var[i].x))
        print("cout total :" + str(m.objective_value))
    else:
        print("Pas de solution possible")


if __name__ == '__main__':
    tp3(22307975)
