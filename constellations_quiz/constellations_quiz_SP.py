import json
import random
import time
import string
import datetime
import os
import argparse
import sys

parser = argparse.ArgumentParser(description='Learn named stars by guessing the constellations while choosing difficulty and regions of the sky.')
parser.add_argument('-score', nargs = 2, metavar=('difficulty', 'region'), type=str, action='store', help='Display highscore for a given difficulty (E - easy, M - medium, H - hard, V - veteran, A - all stars) and sky region (N - north, E - equator, S - south, NE - north and equator, SE - south and equator, A - the whole sky). Scores can only be visible once at least one game was played.')

args = parser.parse_args()


def load_constellations_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data["constellations"]

def get_names_formatted(data):
    formatted_names = [f"{constellation['name'][0]} ({constellation['name'][1]})" for constellation in data]
    return sorted(formatted_names)
    
def get_names_formatted_by_region(data, region):
    formatted_names = [f"{constellation['name'][0]} ({constellation['name'][1]})" for constellation in data if constellation['sky_region'] == region]
    return sorted(formatted_names)
    
def filter_stars_by_difficulty(data, difficulties):
    filtered_stars = [star for constellation in data for star, diff in zip(constellation['stars'], constellation['difficulty']) if diff in difficulties]
    return filtered_stars

def start_timer():
    return time.time()

duration = 90
def is_timer_expired(start_time, duration=duration):
    elapsed_time = time.time() - start_time
    return elapsed_time >= duration

def generate_random_digits():
    return ''.join(random.choices(string.digits, k=4))

def format_time(seconds):
    return str(datetime.timedelta(seconds=seconds))

def display_scoreboard(filename):
    try:
        with open(filename, "r") as file:
            scoreboard = [line.strip() for line in file]

        scoreboard = [line.split(",") for line in scoreboard]

        # Define a custom sorting key function to sort by score (descending) and time (ascending)
        def sorting_key(entry):
            score = int(entry[1])
            hints = int(entry[3])
            time = float(entry[4])
            return (-score, hints, time)

        # Sort the scoreboard using the custom sorting key
        scoreboard.sort(key=sorting_key)

        print(" Rank |         Player         | Score | Correct answers | Hints used | Time (s)  | Completion time")
        print("-" * 103) 
        for i, entry in enumerate(scoreboard[:10], start=1):
            rank = f"{i:2d}"
            player_name = entry[0]
            score = entry[1]
            correct_answers = entry[2]
            hints_used = entry[3]
            elapsed_time = float(entry[4])
            completion_time = entry[5]
            print(f" {rank:<5}| {player_name:<22} |  {score:<5}| {correct_answers:<15} | {hints_used:<10} | {elapsed_time:.6f} | {completion_time}")

    except FileNotFoundError:
        print("No scores found in", filename)


region_mapping = {
    'E': 'Equator',
    'N': 'North',
    'S': 'South',
    'NE': 'North and equator',
    'SE': 'South and equator',
    'A': 'All'
}

difficulty_mapping = {
    'E': 'E',
    'M': 'M',
    'H': 'H',
    'V':'V',
    'A': 'All designated stars'
}

def get_full_region(region):
    return region_mapping.get(region, 'Unknown')
    
def get_full_difficulty(difficulty):
    return difficulty_mapping.get(difficulty, 'Unknown')

if args.score:
    score_input = args.score
    difficulty, region = args.score
    if difficulty not in ["E", "M", "H", "V"]:
        print("Invalid difficulty. Please provide a valid difficulty abbreviation (E for easy, M for medium, H for hard, V for veteran).")
        sys.exit(1)
    if region not in region_mapping:
        print("Invalid region. Please provide a valid region abbreviation (N for north, E for equator, S for south, NE for north and equator, SE for south and equator, A for the whole sky).")
        sys.exit(1)
    str1 = 'scores_'
    str2 = '.txt'
    region_name = get_full_region(region)
    difficulty_name = get_full_difficulty(difficulty)
    highscore = 'scores_'+difficulty_name+'_'+region_name+'.txt'
    display_scoreboard(highscore)
    sys.exit()


def save_score(player_name, score, correct_answers, hints_used, elapsed_time, completion_time, filename):
    with open(filename, "a") as file:
        file.write(f"{player_name},{score},{correct_answers},{hints_used},{elapsed_time},{completion_time}\n")

num_questions = 7
max_hints = 3

file_name = "constellations.json"
data = load_constellations_data(file_name)
num_questions = 7
max_hints = 3

formatted_names = get_names_formatted(data)
formatted_names_str = ', '.join(formatted_names)

max_possible_score = num_questions * 2 + 2 + max_hints
    
print()
print(f"Welcome to the constellations quiz! This quiz is inspired by Android App called Sky Academy and stars therein. In that light, the names taken, alongside magnitude and classification, are exactly what you would find in this application.\n")
print(f"This quiz consists of {num_questions} questions. To answer them correctly, you can either type the whole name of the constellation or its abbreviation (case insensitive). To request the list of constellations, type 'list'. Constellations together with their abbreviations included in the quiz are:", formatted_names_str + ".")
print(f"You have a total of {max_hints} hints available for the entire quiz. To use them, simply type 'hint' during a question. You can only use one hint per question, but be careful: using a hint will cost you 1 point each!")
print(f"Time to finish the test is {duration} seconds. However, you get extra 2 points if you finish it before 30 seconds elapsed. Each correct answer is 2 points and the quiz contains maximum of {max_possible_score} points.")
print(f"To exit the quiz, type 'exit' at any instance. In that case, the score will not count.")
print()
input("Press Enter to start the quiz...\n")

def main():
    
    

    difficulties = []
    regions = []

    print("Choose difficulty:")
    print("1. Easy - the brightest stars in famous constellations (up to magnitude 1.5)")
    print("2. Medium - Fainter stars that are used in connecting lines (up to magnitude 3)")
    print("3. Hard - faint stars with magnitudes larger than 3 used in connecting lines)")
    print("4. Veteran - all named stars from 3 up to 6.5 magnitude that are not included in connecting lines)")
    print("5. All named stars")
    choice = input("Enter your choice (1-5): ")
    print()

    while choice not in ["1", "2", "3", "4", "5", "exit"]:
        print("Invalid choice. Please choose from the options.")
        choice = input("Enter your choice (1-5): ")

    if "1" in choice:
        difficulties.append("E")
    if "2" in choice:
        difficulties.append("M")
    if "3" in choice:
        difficulties.append("H")
    if "4" in choice:
        difficulties.append("V")    
    if "5" in choice:
        difficulties.append("All designated stars")
    if "exit" in choice:
        print("Quiz terminated.")
        sys.exit()

    print("Choose sky region:")
    print("1. North (declination from 40° to 90°)")
    print("2. Equator (declination  from -40° to 40°)")
    print("3. South (declination from -90° to -40°)")
    print("4. All constellations")
    print("5. North and equator (declinations from -40° to 90°)")
    print("6. South and equator (declinations from -90° to 40°)")
    region_choice = input("Enter your choice (1-6): ")
    print()

    while region_choice not in ["1", "2", "3", "4", "5", "6", "exit"]:
        print("Invalid choice. Please choose from the options.")
        region_choice = input("Enter your choice (1-6): ")

    if "1" in region_choice:
        regions.append("North")
        formatted_names_by_region = get_names_formatted_by_region(data, 'North')
        formatted_names_by_region_str = ', '.join(formatted_names_by_region)
        print("You chose northern constellations, here is the list used in this quiz: ",formatted_names_by_region_str+'.')
    if "2" in region_choice:
        regions.append("Equator")
        formatted_names_by_region = get_names_formatted_by_region(data, 'Equator')
        formatted_names_by_region_str = ', '.join(formatted_names_by_region)
        print("You chose equatorial constellations, here is the list used in this quiz: ",formatted_names_by_region_str+'.')
    if "4" in region_choice:
        regions.append("All")
    if "3" in region_choice:
        regions.append("South")
        formatted_names_by_region = get_names_formatted_by_region(data, 'South')
        formatted_names_by_region_str = ', '.join(formatted_names_by_region)
        print("You chose southern constellations, here is the list used in this quiz: ",formatted_names_by_region_str+'.')
    if "5" in region_choice:
        regions.append("North and equator")
        formatted_names_north = get_names_formatted_by_region(data, 'North')
        formatted_names_north_str = ', '.join(formatted_names_north)
        formatted_names_equator = get_names_formatted_by_region(data, 'Equator')
        formatted_names_equator_str = ', '.join(formatted_names_equator)
        combined_str = formatted_names_north_str + ", " + formatted_names_equator_str
        merged_list = combined_str.split(", ")
        sorted_list = sorted(merged_list)
        sorted_str = ", ".join(sorted_list)
        print("You chose both the northern and equatorial constellations, here is the list used in this quiz: ",sorted_str+'.\n')
    if "6" in region_choice:
        regions.append("South and equator")
        formatted_names_south = get_names_formatted_by_region(data, 'South')
        formatted_names_south_str = ', '.join(formatted_names_south)
        formatted_names_equator = get_names_formatted_by_region(data, 'Equator')
        formatted_names_equator_str = ', '.join(formatted_names_equator)
        combined_str = formatted_names_south_str + ", " + formatted_names_equator_str
        merged_list = combined_str.split(", ")
        sorted_list = sorted(merged_list)
        sorted_str = ", ".join(sorted_list)
        print("You chose both the southern and equatorial constellations, here is the list used in this quiz: ",sorted_str+'.\n')
    if "exit" in region_choice:
        print("Quiz terminated.")
        sys.exit()

    while True:
        for difficulty in difficulties:
            for region in regions:
                num_questions = 7
                max_hints = 3

                if difficulty == "All designated stars":
                    all_stars = [star for constellation in data for star in constellation['stars']]  # Use all stars from the data
                else:
                    all_stars = filter_stars_by_difficulty(data, [difficulty])

                if region == "All":
                    region_stars = all_stars
                elif region == "North and equator":
                    region_stars = [star for star in all_stars if any(constellation['sky_region'] in ["North", "Equator"] for constellation in data if star in constellation['stars'])]
                elif region == "South and equator":
                    region_stars = [star for star in all_stars if any(constellation['sky_region'] in ["South", "Equator"] for constellation in data if star in constellation['stars'])]
                else:
                    region_stars = [star for star in all_stars if any(constellation['sky_region'] == region for constellation in data if star in constellation['stars'])]

                if len(region_stars) < num_questions:
                    print(f"Not enough unique stars in the selected region ({region}) and difficulty ({difficulty}) to generate questions.")
                else:
                    while True:
                        player_name = input("Enter your name: ").strip()
                        if player_name == "exit":
                            print("Quiz terminated.")
                            sys.exit()
                        if len(player_name)>10:
                            print("Please enter a name with at most 10 characters.")
                        elif not player_name:
                            print("Please enter a valid name.")
                        else:
                            break
                        #if player_name:  # Check if the name is not empty
                         #   break  # Break the loop if the name is not empty
                        #else:
                          #  print("Please enter a valid name.") 
                    random_digits = generate_random_digits()
                    player_name_with_digits = f"{player_name} #{random_digits}"
                    print(f"Your name is: {player_name_with_digits}")

                    user_exit = False  # Flag to check if the user exited the quiz

                    score, correct_answers, hints_used, elapsed_time = quiz(data, num_questions, max_hints, [difficulty], region_stars)
                    completion_time = time.strftime("%Y-%m-%d %H:%M:%S")

                    if not user_exit:  # Check if the user completed the quiz
                        filename = f"scores_{difficulty}_{region}.txt"
                        existing_scores = []
                        try:
                            with open(filename, "r") as file:
                                existing_scores = [line.strip().split(",") for line in file]
                        except FileNotFoundError:
                            pass

                        # Calculate the rank of the player based on their score
                        player_score = [player_name_with_digits, str(score), str(correct_answers), str(hints_used), str(elapsed_time), completion_time]
                        existing_scores.append(player_score)

                        # Sort the scores by score (descending) and time (ascending)
                        existing_scores.sort(key=lambda x: (-int(x[1]), float(x[4])))

                        # Determine the rank extension (st, nd, rd, or th)
                        rank_extensions = {1: "st", 2: "nd", 3: "rd"}
                        player_rank = None

                        for i, entry in enumerate(existing_scores):
                            if entry == player_score:
                                player_rank = i + 1
                                break

                        if player_rank is not None and player_rank in rank_extensions:
                            rank_extension = rank_extensions[player_rank]
                        else:
                            if player_rank % 100 in [11, 12, 13]:
                                rank_extension = "th"
                            else:
                                last_digit = player_rank % 10
                                if last_digit == 1:
                                    rank_extension = "st"
                                elif last_digit == 2:
                                    rank_extension = "nd"
                                elif last_digit == 3:
                                    rank_extension = "rd"
                                else:
                                    rank_extension = "th"
                        '''    
                        else:
                            rank_extension = "th"
                        '''
                        # Save the updated scores back to the text file
                        with open(filename, "w") as file:
                            for entry in existing_scores:
                                file.write(",".join(entry) + "\n")

                        # Calculate the total number of players
                        total_players = len(existing_scores)

                        print(f"\nYou ({player_name_with_digits}) earned {player_rank}{rank_extension} place out of {total_players}.")
                        print(f"Score: {score}, Correct Answers: {correct_answers}, Hints Used: {hints_used}, Time: {elapsed_time} seconds, Completion Time: {completion_time}\n")

                        print("\n------------------------------------------ Scoreboard (Top 10) ------------------------------------------")
                        display_scoreboard(filename)
                    else:
                        print(f"\nQuiz terminated. You answered {correct_answers} out of {num_questions} questions correctly.")
                        print(f"You used {hints_used} hints and scored {score} points. Goodbye!")
                        
        print("\nTry again?")
        print("1. Yes, with the same settings")
        print("2. Yes, with different settings")
        print("3. No")
        while True:
            
            next_action = input("Enter your choice (1-3): ").strip()

            if next_action == "1":
                break  # Reuse the same `difficulties` and `regions`
            elif next_action == "2":
                print()
                main()  # Restart main to re-prompt difficulty/region
                return
            elif next_action == "3":
                print("Quiz exit.")
                sys.exit()
            else:
                print("Invalid input. Please choose 1, 2, or 3.")
                print()


def quiz(data, num_questions, max_hints, difficulties, region_stars):
    correct_answers = 0
    hints_used = 0
    score = 0
    used_stars = []
    difficulty_str = ", ".join(difficulties)

    elapsed_time = 0  # Initialize elapsed_time to 0

    start_time = start_timer()

    for i in range(num_questions):
        if is_timer_expired(start_time):
            print("Time's up! Quiz terminated.")
            break

        hint_used_for_question = False
        available_stars = [star for star in region_stars if star not in used_stars]
        if not available_stars:
            print("You've already used all available stars.") # for survival/arcade mode
            break
        random_star = random.choice(available_stars)
        used_stars.append(random_star)

        correct_constellation = None
        for constellation in data:
            if random_star in constellation['stars']:
                correct_constellation = constellation
                break

        question_attempts = 0

        while question_attempts < 1:
            if is_timer_expired(start_time):
                print("Time's up! Quiz terminated.")
                return score, correct_answers, hints_used, elapsed_time

            user_input = input(f"Question {i + 1}: What constellation does the star {random_star} belong to? ").lower()
            if user_input == "hint":
                if hints_used < max_hints and not hint_used_for_question:
                    hints_used += 1
                    hint_used_for_question = True
                    print(f"Hint ({hints_used}/{max_hints}): {correct_constellation['hint']}")
                elif hint_used_for_question:
                    print("You've already used a hint for this question.")
                else:
                    print("You've used all available hints for this quiz.")
            elif user_input == "list":
                print()
                print("List of the names in each constellation:")
                for name in get_names_formatted(data):
                    print(name)
                print()
            elif user_input == "exit":
                print(f"Quiz terminated. Score does not count.")
                #print(f"You answered {correct_answers} out of {i} questions ({num_questions} in total) correctly and used {hints_used} hints, scoring",correct_answers*2+max_hints-hints_used, "points, but it does not count. Goodbye!")
                sys.exit()
            elif user_input in [name.lower() for name in correct_constellation['name']]:
                correct_answers += 1
                score += 2
                print(f"Correct, it is {correct_constellation['name'][0]} ({correct_constellation['name'][1]})!")
                print()
                break
            else:
                names = " or ".join(correct_constellation['name'])
                print(f"Incorrect. The correct answer is {names}.")
                print()
                break

    elapsed_time = time.time() - start_time
    if elapsed_time < 30:
        score += 2

    score += (max_hints - hints_used)

    print(f"You answered {correct_answers} out of {num_questions} questions correctly and scored {score} points out of {num_questions*2+2+max_hints} points:")
    print(f"- Each correct answer ({correct_answers} correct answers): 2 points")
    print(f"- Each unused hint ({max_hints - hints_used} hints left): 1 point")
    print(f"- Completed in under 30 seconds ({int(elapsed_time)} seconds): 2 extra points")

    return score, correct_answers, hints_used, elapsed_time


if __name__ == '__main__':
    main()
