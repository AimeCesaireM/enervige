import sys, getopt, string, math

# Alphabet français/anglais
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Fréquence moyenne des lettres en français
# À modifier
freq_FR = [0.09213414037491088, 0.010354463742221126, 0.030178915678726964,
           0.03753683726285317, 0.17174710607479665, 0.010939030914707838,
           0.01061497737343803, 0.010717912027723734, 0.07507240372750529,
           0.003832727374391129, 6.989390105819367e-05, 0.061368115927295096,
           0.026498684088462805, 0.07030818127173859, 0.049140495636714375,
           0.023697844853330825, 0.010160031617459242, 0.06609294363882899,
           0.07816806814528274, 0.07374314880919855, 0.06356151362232132,
           0.01645048271269667, 1.14371838095226e-05, 0.004071637436190045,
           0.0023001447439151006, 0.0012263202640210343]

freq_EN = [
    0.084966,  # A
    0.020720,  # B
    0.045388,  # C
    0.033844,  # D
    0.111607,  # E
    0.018121,  # F
    0.024705,  # G
    0.030034,  # H
    0.075448,  # I
    0.001965,  # J
    0.011016,  # K
    0.054893,  # L
    0.030129,  # M
    0.066544,  # N
    0.071635,  # O
    0.031671,  # P
    0.001962,  # Q
    0.075809,  # R
    0.057351,  # S
    0.069509,  # T
    0.036308,  # U
    0.010074,  # V
    0.012899,  # W
    0.002902,  # X
    0.017779,  # Y
    0.002722   # Z
]


# Chiffrement César
def chiffre_cesar(txt, key):
    """
    Chiffre un texte avec le chiffrement César
    Args:
        txt (str): Le texte à chiffrer
        key (int): La clé de chiffrement
    Returns:
        str: Le texte chiffré
    """
    encrypted = ""
    for c in txt:
        encrypted += alphabet[(alphabet.index(c) + key) % len(alphabet)]
    return encrypted


# Déchiffrement César
def dechiffre_cesar(txt, key):
    """
    Déchiffre un texte avec le chiffrement César
    Args:
        txt (str): Le texte à déchiffrer
        key (int): La clé de chiffrement
    Returns:
        str: Le texte déchiffré
    """
    decrypted = ""
    for c in txt:
        decrypted += alphabet[(alphabet.index(c) - key) % len(alphabet)]
    return decrypted


# Chiffrement Vigenere
def chiffre_vigenere(txt, key):
    """
    Chiffre un texte avec le chiffrement Vigenere
    Args:
        txt (str): Le texte à chiffrer
        key (str): La clé de chiffrement
    Returns:
        str: Le texte chiffré
    """
    encrypted = ""

    def encryptChar(char, decalage):
        return alphabet[(alphabet.index(char) + decalage) % len(alphabet)]

    for position, ch in enumerate(txt):
        encrypted += encryptChar(ch, key[position % len(key)])

    return encrypted


# Déchiffrement Vigenere
def dechiffre_vigenere(txt, key):
    """
    Déchiffre un texte avec le chiffrement Vigenere
    Args:
        txt (str): Le texte à déchiffrer
        key (list): La clé de chiffrement
    Returns:
        str: Le texte déchiffré
    """

    def decryptChar(char, decalage):
        # print(char, decalage)
        return alphabet[(alphabet.index(char) - decalage) % len(alphabet)]

    decrypted = ""
    for position, ch in enumerate(txt):
        decrypted += decryptChar(ch, key[position % len(key)])

    return decrypted


# Analyse de fréquences
def freq(txt):
    """
    Cree un histograme de fréquences des lettres d'un texte
    Args:
        txt (str): Le texte à analyser
    Returns:
        list: Une liste de fréquences des lettres arrangees par index de l'alphabet
    """
    hist = [0.0] * len(alphabet)
    for c in txt:
        hist[alphabet.index(c)] += 1
    return hist


# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """
    Donne la lettre la plus fréquente d'un texte
    Args:
        txt (str): Le texte à analyser
    Returns:
        int: L'indice de cette lettre dans l'alphabet
    """
    l = freq(txt)
    return l.index(max(l))


# indice de coïncidence
def indice_coincidence(hist):
    """
    Calcule l'indice de coïncidence d'un texte
    Args:
        hist (list): L'histograme de fréquences des lettres du texte
    Returns:
        float: L'indice de coïncidence
    """
    ic = 0.0
    n = sum(hist)
    if n <= 1:
        return 0.0
    for i in range(len(alphabet)):
        ic += (hist[i] * (hist[i] - 1) / (n * (n - 1)))
    return ic


def columnsExtractor(cipher, key_length):
    """
    Renvoie les colonnes d'un texte divisee par une clef de facon Vigenere.
    Divise le texte en liste de colonnes; la liste est de longueur key_length
    Args:
        cipher (str): Le texte à diviser
        key_length (int): La longueur de la liste (= la longueur de la clé)
    Returns:
        list: Une liste de colonnes de longueur key_length
    """
    columns = [""] * key_length
    for index, char in enumerate(cipher):
        columns[index % key_length] += char
    return columns


def constructTextFromColumns(columns):
    """
    Construit le texte d'une liste de colonnes qui etaient divisées par columnsExtractor()
    Args:
        columns (list): Une liste de colonnes du texte
    Returns:
        str: Le texte construit
    """
    key_length = len(columns)
    text = ""
    cipher_length = sum([len(col) for col in columns])
    for i in range(cipher_length):
        index = i % key_length
        text += columns[index][i // key_length]
    return text


# Recherche la longueur de la clé
def longueur_clef(cipher):
    """
    Cherche la longueur de la clé en essayant plusieurs longueurs de cles et
    calcualant la moyenne des indices de coïncidence des colonnes pour chaque
    longueur de clé.
    Args:
        cipher (str): Le texte
    Returns:
        int: La longueur de la clé
    """
    MAX_KEY_LENGTH = 20

    for key_length in range(1, MAX_KEY_LENGTH + 1):
        columns = columnsExtractor(cipher, key_length)
        hists = [freq(col) for col in columns]
        indices = [indice_coincidence(h) for h in hists]
        average = sum(indices) / len(indices)

        if average > 0.06:
            return key_length

    return 0


# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Renvoie le tableau des décalages probables, etant
    donné la longueur de la clé en utilisant la lettre
    la plus fréquente de chaque colonne.
    La lettre la plus fréquente de chaque colonne est considerée
    comme le chiffre du caractère E.
    Args:
        cipher (str): Le texte
        key_length (int): La longueur de la clé
    Returns:
        list: Le tableau des décalages probables
    """
    decalages = [0] * key_length
    columns = columnsExtractor(cipher, key_length)
    for index, col in enumerate(columns):
        mostFrequentIndex = lettre_freq_max(col)
        decalageRaw = mostFrequentIndex - alphabet.index("E")
        if decalageRaw < 0:
            decalageRaw += len(alphabet)
        decalages[index] = decalageRaw

    return decalages


# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """
    Renvoie le texte déchiffré.
    Dechiffre un texte en utilisant les decalages suggerés par clef_par_decalages()
    Chaque lettre est dechiffree en utilisant le decalage correspondant à ca colonne.
    Args:
        cipher (str): Le texte à dechiffrer
    Returns:
        str: Le texte déchiffré

    Seulement 18 textes sur 100 sont correctement crytanayses et dechiffres.
    Divers raison pour cela:
        - si le texte est trop court, le calcul de l'index de coincidence peut etre different du vrai IC pour la veritable
        longeur de cle. Donc, pour une longeur non-correcte, on peut calculer une moyenne de plus de 0.06
        des textes Francais 'standards'
        - si la lettre la plus frequente n'est pas 'E', clef_par_decalages() est suscetibles a ce tromper et a renvoyer
        la mauvaise cle pour le dechiffrement'
        - si la cle est plus longue que 20 caracteres, notre programme ne cryptanalysera pas le chiffre correctement.
        - Si le texte claire a beaucoup des repetitions, cela peut biaser nos calculs de l'IC qui ensuite nous donne
        la mauvaise longeur de clef.
    """

    key_length = longueur_clef(cipher)
    decalages = clef_par_decalages(cipher, key_length)
    decrypted = ""
    for index, char in enumerate(cipher):
        diff = alphabet.index(char) - decalages[index % key_length]
        if diff < 0:
            diff += len(alphabet)
        decrypted += alphabet[diff]
    return decrypted


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1, h2, d):
    """
    Renvoie l'indice de coincidence mutuelle entre deux textes.
    Args:
        h1 (list): L'histograme de fréquences des lettres du texte 1
        h2 (list): L'histograme de fréquences des lettres du texte 2, qui on assume est decale de d.
    Returns:
        float: L'indice de coincidence mutuelle avec le decalage d
    """
    n1 = sum(h1)
    n2 = sum(h2)
    icm = 0.0
    for i in range(len(alphabet)):
        icm += (h1[i] * h2[(i + d) % len(alphabet)]) / (n1 * n2)
    return icm


# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Renvoie le tableau des décalages probables, etant
    donné la longueur de la clé en comparant l'indice
    de décalage mutuel par rapport à la première colonne.
    Pour chaque colonne, on choisi le decalage qui maximise
    l'indice de coincidence mutuel avec la première colonne.
    Args:
        cipher (str): Le texte
        key_length (int): La longueur de la clé
    Returns:
        list: Le tableau des décalages probables
    """
    decalages = [0] * key_length
    cols = columnsExtractor(cipher, key_length)
    f0 = freq(cols[0])

    for i, c in enumerate(cols):
        f = freq(c)
        max_icm = 0.0
        max_decalage = 0.0
        for d in range(len(alphabet)):
            icm = indice_coincidence_mutuelle(f0, f, d)
            if icm > max_icm:
                max_decalage = d
                max_icm = icm
        decalages[i] = max_decalage

    return decalages


# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Renvoie le texte déchiffré.
    En premier temps, dechiffrer chaque colonne du texte en utilisant
    les decalages suggerés par tableau_decalages_ICM().Ensuite, dechiffrer
    le texte en utilisant le chiffrement Cesar, on assume que le deuxieme
    decalage est le decalage entre la lettre la plus frequente du premier dechiffre
    et la lettre 'E'.

    43/100 textes sont dechiffres.
    - Cette methode depend toujours d'une analyse de frequences, qui devient infiable avec des textes courts.
    - Cette methode dechiffre plus de textes par ce que l'ICM est plus apte a detecter des repetitions qui avez
    auparavant rendu un indice de coincidence qui ne reflete pas la langue francaise.
    - Aussi, parce que cette methode compare les colones du texte entre elles, elle compare ce texte dans son
    propre contexte statistique, au lieu de le comparer au contexte statistique 'general'.
    Args:
        cipher (str): Le texte à dechiffrer
    Returns:
        str: Le texte déchiffré
    """
    key_length = longueur_clef(cipher)
    decalages = tableau_decalages_ICM(cipher, key_length)
    colonnes = columnsExtractor(cipher, key_length)

    for i in range(len(colonnes)):
        colonnes[i] = dechiffre_cesar(colonnes[i], decalages[i])

    levelOneDecrypted = constructTextFromColumns(colonnes)
    e_chiffre = lettre_freq_max(levelOneDecrypted)

    decalage_final = e_chiffre - alphabet.index("E")

    if decalage_final < 0:
        decalage_final += len(alphabet)
    levelTwoDecrypted = dechiffre_cesar(levelOneDecrypted, decalage_final)

    return levelTwoDecrypted


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1, L2):
    """
    Renvoie la correlation lineaire de Pearson entre deux listes de même taille
    On arrondit la correlation à 10 chiffres apres la virgule parce que Python a
    des soucis avec les floats. Voir: https://docs.python.org/3/tutorial/floatingpoint.html
    Args:
        L1 (list): La premiere liste
        L2 (list): La deuxieme liste
    Returns:
        float: La correlation lineaire de Pearson, arrondie à 10 chiffres apres la virgule.
    """

    def expectedValue(L):
        return sum(L) / len(L)

    def squaredDeviation(L):
        m = expectedValue(L)
        return sum([math.pow((x - m), 2) for x in L])

    def modifiedStdDev(L):
        return math.sqrt(squaredDeviation(L))

    exp1 = expectedValue(L1)
    exp2 = expectedValue(L2)
    numerator = sum([(L1[i] - exp1) * (L2[i] - exp2) for i in range(len(L1))])
    denominator = modifiedStdDev(L1) * modifiedStdDev(L2)
    if denominator == 0:
        raise ValueError('Length too small to calculate a standard deviation')
    return round(numerator / denominator, 10)


# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length, freqs=None):
    """
    Renvoie un tuple de la meilleur clé possible par correlation etant
    donné une longueur de clé et le score de cette clé.
    Pour chaque colonne, on choisi le decalage qui maximise la correlation
    entre l'histogramme de cette colonne et l'histogramme de la langue.
    La cle renvoyee sera la liste des decalages choisis.
    Le score est la moyenne des correlations.
    Args:
        cipher (str): Le texte à dechiffrer
        key_length (int): La longueur de la cle
        freqs (list) : Table de frequence
    Returns:
        (float, list): Un tuple du score et la cle
    """
    if freqs is None:
        freqs = freq_FR
    key = [0] * key_length
    score = 0.0

    columns = columnsExtractor(cipher, key_length)

    for index, col in enumerate(columns):
        key[index] = 0
        max_corr = 0
        for decal in range(len(alphabet)):
            col_dechiffre = dechiffre_cesar(col, decal)
            corr = correlation(freqs, freq(col_dechiffre))
            if corr > max_corr:
                key[index] = decal
                max_corr = corr

        score += max_corr
    score /= key_length

    return score, key

def clef_correlations_anglais(cipher, key_length):
    return clef_correlations(cipher, key_length, freq_EN)




# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Renvoie le texte déchiffré
    Pour chaque longueur de clé possible, on choisi la clé qui maximise le score.
    Apres, on choisi la clé, de ces clés, qui maximise le score.

    94/100 texts dechiffres.
    - Cettw methode utilise la meme logique que l'ICM entre les colones, mais considere toute la relation lineaire
    entre les deux textes plutot que seulement la coincidence mutuelle. Donc elle capture plus d'infos (including l'
    info que l'ICM nous donne.)
    - La correlation Pearson est moins sensitive aux 'outliers' car elle considere les deux ensembles des caracteres.

    - Caracteristiques des textes qui echouent:
        *  Peut etre une clef plus longue que 20 caracteres, ou bien avec un autre ensemble des caracteres
        * Peut etre pas chiffres par la methode Vigenere
        * Textes trop courts
        * Textes avec une distribution uniforme des caracteres (ou meme des textes aleatoires)
        * textes en langues differentes


    Args:
        cipher (str): Le texte à dechiffrer
    Returns:
        str: Le texte déchiffré
    """
    MAX_KEY_LENGTH = 26
    results = []

    for key_length in range(1, MAX_KEY_LENGTH + 1):
        results.append(clef_correlations(cipher, key_length))

    max_score = 0.0
    key = None
    for entry in results:
        if entry[0] > max_score:
            max_score = entry[0]
            key = entry[1]

    decrypted = dechiffre_vigenere(cipher, key)
    return decrypted

def cryptanalyse_v3_anglais(cipher):
    MAX_KEY_LENGTH = 26
    results = []

    for key_length in range(1, MAX_KEY_LENGTH + 1):
        results.append(clef_correlations_anglais(cipher, key_length))

    max_score = 0.0
    key = None
    for entry in results:
        if entry[0] > max_score:
            max_score = entry[0]
            key = entry[1]

    decrypted = dechiffre_vigenere(cipher, key)
    return decrypted



################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################


# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f = open(fichier, "r")
    txt = (f.readlines())[0].rstrip('\n')
    f.close()
    return txt


# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)


def usage():
    print("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)


def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv, "hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier == '':
        usage()
    if not (version == 1 or version == 2 or version == 3):
        usage()

    print("Cryptanalyse version " + str(version) + " du fichier " + fichier + " :")
    print(cryptanalyse(fichier, version))


if __name__ == "__main__":
    main(sys.argv[1:])
