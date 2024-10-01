import math

class Task:
    def __init__(self, id, exec_t, deadline, period, priority):
        self.id = id
        self.exec_t = exec_t
        self.deadline = deadline
        self.period = period
        self.priority = priority
        self.remainingTime = exec_t
        self.nextStartTime = 0
        self.deadlineMissed = False

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

# Déclaration d'une nouvelle tâche
def declare_task():
    id = getValidInt("Id de la tâche : ")
    exec_t = getValidInt("Durée d'exécution (en secondes) : ", minValue=1)
    deadline = getValidInt("Durée de l'échéance (en secondes) : ", minValue=1)
    period = getValidInt("Durée de la période (en secondes) : ", minValue=1)
    priority = getValidInt("Priorité : ", minValue=0)

    task = Task(id, exec_t, deadline, period, priority)
    
    print(f"\nTâche déclarée :\nId : {task.id}\nExécution : {task.exec_t}\nÉchéance : {task.deadline}\nPériode : {task.period}\nPriorité : {task.priority}\n")
    
    return task

# Affiche les tâches déclarées
def display_tasks(tasks):
    print("\nTâches déclarées :")
    for task in tasks:
        print(f"Id : {task.id}\nExécution : {task.exec_t}\nÉchéance : {task.deadline}\nPériode : {task.period}\nPriorité : {task.priority}\n")

# Vérification des conditions de U et Urm, et test de faisabilité selon l'algorithme choisi
def test_faisabilite(tasks, schedulerChoice):
    n_tasks = len(tasks)
    U = sum(task.exec_t / task.period for task in tasks)

    print(f"Calcul de U : {U}")
    
    # Premier test de validité : U doit être <= 1
    if U > 1:
        print("Le système n'est pas faisable car U > 1.")
        return False

    print("Le système respecte la condition U <= 1.")
    
    # Si l'utilisateur a choisi RM, on vérifie Urm
    if schedulerChoice == "RM":
        Urm = n_tasks * (math.pow(2, 1.0 / n_tasks) - 1)
        print(f"Calcul de Urm : {Urm}")
        if U <= Urm:
            print("Le système est faisable car U <= Urm.")
            return True
        else:
            print("Urm < U, on ne sait pas encore, on vérifie !")
            return None  # Continuer la vérification de faisabilité pour RM

    # Si HPF ou DM, on passe au second test de faisabilité (à implémenter)
    if schedulerChoice in ["HPF", "DM"]:
        print("Passons au deuxième test de faisabilité pour HPF ou DM (à implémenter).")
        # Ici, implémentez votre second test de faisabilité.
        return None

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

# Simulation avec préemption (non modifiée)
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

# Choix de l'ordonnanceur et faisabilité
def choose_scheduler(tasks, simulationTime):
    while True:
        print("Choisissez l'algorithme d'ordonnancement :")
        print("1. HPF (Highest Priority First)")
        print("2. RM (Rate Monotonic)")
        print("3. DM (Deadline Monotonic)")
        schedulerChoice = getValidInt("Votre choix (1/2/3) : ", minValue=1, maxValue=3)

        # Convertir le choix en texte pour faciliter l'utilisation
        schedulerType = None
        if schedulerChoice == 1:
            schedulerType = "HPF"
        elif schedulerChoice == 2:
            schedulerType = "RM"
        elif schedulerChoice == 3:
            schedulerType = "DM"

        print(f"Algorithme choisi : {schedulerType}")

        # Test de faisabilité en fonction de l'algorithme choisi
        faisabilite_result = test_faisabilite(tasks, schedulerType)

        # Si le test de faisabilité est validé
        if faisabilite_result is True:
            print(f"Le système est faisable avec l'algorithme {schedulerType}.")
        elif faisabilite_result is None:
            print(f"Le système nécessite des vérifications supplémentaires pour l'algorithme {schedulerType}.")
            # Appeler le deuxième test de faisabilité si nécessaire (implémentation à ajouter)

        # Choix de la préemption
        print("Souhaitez-vous utiliser la préemption ?")
        print("1. Oui (préemption activée)")
        print("2. Non (pas de préemption)")
        preemptionChoice = getValidInt("Votre choix (1/2) : ", minValue=1, maxValue=2)

        # Lancer la simulation en fonction du choix de l'utilisateur (préemptif ou non)
        if preemptionChoice == 1:
            print(f"Simulation avec préemption en utilisant {schedulerType}.")
            schedulerSimuPreemptive(tasks, simulationTime, schedulerType)
        else:
            print(f"Simulation sans préemption en utilisant {schedulerType}.")
            schedulerSimuNonPreemptive(tasks, simulationTime, schedulerType)

        break  # Quitter la boucle après avoir fait un choix valide

# Fonction principale
def main():
    max_tasks = 10  # Nombre maximum de tâches
    tasks = []

    # Déclaration des tâches
    while len(tasks) < max_tasks:
        tasks.append(declare_task())
        # Boucle de validation pour "y" ou "n"
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
    choose_scheduler(tasks, simulationTime)

if __name__ == "__main__":
    main()


