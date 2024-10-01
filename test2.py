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

# Premier test de faisabilité
def faisabilite1(tasks):
    n_tasks = len(tasks)
    Urm = n_tasks * (math.pow(2, 1.0 / n_tasks) - 1)
    
    U = sum(task.exec_t / task.period for task in tasks)
    
    print(f"U = {U}, Urm = {Urm}")
    
    # Sortie
    if U > 1 or U >= Urm:
        return 0  # Système non faisable
    elif U <= Urm and U < 1:
        return 1  # Système faisable
    else:
        return 2  # Problème

# Fonction récursive pour le deuxième test de faisabilité
def recursive(tasks, Tj, i, R, n_tasks):
    if Tj == 0:
        return tasks[i].exec_t
    else:
        Tj += 1
        R[i][Tj] = tasks[i].exec_t
        for j in range(n_tasks):
            if j != i and tasks[j].period < tasks[i].period:
                R[i][Tj] += (R[i][Tj - 1] / tasks[j].period) * tasks[j].exec_t

        if R[i][Tj] == R[i][Tj - 1]:
            return R[i][Tj]
        else:
            return recursive(tasks, Tj, i, R, n_tasks)

# Simulation simple (sans préemption)
def schedulerSimu(tasks, simulationTime):
    for time in range(simulationTime):
        print(f"Temps : {time}")
        taskExecuted = False

        for task in tasks:
            if time >= task.nextStartTime and task.remainingTime > 0:
                print(f"Exécution de {task.id} (période: {task.period}, échéance: {task.deadline}, priorité: {task.priority})")
                task.remainingTime -= 1
                taskExecuted = True

                # Si la tâche est terminée
                if task.remainingTime == 0:
                    if time > task.deadline:
                        print(f"La tâche {task.id} a échoué son échéance à t={time}.")
                        task.deadlineMissed = True
                    else:
                        print(f"Tâche {task.id} terminée à t={time}.")
                    task.nextStartTime += task.period
                    task.remainingTime = task.exec_t  
                break 

        if not taskExecuted:
            print("Aucune tâche à exécuter.")

# Sélection de l'ordonnanceur avec validation
def choose_scheduler():
    while True:
        print("Choisissez l'algorithme d'ordonnancement :")
        print("1. HPF (Highest Priority First)")
        print("2. RM (Rate Monotonic)")
        print("3. DM (Deadline Monotonic)")
        choice = getValidInt("Votre choix (1/2/3) : ", minValue=1, maxValue=3)
        return choice

# Fonction principale
def main():
    max_tasks = 10  # Nombre maximum de tâches
    tasks = []

    # Déclaration des tâches
    while len(tasks) < max_tasks:
        tasks.append(declare_task())
        continue_declaration = input("Déclarer une autre tâche ? (y/n) : ").strip().lower()
        if continue_declaration != 'y':
            break

    # Afficher les tâches déclarées
    display_tasks(tasks)

    # Premier test de faisabilité
    feasibility_result = faisabilite1(tasks)

    if feasibility_result == 0:
        print("Le système n'est pas faisable.")
    elif feasibility_result == 1:
        print("Le système est faisable.")
    elif feasibility_result == 2:
        # Deuxième test de faisabilité
        R = [[0 for _ in range(10)] for _ in range(10)]  # Vous pouvez ajuster la taille de R
        for i in range(len(tasks)):
            R_value = recursive(tasks, 0, i, R, len(tasks))
            if R_value > tasks[i].deadline:
                print("Le système n'est pas faisable.")
                return
        print("Le système est faisable.")

    # Choix de l'ordonnanceur
    simulationTime = getValidInt("Entrez le temps de simulation (en secondes) : ", minValue=1)
    schedulerChoice = choose_scheduler()

    # Ordonnancement basé sur le choix
    if schedulerChoice == 1:
        print("Ordonnancement HPF choisi.")
    elif schedulerChoice == 2:
        print("Ordonnancement RM choisi.")
    elif schedulerChoice == 3:
        print("Ordonnancement DM choisi.")
    
    # Simulation
    schedulerSimu(tasks, simulationTime)

if __name__ == "__main__":
    main()
