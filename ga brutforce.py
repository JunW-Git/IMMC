import random
import math
import copy


A = [
    ["Manchester City", 53.4831, 2.2004],
    ["Club America", 19.3029, 99.1505],
    ["Ah Ahly", 30.0519, 31.2336],
    ["Al Hilal", 24.7136, 46.6753],
    ["Melbourne City", -37.8136, 144.9631],
]
original_A = copy.deepcopy(A)

B = [
    ["Real Madrid", 40.4531, 3.6883],
    ["Bayern Munich", 48.2188, 11.6247],
    ["Independiente", -0.2150, -78.5048],
    ["LAFC", 34.0127, 118.2840],
    ["Al Nassr", 24.7743, 46.7386],
]
original_B = B.copy()

C = [
    ["Paris Saint-German", 48.8414, 2.2530],
    ["River Plate", -34.5456, -58.4491],
    ["Auckland City", -36.8509, 174.7645],
    ["Memlodi Sundowns", -25.7463, 28.2227],
    ["Kawasaki Frontale", 35.5550, 139.6206],
]
original_C = C.copy()

D = [
    ["Inter Milan", 45.4781, 9.1240],
    ["Inter Miami", 25.9580, 80.2389],
    ["Palmeiras", -23.5475, -46.6658],
    ["Esperance de Tunis", 36.8375, 10.1794],
    ["Sydney FC", -33.8688, 151.2093], 
]
original_D = D.copy()

num_teams = 5


def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6378.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers
    distance = R * c
    return distance

# ----------------------------------------------------------------------------------------------------------

population_size = 10
tournament_size = population_size // 2 # How many parents will be selected to produce offspring

# Generate matchups for each team: 2 home and 2 away games
def match_up(teams):
    copy_teams = teams.copy()
    random.shuffle(copy_teams)
    matchups = []
    home_away = ["home", "home", "away", "away"]
    for row in range(len(copy_teams) - 1):
        count = 0
        for col in range(row + 1, len(copy_teams)):
            if home_away[count] == "home":
                matchups.append([copy_teams[row], copy_teams[col]])
            if home_away[count] == "away":
                matchups.append([copy_teams[col], copy_teams[row]])
            count += 1
    random.shuffle(matchups)
    return matchups


# Calculates total distance
def score(matchups):
    original = matchups
    distance = 0
    count = 0
    for pair in matchups:
        # If home team is not at home
        if original[count][1] != matchups[count][1]:
            distance += haversine(matchups[count][1][1], matchups[count][1][2], original[count][1][1], original[count][1][2])
            matchups[count][1][1], matchups[count][1][2] = original[count][1][1], original[count][1][2] # Move team back home
        # If home team is home
        else:
            pair1 = pair[0]
            pair2 = pair[1]
            distance += haversine(pair1[1], pair1[2], pair2[1], pair2[2])
            # Update first team to second teams location - First team moves to second team
            pair1[1], pair1[2] = pair2[1], pair2[2]
        count += 1
    return abs(distance)


def crossover(matches1, matches2):
    for n in range(4):
        pair1_temp = random.choice(matches1)
        pair1 = [pair1_temp[0][0], pair1_temp[1][0]] # Remove coords
        pair1_inverse = [pair1_temp[1][0], pair1_temp[0][0]] # Remove coords

        # Try to find same match in other solution and swap
        for pair2_temp in matches2:
            pair2 = [pair2_temp[0][0], pair2_temp[1][0]] # Remove coords
            if pair1 == pair2:
                matches1[matches1.index(pair1_temp)] = matches2[matches2.index(pair2_temp)]
            elif pair1_inverse == pair2:
                matches1[matches1.index(pair1_temp)] = matches2[matches2.index(pair2_temp)]
    return matches1, matches2


def generate_population():
    global D, original_D
    list_of_solutions = []
    best_solution = [0, 99999999]
    # List of solutions
    previous = [0, 0]
    for i in range(10000):
        solution = [match_up(D), 0]
        D = copy.deepcopy(original_D)
        solution[1] = score(solution[0])
        # Prevent an already solution from being made again
        while previous == solution:
            solution = [match_up(D), 0]
            solution[1] = score(solution[0])
        if solution[1] < best_solution[1] and solution != 0:
            best_solution = copy.deepcopy(solution)
        previous = solution
        list_of_solutions.append(solution)
    return best_solution


# Tournament Selection: Select two parents from the population
def tournament_selection(population):
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda x: x[1])  # Sort by distance (lower is better)
    return tournament[0], tournament[1]  # Return two best solutions


def genetic_algorithm():
    population = generate_population()

    best_solution = [0, 10000000]
    for generation in range(10000):
        matches = generate_population()
        if matches[0][1] < best_solution[1]:
            best_solution = matches[0]

        # Print the best solution of this generation
        best_solution = min(population, key=lambda x: x[1])
        print(f"Generation {generation}: Best distance = {best_solution[1]}")

    # Return the best solution found
    return min(population, key=lambda x: x[1])

# Run the Genetic Algorithm to find the optimal schedule
# best_solution = genetic_algorithm()
# print("Best Schedule:", best_solution[0])
# print("Best Distance:", best_solution[1])


BEST = generate_population()
print(f"Score: {BEST[1]}")
for pairs in BEST[0]:
    print(f"Matches: {pairs[0][0]}, {pairs[1][0]}")