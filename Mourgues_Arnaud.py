# ----------------- TP3 -----------------
# Auteur : Favre Erwan
# Date : 08/12/2023
# ----------------------------------------
from mip import *

# CONTRAINTES GENERALES
listBands = ['A', 'B', 'C', 'D', 'E', 'F']
largeur_bande = [245, 283, 255, 271, 292]
largeur_differentes_bandes = [
    [90, 80, 65, 63, 57],
    [110, 92, 80, 74, 70, 65],
    [110, 100, 80, 65, 45],
    [85, 80, 75, 70, 60]]
prix_vente = [
    [15, 12, 10, 9, 7],
    [100, 80, 70, 65, 60, 57],
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
    print("Largeur total de papier disponible correspondant : " + str(largeur_bande[num_etudiant % 5]) + " avec num_étudiant%5 : " + str(num_etudiant % 5))
    print("Largeur des bandes correspondantes: " + str(largeur_differentes_bandes[num_etudiant % 4]) + " avec num_étudiant%4 : " + str(num_etudiant % 4))
    print("Prix de vente au mètre de chacune des bandes: " + str(prix_vente[num_etudiant % 3]) + " avec num_étudiant%3 : " + str(num_etudiant % 3))
    print("Contraintes sur ces bandes: " + str(contraintes_prix_vente[num_etudiant % 6]) + " avec num_étudiant%6 : " + str(num_etudiant % 6))
    print("\n Contraintes à considérer avec num_etudiant%7 : " + str(num_etudiant % 7) + " : ")
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
                trouver_decoupe(liste_bandes[z:], largeur - liste_bandes[z], bande_courante + str(lettre_liste[z]),
                                lettre_liste[z:])

    trouver_decoupe(largeur_bande_etudiant, largeur_bande[num_etudiant % 5], "", nom_liste)
    print("\nListe des bandes à considérer : " + str(bandes_finales))
    print("Nombre de découpe possible : " + str(len(bandes_finales)))

    def calcul_largeur_bande(bande):
        largeur = 0
        for i in range(0, len(bande)):
            # On récupère l'index de la lettre grâce à ord() et on soustrait 65 car A = 65 en ASCII
            largeur += largeur_bande_etudiant[ord(bande[i]) - 65]
        return largeur

    def calculer_chutes(bandes_finales, largeur):
        chutes = []
        for i in range(0, len(bandes_finales)):
            chutes.append(largeur - calcul_largeur_bande(bandes_finales[i]))
        return chutes

    Dico_Prix_Lettre = {}
    for i in range(0, len(prix_vente[num_etudiant % 3])):
        Dico_Prix_Lettre[chr(65 + i)] = prix_vente[num_etudiant % 3][i]
    print(len(bandes_finales))
    Dico_Prix = {}
    for i in range(0, len(bandes_finales) - 1):
        if (len(bandes_finales[i]) == 2):
            Pv = Dico_Prix_Lettre[bandes_finales[i][0]] + Dico_Prix_Lettre[bandes_finales[i][1]]
            Dico_Prix[bandes_finales[i]] = Pv
        else:
            Pv = Dico_Prix_Lettre[bandes_finales[i][0]] + Dico_Prix_Lettre[bandes_finales[i][1]] + Dico_Prix_Lettre[
                bandes_finales[i][2]]
            Dico_Prix[bandes_finales[i]] = Pv
    print(Dico_Prix)
    # On commence la modélisation du problème
    # On crée le modèle
    m = Model("TP3 - Découpe de papier", sense=MAXIMIZE)

    # On crée les variables
    index = [i for i in range(0, len(bandes_finales))]
    varname = bandes_finales
    var = [m.add_var(v) for v in bandes_finales]

    # Valeur du benef
    total = 0
    for i in range(0, len(bandes_finales)):
        total += var[i]
    benef = xsum(
        Dico_Prix_Lettre[bandes_finales[i][j]] * var[i] for i in range(0, len(bandes_finales)) for j in range(0, len(bandes_finales[i])))
    chutes = calculer_chutes(bandes_finales, largeur_bande[num_etudiant % 5])
    perte = xsum((var[i] * (chutes[i]/100) * 3) for i in range(0, len(bandes_finales)))
    print(perte)
    # On crée la fonction objective
    m.objective = benef - perte

    #

    print(total)

    # Contrainte 0

    m += total <= 1000

    # Contrainte 3
    totalBis = 0
    for i in range(0, len(bandes_finales)):
        totalBis += len(bandes_finales[i]) * var[i]

    def count_letter(letter, string):
        compteur = 0
        for z in string:
            if letter in z:
                compteur += 1
        return compteur

    for i in range(0, len(listBands)):
        m += xsum(var[j] * count_letter(listBands[i], bandes_finales[j]) for j in index) <= 0.5 * totalBis

    # Contraintes 6
    m += (xsum(var[i] * count_letter('A', bandes_finales[i]) for i in index) >=
          100 + xsum(var[i] * count_letter('C', bandes_finales[i]) for i in index))

    # On lance l'optimisation
    m.optimize()

    # On affiche le résultat
    if m.status == OptimizationStatus.OPTIMAL:
        # affichage du resultat
        for i in index:
            print(bandes_finales[i] + " = " + str(var[i].x))
        print("cout total :" + str(m.objective_value))
    else:
        print("Pas de solution possible")


if __name__ == '__main__':
    tp3(22307975)
