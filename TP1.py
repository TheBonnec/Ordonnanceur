class Task:
    def __init__(self, name, executionTime, deadline, period, priority):
        self.name = name
        self.executionTime = executionTime
        self.deadline = deadline
        self.period = period
        self.priority = priority
        self.remainingTime = executionTime
        self.nextStartTime = 0
        self.deadlineMissed = False
        

def getValidInt(prompt, minValue=None, maxValue=None):
    while True:
        try:
            value = int(input(prompt))
            if minValue is not None and value < minValue:
                raise ValueError(f"Veuillez entrer un nombre supérieur ou égal à {minValue}.")
            return value
        except ValueError as e:
            print(f"Erreur : {e}. Veuillez entrer une valeur entière valide.")

def getTasks():
    taskList = []
    numTasks = getValidInt("Entrez le nombre de tâches : ", minValue=1)

    for i in range(numTasks):
        print(f"\nSaisie des informations pour la tâche {i+1}:")
        name = input("Nom de la tâche : ").strip()
        executionTime = getValidInt("Durée d'exécution (en secondes) : ", minValue=1)
        deadline = getValidInt("Échéance (en secondes) : ", minValue=1)
        period = getValidInt("Période (en secondes) : ", minValue=1)
        priority = getValidInt("Priorité : ", minValue=0)

        taskList.append(Task(name, executionTime, deadline, period, priority))

    return taskList

# HPF
def hpfScheduler(tasks, simulationTime):
    print("HPF (Highest Priority First) : Les tâches avec la plus haute priorité sont exécutées en premier.")
    tasks.sort(key=lambda x: x.priority, reverse=True)
    schedulerSimu(tasks, simulationTime)

# RM
def rmScheduler(tasks, simulationTime):
    print("RM (Rate Monotonic) : Les tâches avec la plus petite période sont exécutées en premier.")
    tasks.sort(key=lambda x: x.period)
    schedulerSimu(tasks, simulationTime)

# DM
def dmScheduler(tasks, simulationTime):
    print("DM (Deadline Monotonic) : Les tâches avec la plus petite échéance sont exécutées en premier.")
    tasks.sort(key=lambda x: x.deadline)
    schedulerSimu(tasks, simulationTime)
    

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
                        print(f"La tâche {task.name} a échoué son échéance à t={time}.")
                        task.deadlineMissed = True
                    currentTask = task
                    break

        if currentTask:
            print(f"Exécution de {currentTask.name} (période: {currentTask.period}, échéance: {currentTask.deadline}, priorité: {currentTask.priority})")
            currentTask.remainingTime -= 1
            taskExecuted = True

            if currentTask.remainingTime == 0:
                if time <= currentTask.deadline:
                    print(f"{currentTask.name} est terminé à t={time}.")
                currentTask.nextStartTime += currentTask.period
                currentTask.remainingTime = currentTask.executionTime
                currentTask = None

        if not taskExecuted:
            print("Aucune tâche à exécuter.")



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
                            print(f"Tâche {task.name} (période: {task.period}) interrompt la tâche {currentTask.name} (période: {currentTask.period}) à t={time}.")
                        elif schedulerType == "HPF":
                            print(f"Tâche {task.name} (priorité: {task.priority}) interrompt la tâche {currentTask.name} (priorité: {currentTask.priority}) à t={time}.")
                        elif schedulerType == "DM":
                            print(f"Tâche {task.name} (échéance: {task.deadline}) interrompt la tâche {currentTask.name} (échéance: {currentTask.deadline}) à t={time}.")
                    currentTask = task
                break
        
        if currentTask:
            print(f"Exécution de {currentTask.name} (période: {currentTask.period}, échéance: {currentTask.deadline}, priorité: {currentTask.priority})")
            currentTask.remainingTime -= 1
            taskExecuted = True

            if currentTask.remainingTime == 0:
                if time > currentTask.deadline:
                    print(f"La tâche {currentTask.name} a échoué son échéance à t={time}.")
                    currentTask.deadlineMissed = True
                else:
                    print(f"{currentTask.name} est terminé à t={time}.")
                currentTask.nextStartTime += currentTask.period
                currentTask.remainingTime = currentTask.executionTime  
                currentTask = None

        if not taskExecuted:
            print("Aucune tâche à exécuter.")


def chooseScheduler(tasks, simulationTime):
    while True:
        print("Choisissez l'algorithme d'ordonnancement :")
        print("1. HPF (Highest Priority First)")
        print("2. RM (Rate Monotonic)")
        print("3. DM (Deadline Monotonic)")
        schedulerChoice = getValidInt("Votre choix (1/2/3) : ", minValue=1, maxValue=3)

        print("Souhaitez-vous utiliser la préemption ?")
        print("1. Oui (préemption activée)")
        print("2. Non (pas de préemption)")
        preemptionChoice = getValidInt("Votre choix (1/2) : ", minValue=1, maxValue=2)

        if schedulerChoice in [1, 2, 3] and preemptionChoice in [1, 2]:
            if preemptionChoice == 1:
                if schedulerChoice == 1:
                    print("Vous avez choisi HPF avec préemption.")
                    schedulerSimuPreemptive(tasks, simulationTime, schedulerType="HPF")
                elif schedulerChoice == 2:
                    print("Vous avez choisi RM avec préemption.")
                    schedulerSimuPreemptive(tasks, simulationTime, schedulerType="RM")
                elif schedulerChoice == 3:
                    print("Vous avez choisi DM avec préemption.")
                    schedulerSimuPreemptive(tasks, simulationTime, schedulerType="DM")
            else:
                if schedulerChoice == 1:
                    print("Vous avez choisi HPF sans préemption.")
                    schedulerSimuNonPreemptive(tasks, simulationTime, schedulerType="HPF")
                elif schedulerChoice == 2:
                    print("Vous avez choisi RM sans préemption.")
                    schedulerSimuNonPreemptive(tasks, simulationTime, schedulerType="RM")
                elif schedulerChoice == 3:
                    print("Vous avez choisi DM sans préemption.")
                    schedulerSimuNonPreemptive(tasks, simulationTime, schedulerType="DM")
            break
        else:
            print("Erreur : choix non valide. Veuillez réessayer.")

if __name__ == "__main__":
    tasks = getTasks()
    simulationTime = getValidInt("Entrez le temps de simulation (en secondes) : ", minValue=1)
    chooseScheduler(tasks, simulationTime)

