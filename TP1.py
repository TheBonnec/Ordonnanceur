import math

class Task:
    def __init__(self, id, exec_t, deadline, period, priority):
        self.id = id
        self.exec_t = exec_t  # Temps d'exécution (C_i)
        self.deadline = deadline  # Échéance (D_i)
        self.period = period  # Période (T_i)
        self.priority = priority  # Priorité (utile pour HPF)
        self.remainingTime = exec_t  # Temps restant à exécuter
        self.nextStartTime = 0  # Prochain temps de démarrage de la tâche
        self.deadlineMissed = False  # Indicateur si la tâche a manqué son échéance

# Fonction pour obtenir un entier valide de l'utilisateur
def getValidInt(prompt, minValue=None, maxValue=None):
    while True:
        try:
            value = int(input(prompt))
            if minValue is not None and value < minValue:
                raise ValueError(f"Veuillez entrer un nombre supérieur ou égal à {minValue}.")
            if maxValue is not None and value > maxValue:
                raise ValueError(f"Veuillez entrer un nombre inférieur ou égal à {maxValue}.")
            return value
        except ValueError as e:
            print(f"Erreur : {e}. Veuillez entrer une valeur entière valide.")

# Fonction pour demander à l'utilisateur quel algorithme utiliser
def choose_scheduler_mode():
    print("Choisissez l'algorithme d'ordonnancement :")
    print("1. HPF (Highest Priority First)")
    print("2. RM (Rate Monotonic)")
    print("3. DM (Deadline Monotonic)")
    schedulerChoice = getValidInt("Votre choix (1/2/3) : ", minValue=1, maxValue=3)

    # Retourner le schedulerType sous forme de chaîne
    if schedulerChoice == 1:
        return "HPF"
    elif schedulerChoice == 2:
        return "RM"
    elif schedulerChoice == 3:
        return "DM"
    
# Fonction pour déclarer une tâche
def declare_task(schedulerType):
    id = getValidInt("Id de la tâche : ")
    exec_t = getValidInt("Durée d'exécution (en secondes) : ", minValue=1)
    deadline = getValidInt("Durée de l'échéance (en secondes) : ", minValue=1)
    period = getValidInt("Durée de la période (en secondes) : ", minValue=1)
    
    # Demander les priorités uniquement pour HPF
    if schedulerType == "HPF":
        priority = getValidInt("Priorité : ", minValue=1)
    else:
        priority = 0  # Initialiser à 0, calculé plus tard pour RM et DM

    task = Task(id, exec_t, deadline, period, priority)
    print(f"\nTâche déclarée :\nId : {task.id}\nExécution : {task.exec_t}\nÉchéance : {task.deadline}\nPériode : {task.period}\nPriorité : {task.priority}\n")
    return task

# Fonction pour afficher les tâches
def display_tasks(tasks):
    print("\nTâches déclarées :")
    for task in tasks:
        print(f"Id : {task.id}\nExécution : {task.exec_t}\nÉchéance : {task.deadline}\nPériode : {task.period}\nPriorité : {task.priority}\n")

# Fonction pour calculer les priorités pour RM (basé sur la période) et DM (basé sur l'échéance)
def calculate_priorities(tasks, schedulerType):
    if schedulerType == "RM":
        # Trier par période croissante pour RM
        tasks.sort(key=lambda x: x.period)
        # Assigner les priorités basées sur les périodes
        for i, task in enumerate(tasks):
            task.priority = len(tasks) - i
            print(f"Tâche {task.id} (RM) a maintenant une priorité de {task.priority} (basé sur la période).")
    elif schedulerType == "DM":
        # Trier par échéance croissante pour DM
        tasks.sort(key=lambda x: x.deadline)
        # Assigner les priorités basées sur les échéances
        for i, task in enumerate(tasks):
            task.priority = len(tasks) - i
            print(f"Tâche {task.id} (DM) a maintenant une priorité de {task.priority} (basé sur l'échéance).")

# Fonction pour tester la faisabilité basée sur U et Urm
def test_faisabilite(tasks, schedulerType):
    n_tasks = len(tasks)
    U = sum(task.exec_t / task.period for task in tasks)

    print(f"Calcul de U : {U}")
    
    # Premier test de validité : U doit être <= 1
    if U > 1:
        print("Le système n'est pas faisable car U > 1.")
        return False

    print("Le système respecte la condition U <= 1.")
    
    # Si l'utilisateur a choisi RM, on vérifie Urm
    if schedulerType == "RM":
        Urm = n_tasks * (math.pow(2, 1.0 / n_tasks) - 1)
        print(f"Calcul de Urm : {Urm}")
        if U <= Urm:
            print("Le système est faisable car U <= Urm.")
            return True
        else:
            print("Urm < U, on ne sait pas encore, on vérifie !")
            return None  # Continuer la vérification de faisabilité pour RM

    # Si HPF, RM, DM, on passe au second test de faisabilité (étape 2)
    if schedulerType in ["HPF", "DM", "RM"]:
        return None  # Continuer vers l'étape 2

# Nouvelle fonction pour vérifier le temps de réponse
def vérificationTempsDeRéponse(tasks):
    for i in range(len(tasks)):
        tache = tasks[i]

        r1 = tache.exec_t
        condition = True

        while condition:
            r2 = tache.exec_t
            for tachePlusPrioritaire in tasks[:i]:
                r2 += (int(r1 / tachePlusPrioritaire.period) + 1) * tachePlusPrioritaire.exec_t

            if r2 == r1:
                condition = False
            elif r2 > tache.deadline:
                print(f"Le système n'est pas faisable pour la tâche {tache.id}. r_i = {r2}, D_i = {tache.deadline}")
                return False

            r1 = r2
    print("Le système est faisable après le deuxième test.")
    return True

# Simulation sans préemption (non modifiée)
def schedulerSimuNonPreemptive(tasks, simulationTime, schedulerType):
    currentTask = None
    for time in range(simulationTime):
        print(f"Temps : {time}")
        taskExecuted = False
        
        if currentTask is None or currentTask.remainingTime == 0:
            if schedulerType == "HPF":
                tasks.sort(key=lambda x: x.priority, reverse=True)
            elif schedulerType == "RM":
                tasks.sort(key=lambda x: x.period)
            elif schedulerType == "DM":
                tasks.sort(key=lambda x: x.deadline)
                
            for task in tasks:
                if time >= task.nextStartTime and task.remainingTime > 0:
                    if time > task.deadline and not task.deadlineMissed:
                        print(f"La tâche {task.id} a échoué son échéance à t={time}.")
                        task.deadlineMissed = True
                    currentTask = task
                    break

        if currentTask:
            print(f"Exécution de {currentTask.id} (période: {currentTask.period}, échéance: {currentTask.deadline}, priorité: {currentTask.priority})")
            currentTask.remainingTime -= 1
            taskExecuted = True

            if currentTask.remainingTime == 0:
                if time <= currentTask.deadline:
                    print(f"{currentTask.id} est terminé à t={time}.")
                currentTask.nextStartTime += currentTask.period
                currentTask.remainingTime = currentTask.exec_t
                currentTask = None

        if not taskExecuted:
            print("Aucune tâche à exécuter.")

# Simulation avec préemption
def schedulerSimuPreemptive(tasks, simulationTime, schedulerType):
    currentTask = None
    for time in range(simulationTime):
        print(f"Temps : {time}")
        taskExecuted = False

        if schedulerType == "HPF":
            tasks.sort(key=lambda x: x.priority, reverse=True)
        elif schedulerType == "RM":
            tasks.sort(key=lambda x: x.period)
        elif schedulerType == "DM":
            tasks.sort(key=lambda x: x.deadline)

        for task in tasks:
            if time >= task.nextStartTime and task.remainingTime > 0:
                if currentTask is None or (schedulerType == "HPF" and task.priority > currentTask.priority) or \
                   (schedulerType == "RM" and task.period < currentTask.period) or \
                                       (schedulerType == "DM" and task.deadline < currentTask.deadline):
                    if currentTask and currentTask != task:
                        if schedulerType == "RM":
                            print(f"Tâche {task.id} (période: {task.period}) interrompt la tâche {currentTask.id} (période: {currentTask.period}) à t={time}.")
                        elif schedulerType == "HPF":
                            print(f"Tâche {task.id} (priorité: {task.priority}) interrompt la tâche {currentTask.id} (priorité: {currentTask.priority}) à t={time}.")
                        elif schedulerType == "DM":
                            print(f"Tâche {task.id} (échéance: {task.deadline}) interrompt la tâche {currentTask.id} (échéance: {currentTask.deadline}) à t={time}.")
                    currentTask = task
                break
        
        if currentTask:
            print(f"Exécution de {currentTask.id} (période: {currentTask.period}, échéance: {currentTask.deadline}, priorité: {currentTask.priority})")
            currentTask.remainingTime -= 1
            taskExecuted = True

            if currentTask.remainingTime == 0:
                if time > currentTask.deadline:
                    print(f"La tâche {currentTask.id} a échoué son échéance à t={time}.")
                    currentTask.deadlineMissed = True
                else:
                    print(f"{currentTask.id} est terminé à t={time}.")
                currentTask.nextStartTime += currentTask.period
                currentTask.remainingTime = currentTask.exec_t  
                currentTask = None

        if not taskExecuted:
            print("Aucune tâche à exécuter.")

# Fonction principale
def main():
    max_tasks = 10  # Nombre maximum de tâches
    tasks = []

    # Choisir l'algorithme d'ordonnancement avant tout le reste
    schedulerType = choose_scheduler_mode()

    # Déclaration des tâches
    while len(tasks) < max_tasks:
        tasks.append(declare_task(schedulerType))
        while True:
            continue_declaration = input("Déclarer une autre tâche ? (y/n) : ").strip().lower()
            if continue_declaration in ['y', 'n']:
                break
            else:
                print("Veuillez rentrer un 'y' ou 'n' valide.")
        if continue_declaration == 'n':
            break

    # Afficher les tâches déclarées
    display_tasks(tasks)

    # Premier test de faisabilité avec calcul de U et Urm
    simulationTime = getValidInt("Entrez le temps de simulation (en secondes) : ", minValue=1)
    
    # Calcul de faisabilité
    faisabilite_result = test_faisabilite(tasks, schedulerType)

    # Choix de la préemption
    print("Souhaitez-vous utiliser la préemption ?")
    print("1. Oui (préemption activée)")
    print("2. Non (pas de préemption)")
    preemptionChoice = getValidInt("Votre choix (1/2) : ", minValue=1, maxValue=2)

    # Vérification du temps de réponse (après choix de la préemption)
    faisabilite_etape2 = vérificationTempsDeRéponse(tasks)
    


    # Lancer la simulation en fonction du choix de l'utilisateur (préemptif ou non)
    if preemptionChoice == 1:
        print(f"Simulation avec préemption en utilisant {schedulerType}.")
        schedulerSimuPreemptive(tasks, simulationTime, schedulerType)
    else:
        print(f"Simulation sans préemption en utilisant {schedulerType}.")
        schedulerSimuNonPreemptive(tasks, simulationTime, schedulerType)

if __name__ == "__main__":
    main()


