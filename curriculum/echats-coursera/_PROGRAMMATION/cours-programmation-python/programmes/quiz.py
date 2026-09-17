class Joueur:
    espece = "humain"

    def __init__(self, nom, age, devise):
        self.nom = nom
        self.age = age
        self.devise = devise

class Question:
    def __init__(self, question, theme, choix, reponse):
        self.question = question
        self.theme = theme
        self.choix = choix
        self.reponse = reponse

    def afficher_question(self):
        print(f"{'=' * 40}")
        print(f"Question : {self.question}")
        print(f"{'=' * 40}")
        if len(self.choix) == 2:
            print(f"1. {self.choix[0]}   |   2. {self.choix[1]}")
        elif len(self.choix) == 3:
            print(f"1. {self.choix[0]}   |    2. {self.choix[1]}")
            print(f"        3. {self.choix[2]}")
        elif len(self.choix) == 4:
            print(f"1. {self.choix[0]}   |   2. {self.choix[1]}")
            print(f"3. {self.choix[2]}   |    4. {self.choix[3]}")
        else:
            for i, rep in enumerate(self.choix, start=1):
                print(f"{i}. {rep}")
        print(f"{'=' * 40}")

joueur = Joueur("undefined", 0, "undefined")
score = 0
tableau_score = []

def charger_questions():
    questions = []
    with open("questions.txt", "r", encoding="utf-8") as f:
        for ligne in f:
            if ligne.strip() == "":
                continue
            parts = ligne.strip().split("|")
            q = parts[0]
            theme = parts[1]
            choix = parts[2].split(",")
            reponse = parts[3]
            questions.append(Question(q, theme, choix, reponse))
    return questions

def menu(entreePrecedente):
    if entreePrecedente == True:
        print("-------------------------------------------------------")
        print("1: Jouer")
        print("2: Identification")
        print("3: Voir mes informations")
        print("4: Tableau des scores")
        print("5: Quitter")
    choix = input(">>> ")
    if choix.isdigit():
        choix = int(choix)
    else:
        return False
    match choix:
        case 1:
            jouer_quiz()
            return True
        case 2:
            creer_joueur()
            return True
        case 4:
            afficher_scores()
            return True
        case 5:
            exit()

def creer_joueur():
    global joueur
    nom = input(">>> Votre nom est : ")
    age = input(">>> Votre age est : ")
    devise = input(">>> Votre devise est: ")
    joueur = Joueur(nom, age, devise)

def voir_informations():
    print(f"Nom: {joueur.nom}\nAge: {joueur.age}\nDevise: {joueur.devise}")

def afficher_scores():
    print("\n=== TABLEAU DES SCORES ===")
    for i, (nom, sc) in enumerate(tableau_score, start=1):
        print(f"{i}. {nom} : {sc}")
    print("==========================\n")

def jouer_quiz():
    global score
    global tableau_score
    questions = charger_questions()
    score = 0
    for q in questions:
        q.afficher_question()
        reponse = input(">>> ")
        if reponse.isdigit():
            index = int(reponse) - 1
            if 0 <= index < len(q.choix) and q.choix[index].strip().lower() == q.reponse.strip().lower():
                print("Correct !")
                score += 1
            else:
                print(f"Incorrect ! La bonne réponse était : {q.reponse}")
        else:
            if reponse.strip().lower() == q.reponse.strip().lower():
                print("Correct !")
                score += 1
            else:
                print(f"Incorrect ! La bonne réponse était : {q.reponse}")
    print(f"Quiz terminé. Votre score : {score}/{len(questions)}")
    tableau_score.append((joueur.nom, score))

if __name__ == "__main__":
    print("\n\nＧＲＡＮＤ　ＱＵＩＺ　ＤＵ　ＰＹＴＨＯＮ")
    afficherChoix = True
    while True:
        afficherChoix = menu(afficherChoix)
