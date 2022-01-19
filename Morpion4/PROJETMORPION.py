import time
import numpy as np
import copy

X = 1
O = 2
STATS = True
Puissance=1
TaillePlateau=12
NombreDeCoupALavance=-1

##Classe Joueur
class Player:
    def __init__(self):
        pass

    def MeilleurEmplacement(self, state):
        choix=""
        while "," not in choix:
            choix = input('Ligne,Colonne : ')
        choix=choix.split(",")
        return (int(choix[0])-1, int(choix[1])-1)

##classe IA
class IA:
    def __init__(self, LimiteTemps=0, ProfondeurMaximaleRecherche=-1, UtilisationDictionnaire=True):
        if LimiteTemps != 0 and ProfondeurMaximaleRecherche != -1:
            print("Si la limite de temps n'est pas 0, ProfondeurMaximaleRecherche sera ignoré")
        self.LimiteTemps = LimiteTemps
        self.ProfondeurMaximaleRecherche = ProfondeurMaximaleRecherche
        self.use_AB = True
        self.UtilisationDictionnaire = True
        self.EtatExplore = 0
        self.Elagage = 0
        self.EtatDejaVu = dict()

    def Evaluation(self, state):
        if self.UtilisationDictionnaire and state in self.EtatDejaVu:
            return self.EtatDejaVu[state]
        score = 0
        lines = state.RecupLigne()
        for l in lines:
            player_counts = {X: np.count_nonzero(l == X), O: np.count_nonzero(l == O)}
            if player_counts[X] == state.allignement:
                score = score + 100**state.taille
                return score
            elif player_counts[O] == state.allignement:
                score = score - 100**state.taille
                return score

            for i in range(state.allignement-1, 0, -1):
                if player_counts[X] == i and player_counts[O] == 0:
                    score = score + (20 **i) * (1/i)
                if player_counts[O] == i and player_counts[X] == 0:
                    score = score - (20 **i) * (1/i)
        return score

    def EmplacementDisponible(self, state):
        EmplacementVide = np.where(state.board == 0)
        return list(zip(EmplacementVide[0], EmplacementVide[1]))

    def EtatSuivant(self, state, move):
        self.EtatExplore += 1
        r = move[0]
        c = move[1]
        NewEtat = Etat(state)
        NewEtat.board[r][c] = state.TourJoueur
        NewEtat.TourJoueur = IA.InversionTour(state.TourJoueur)
        return NewEtat

    def EtatVoisin(self, state):
        return [self.EtatSuivant(state, m) for m in self.EmplacementDisponible(state)]

    def MeilleurEmplacement(self, state):
        EmplacementsPotentiel = self.EmplacementDisponible(state)
        EtatsPotentiel = self.EtatVoisin(state)
        if self.LimiteTemps == 0:
            values = [self.minimax(s, self.ProfondeurMaximaleRecherche) for s in EtatsPotentiel]
        else:
            ProfondeurMaximale = state.taille**2
            ProfondeurActuel = 1
            start_time = time.time()
            values = []
            while time.time() < (start_time + self.LimiteTemps):
                if ProfondeurActuel > ProfondeurMaximale:
                    break
                values = [self.minimax(s, ProfondeurActuel) for s in EtatsPotentiel]
                ProfondeurActuel = ProfondeurActuel+1

            print(f"Profondeur Maximale: {ProfondeurActuel}")
        if state.TourJoueur == X:
            return EmplacementsPotentiel[np.argmax(values)]
        else:
            return EmplacementsPotentiel[np.argmin(values)]

    def minimax(self, state, ProfondeurMaximaleRecherche, alpha=-10e10, beta=10e10):
        if ProfondeurMaximaleRecherche == 0 or state.win():
            return self.Evaluation(state)
        if self.UtilisationDictionnaire and state in self.EtatDejaVu:
            return self.EtatDejaVu[state]
        voisins = self.EtatVoisin(state)

        # Joueur à maximiser
        if state.TourJoueur == X:
            value = -10e10
            for n in voisins:
                value = max(value, self.minimax(n, ProfondeurMaximaleRecherche-1, alpha, beta))
                # A-B
                if self.use_AB:
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        self.Elagage += 1
                        break
            return value

        # Joueur à minimiser
        else:
            value = 10e10
            for n in voisins:
                value = min(value, self.minimax(n, ProfondeurMaximaleRecherche-1, alpha, beta))
                # A-B
                if self.use_AB:
                    beta = min(beta, value)
                    if alpha >= beta:
                        self.Elagage += 1
                        break
        return value

    @staticmethod
    def InversionTour(turn):
        if turn == X:
            return O
        else:
            return X

##Class Etat

class Etat:
    def __init__(self, old=None, taille=12, allignement=4):
        if old is not None:
            self.board = copy.deepcopy(old.board)
            self.TourJoueur = old.TourJoueur
            self.taille = old.taille
            self.allignement = old.allignement
        else:
            if taille < 3:
                return print("La taille du board doit être d'au moins 3x3")
            self.board = np.zeros((taille,taille))
            self.TourJoueur = X
            self.taille = taille
            self.allignement = allignement
            if allignement > taille:
                return print("L'allignement doit être <= taille")

    def __str__(self):
        res = "  " + "".join(str(list(range(1,self.taille+1))).split(","))[1:-1]
        res = res + "\n"
        for r in range(self.taille):
            res = res + str(r+1) + " "
            for c in range(self.taille):
                if self.board[r][c] == X:
                    res = res + "X "
                elif self.board[r][c] == O:
                    res = res + "O "
                else:
                    res = res + "_ "
            res = res + "\n"
        return res

    def __eq__(self, state2):
        return np.all(np.equal(self.board, state2.board)) and self.TourJoueur == state2.TourJoueur

    def __hash__(self):
        return hash(str(self) + str(self.TourJoueur))

    def win(self):
        lines = self.RecupLigne()
        for l in lines:
            player_counts = {X: np.count_nonzero(l == X), O: np.count_nonzero(l == O)}
            if player_counts[X] == self.allignement:
                return "X"
            elif player_counts[O] == self.allignement:
                return "O"

        if np.any(np.where(self.board == 0)):
            return False
        return "D"

    #retourne une liste de toute les lignes du board assez longue pour gagner
    def RecupLigne(self):
        lines = []
        for rc in range(self.taille):
            for i in range(0, self.taille-self.allignement+1):
                # Ligne
                Ligne = self.board[rc, i:i+self.allignement]
                if len(Ligne) <= 2:
                    print(Ligne)
                lines.append(Ligne)
                # colonne
                Colonne = self.board[i:i+self.allignement, rc]
                if len(Colonne) <= 2:
                    print(Colonne)
                lines.append(Colonne)
        # Verifie toutes les diagonales assez longue pour alligner 4 pièces
        for i in range(-self.taille + self.allignement, self.taille-self.allignement+1):
            diagonalle = np.diag(self.board, i)
            diagonalleInverse = np.diag(np.fliplr(self.board), i)
            for diag in [diagonalle, diagonalleInverse]:
                if len(diag) == self.allignement:
                    lines.append(diag)
                else:
                    for j in range(0, len(diag)-self.allignement+1):
                        lines.append(diag[j:j+self.allignement])
        return lines

##Jeu
def Morpion4(Joueur1, Joueur2, EtatPredefinis=None):
    if STATS:
        gameStart = time.time()
    allignement=4
    taille=TaillePlateau
    if EtatPredefinis:
        game = EtatPredefinis
    else:
        game = Etat(None, taille, allignement)

    TourX = True

    while not game.win():
        print(game)
        if TourX:
            Joueur=Joueur1
            JoueurNumero = X
        else:
            Joueur=Joueur2
            JoueurNumero = O

        #if isinstance(Joueur, IA):
                #print(f"Evaluation de victoire: {Joueur.Evaluation(game)}")
        if Joueur == Joueur1:
            print(f"Tour Joueur 1 ({Symbole(JoueurNumero)})")
        else:
            print(f"Tour Joueur 2 ({Symbole(JoueurNumero)})")

        start_time = time.time()
        Emplacement = Joueur.MeilleurEmplacement(game)

        if STATS:
            if isinstance(Joueur, IA):
                #print(f"Etats exploré: {Joueur.EtatExplore}")
                #print(f"Coupures Alpha-Beta: {Joueur.Elagage}")
                end_time = time.time()
                print(f"Temps Écoulé: {round(end_time-start_time, 2)}s")


        while not EmplacementValide(Emplacement, game):
            Emplacement = Joueur.Emplacement(game)

        game.board[Emplacement[0]][Emplacement[1]] = JoueurNumero
        game.TourJoueur = IA.InversionTour(game.TourJoueur)
        TourX = not TourX

    if STATS:
        gameEnd = time.time()
        print(f"Temps total de jeu: {round(gameEnd-gameStart, 2)}")

    print(game)
    winner = game.win()
    if winner == "D":
        print("Égalité!")
    else:
        print(f"{winner} a gagné!")

    rejouer = input("Rejouer? (o/n): ")
    if rejouer == "o":
        Morpion4(Joueur1, Joueur2)

def Symbole(num):
    return "X" if num == X else "O"

def EmplacementValide(Emplacement, game):
    taille = len(game.board)
    if len(Emplacement) != 2:
        print("Ligne,Colonne!")
        return False
    for p in Emplacement:
        if p < 0 or p >= taille:
            print("En dehors des limites!")
            return False
    if game.board[Emplacement[0]][Emplacement[1]] != 0:
        print("Case déjà prise!")
        return False
    return True

def recuperation():
    EtatPredefinisPourX = Etat(None, TaillePlateau, 4)
    EtatPredefinisPourX.board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    EtatPredefinisPourX.TourJoueur = X
    Morpion4(Joueur1,Joueur2,EtatPredefinisPourX)

Joueur1 = IA(LimiteTemps=Puissance, ProfondeurMaximaleRecherche=NombreDeCoupALavance, UtilisationDictionnaire=True)
#Joueur1 = Player()
#Joueur2 = IA(LimiteTemps=Puissance, ProfondeurMaximaleRecherche=NombreDeCoupALavance, UtilisationDictionnaire=True)
Joueur2 = Player()

#recuperation()
Morpion4(Joueur1, Joueur2, None)