import random

population_size = 100

num_generations = 100

crossover_rate = 0.8

mutation_rate = 0.1

num_days = 3

num_hours = 4


class Teacher:
    def __init__(self, name, discipline):
        self.name = name
        self.discipline = discipline

    def teaches(self, discipline):
        return discipline == self.discipline

    def __str__(self):
        return self.name


class Class:
    def __init__(self, discipline, teacher):
        self.discipline = discipline
        self.teacher = teacher

    def __str__(self):
        return f"{self.discipline} {self.teacher}"


disciplines_count = {
    0: 1,
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 2,
    6: 1,
    7: 1,
    8: 1,
    9: 2,
}

disciplines = [
    "Iнформаційні технології в менеджментi",
    "Вибрані розділи трудового права і основ підприємницької діяльності",
    "Розробка програмного забезпечення",
    "Лаб. Розробка програмного забезпечення",
    "ОС з розподілом часу",
    "Проблеми штучного інтелекту",
    "Нейронні мережі",
    "Лаб. Нейронні мережі",
    "Інтелектуальні системи",
    "Лаб. Інтелектуальні системи",
]

teachers = [
    Teacher("Вергунова І.М.", 0),
    Teacher("Богуславський О.В.", 1),
    Teacher("Карнаух Т.О.", 2),
    Teacher("Карнаух Т.О.", 3),
    Teacher("Коваль Ю.В.", 4),
    Teacher("Крак Ю.В.", 5),
    Teacher("Пашко А.О.", 6),
    Teacher("Пашко А.О.", 7),
    Teacher("Глибовець М.М.", 8),
    Teacher("Федорус О.М.", 9),
    Teacher("Тарануха В.Ю.", 9),
]


def printSchedule(schedule):
    for cls in schedule:
        print(f"{str(cls)}: {str(schedule[cls])}")


def generate_random_schedule():
    schedule = {}

    for day in range(num_days):
        for hour in range(num_hours):
            discipline_idx = random.randint(0, len(disciplines) - 1)
            discipline = disciplines[discipline_idx]

            eligible_teachers = list(
                filter(lambda x: x.teaches(discipline_idx), teachers)
            )
            teacher_idx = random.randint(0, len(eligible_teachers) - 1)
            teacher = eligible_teachers[teacher_idx]

            schedule[(day, hour)] = Class(discipline, teacher)

    return schedule


def get_fitness(schedule):
    fitness = 0

    schedule_disciplines = [
        schedule[(day, hour)].discipline
        for day in range(num_days)
        for hour in range(num_hours)
    ]
    schedule_teachers = [
        schedule[(day, hour)].teacher
        for day in range(num_days)
        for hour in range(num_hours)
    ]

    fitness += len(set(schedule_disciplines)) + len(set(schedule_teachers))

    # add 1 if a discipline is taught less than 3 times in 2 days
    for _ in range(5):
        for discipline in disciplines:
            if schedule_disciplines.count(discipline) < 3:
                fitness += 1

    # add 1 if a teacher teaches less than 3 times in 2 days
    for _ in range(5):
        for teacher in teachers:
            if schedule_teachers.count(teacher) < 3:
                fitness += 1

    # subtract 1 if a there are 2 disciplines in a row
    for i in range(0, len(schedule_disciplines) - 1):
        if schedule_disciplines[i] == schedule_disciplines[i + 1]:
            fitness -= 1

    # subtract 1 if a there are 2 teachers in a row
    for i in range(0, len(schedule_teachers) - 1):
        if schedule_teachers[i] == schedule_teachers[i + 1]:
            fitness -= 1

    # subtract 1 for each discipline that is taught more than it should be
    for discipline in disciplines:
        if (
            schedule_disciplines.count(discipline)
            > disciplines_count[disciplines.index(discipline)]
        ):
            fitness -= 1

    # add 1 if a discipline is taught by a single teacher
    for discipline in disciplines:
        if schedule_disciplines.count(discipline) == 1:
            fitness += 1

    return fitness


def crossover(schedule1, schedule2, crossover_rate):
    new_schedule = {}

    for day, hour in schedule1:
        if random.random() < crossover_rate:
            new_schedule[(day, hour)] = schedule1[(day, hour)]
        else:
            new_schedule[(day, hour)] = schedule2[(day, hour)]
    return new_schedule


def mutation(schedule):
    day = random.randint(0, num_days - 1)
    hour = random.randint(0, num_hours - 1)

    discipline_idx = random.randint(0, len(disciplines) - 1)
    discipline = disciplines[discipline_idx]

    eligible_teachers = list(filter(lambda x: x.teaches(discipline_idx), teachers))
    teacher_idx = random.randint(0, len(eligible_teachers) - 1)
    teacher = eligible_teachers[teacher_idx]
    schedule[(day, hour)] = Class(discipline, teacher)


def genetic_algorithm():
    population = [generate_random_schedule() for i in range(population_size)]

    for gen in range(num_generations):
        fitnesses = [get_fitness(schedule) for schedule in population]

        best_schedule_idx = max(range(len(fitnesses)), key=lambda x: fitnesses[x])
        best_schedule = population[best_schedule_idx]

        print("Generation:", gen, "Best fitness:", fitnesses[best_schedule_idx])

        new_population = [best_schedule]

        while len(new_population) < population_size:
            parent1_idx = random.randint(0, len(population) - 1)
            parent2_idx = random.randint(0, len(population) - 1)
            parent1 = population[parent1_idx]
            parent2 = population[parent2_idx]
            # crossing
            child = crossover(parent1, parent2, crossover_rate)
            # mutation
            if random.random() < mutation_rate:
                mutation(child)
            # new child after crossover and mutation
            new_population.append(child)
        # update population
        population = new_population

    printSchedule(best_schedule)

    # check if all teachers are assigned
    schedule_teachers = [
        best_schedule[(day, hour)].teacher
        for day in range(num_days)
        for hour in range(num_hours)
    ]

    # check if all disciplines are assigned
    schedule_disciplines = [
        best_schedule[(day, hour)].discipline
        for day in range(num_days)
        for hour in range(num_hours)
    ]

    # print out assignments count of each teacher
    for teacher in teachers:
        print(f"{str(teacher)}: {schedule_teachers.count(teacher)}")

    # print out assignments count of each discipline
    for discipline in disciplines:
        print(f"{str(discipline)}: {schedule_disciplines.count(discipline)}")


genetic_algorithm()
