import json
import random
import time
import string
import datetime
import os

def load_constellations_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data["constellations"]

def get_names_formatted(data):
    formatted_names = [f"{constellation['name'][0]} ({constellation['name'][1]})" for constellation in data]
    return sorted(formatted_names)
    
def filter_stars_by_difficulty(data, difficulties):
    filtered_stars = [star for constellation in data for star, diff in zip(constellation['stars'], constellation['difficulty']) if diff in difficulties]
    return filtered_stars

def start_timer():
    return time.time()

def is_timer_expired(start_time, duration=60):
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

        def sorting_key(entry):
            score = int(entry[1])
            time = float(entry[4])
            return (-score, time)

        scoreboard.sort(key=sorting_key)

        print("Rank   | Player                 | Score | Correct Answers | Hints Used | Time (s)  | Completion Time")
        print("-" * 104)
        for i, entry in enumerate(scoreboard[:10], start=1):
            rank = f"{i:2d}"
            player_name = entry[0]
            score = entry[1]
            correct_answers = entry[2]
            hints_used = entry[3]
            elapsed_time = entry[4]
            completion_time = entry[5]
            elapsed_time = float(entry[4])
            print(f"{rank:<6} | {player_name:<22} | {score:<5} | {correct_answers:<15} | {hints_used:<10} | {elapsed_time:.6f} | {completion_time}")

    except FileNotFoundError:
        print("No scores found in", filename)

def save_score(player_name, score, correct_answers, hints_used, elapsed_time, completion_time, filename):
    with open(filename, "a") as file:
        file.write(f"{player_name},{score},{correct_answers},{hints_used},{elapsed_time},{completion_time}\n")

def main():
    file_name = "constellations.json" 
    data = load_constellations_data(file_name)

    num_questions = 7
    max_hints = 3

    formatted_names = get_names_formatted(data)
    formatted_names_str = ', '.join(formatted_names)

    max_possible_score = num_questions * 2 + 2 + max_hints
    print()
    print(f"Welcome to the constellations quiz! This quiz is inspired by Android App called Sky Academy and stars therein. In that light, the names taken, alongside magnitude and classification, are exactly what you would find in this application.\n")
    print(f"This quiz consists of {num_questions} questions. To answer them correctly, you can either type the whole name of the constellation or its abbreviation (case insensitive). To request the list of constellations, type 'list'. Constellations together with their abbreviations included in the quiz are:", formatted_names_str, ".")
    print(f"You have a total of {max_hints} hints available for the entire quiz. To use them, simply type 'hint' during a question. You can only use one hint per question, but be careful: using a hint will cost you 1 point each!")
    print(f"Time to finish the test is unlimited. However, you get extra 2 points if you finish it before 30 seconds elapsed. Each correct answer is 2 points and the quiz contains maximum of {max_possible_score} points.")
    print(f"To exit the quiz, type 'exit'.")
    print()
    input("Press Enter to start the quiz...\n")

    difficulties = []
    regions = []

    print("Choose difficulty:")
    print("1. Easy (Brightest stars in famous constellations, up to magnitude 1.5)")
    print("2. Medium (Constellations with fainter stars, up to magnitude 3)")
    print("3. Hard (Faint stars with magnitudes larger than 3 and/or are not used in connecting lines)")
    print("4. All designated stars")
    choice = input("Enter your choice (1-4): ")
    print()

    while choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Please choose from the options.")
        choice = input("Enter your choice (1-4): ")

    if "1" in choice:
        difficulties.append("E")
    if "2" in choice:
        difficulties.append("M")
    if "3" in choice:
        difficulties.append("H")
    if "4" in choice:
        difficulties.append("All designated stars")  

    print("Choose sky region:")
    print("1. North (from 40° to 90°)")
    print("2. Equator (declination ranges from -40° to 40°)")
    print("3. Both (north and equator constellations)")
    region_choice = input("Enter your choice (1-3): ")
    print()

    while region_choice not in ["1", "2", "3"]:
        print("Invalid choice. Please choose from the options.")
        region_choice = input("Enter your choice (1-3): ")

    if "1" in region_choice:
        regions.append("North")
    if "2" in region_choice:
        regions.append("Equator")
    if "3" in region_choice:
        regions.append("Both")

    for difficulty in difficulties:
        for region in regions:
            num_questions = 7
            max_hints = 3

            if difficulty == "All designated stars":
                all_stars = [star for constellation in data for star in constellation['stars']]  
            else:
                all_stars = filter_stars_by_difficulty(data, [difficulty])

            if region == "Both":
                region_stars = all_stars
            else:
                region_stars = [star for star in all_stars if any(constellation['sky_region'] == region for constellation in data if star in constellation['stars'])]

            if len(region_stars) < num_questions:
                print(f"Not enough unique stars in the selected region ({region}) and difficulty ({difficulty}) to generate questions.")
            else:
                player_name = input("Enter your name: ")
                random_digits = generate_random_digits()
                player_name_with_digits = f"{player_name} #{random_digits}"
                print(f"Your name is: {player_name_with_digits}")

                user_exit = False 

                score, correct_answers, hints_used, elapsed_time = quiz(data, num_questions, max_hints, [difficulty], region_stars)
                completion_time = time.strftime("%Y-%m-%d %H:%M:%S")

                if not user_exit:
                    filename = f"scores_{difficulty}_{region}.txt"
                    existing_scores = []
                    try:
                        with open(filename, "r") as file:
                            existing_scores = [line.strip().split(",") for line in file]
                    except FileNotFoundError:
                        pass

                    player_score = [player_name_with_digits, str(score), str(correct_answers), str(hints_used), str(elapsed_time), completion_time]
                    existing_scores.append(player_score)

                    existing_scores.sort(key=lambda x: (-int(x[1]), float(x[4])))

                    rank_extensions = {1: "st", 2: "nd", 3: "rd"}
                    player_rank = None

                    for i, entry in enumerate(existing_scores):
                        if entry == player_score:
                            player_rank = i + 1
                            break

                    if player_rank is not None and player_rank in rank_extensions:
                        rank_extension = rank_extensions[player_rank]
                    else:
                        rank_extension = "th"

                    with open(filename, "w") as file:
                        for entry in existing_scores:
                            file.write(",".join(entry) + "\n")

                    total_players = len(existing_scores)

                    print(f"\nYou ({player_name_with_digits}) earned {player_rank}{rank_extension} place out of {total_players}.")
                    print(f"Score: {score}, Correct Answers: {correct_answers}, Hints Used: {hints_used}, Time: {elapsed_time} seconds, Completion Time: {completion_time}\n")

                    print("\n------------------------------------------ Leaderboards (Top 10) ------------------------------------------")
                    display_scoreboard(filename)
                else:
                    print(f"\nQuiz terminated. You answered {correct_answers} out of {num_questions} questions correctly.")
                    print(f"You used {hints_used} hints and scored {score} points. Goodbye!")

def quiz(data, num_questions, max_hints, difficulties, region_stars):
    correct_answers = 0
    hints_used = 0
    score = 0
    used_stars = []
    difficulty_str = ", ".join(difficulties)

    elapsed_time = 0

    start_time = start_timer()

    for i in range(num_questions):
        if is_timer_expired(start_time):
            print("Time's up! Quiz terminated.")
            break

        hint_used_for_question = False
        available_stars = [star for star in region_stars if star not in used_stars]
        if not available_stars:
            print("You've already used all available stars.")
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
                    print("You've used all available hints for the quiz.")
            elif user_input == "list":
                print()
                print("List of the names in each constellation:")
                for name in get_names_formatted(data):
                    print(name)
                print()
            elif user_input == "exit":
                print(f"Quiz terminated. You answered {correct_answers} out of {i} questions correctly.")
                print(f"You used {hints_used} hints and scored {score} points. Goodbye!")
                return score, correct_answers, hints_used, elapsed_time
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
