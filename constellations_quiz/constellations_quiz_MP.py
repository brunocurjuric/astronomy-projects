import json
import random
import time
import string
import datetime
import os
import argparse
import sys

parser = argparse.ArgumentParser(description='Learn named stars and compete with other players in this hot seat multiplayer mode by guessing the constellations while choosing difficulty and region of the sky.')

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

def clear_top_lines(lines=30):
    print("\n" * lines)

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
print(f"Welcome to the constellations quiz - multiplayer mode! This quiz is inspired by Android App called Sky Academy and stars therein. In that light, the names taken, alongside magnitude and classification, are exactly what you would find in this application. In this multiplayer mode two or more players are competing against each other, playing the same quiz one after another with the final score afterwards.\n")
print(f"This quiz consists of {num_questions} questions. To answer them correctly, you can either type the whole name of the constellation or its abbreviation (case insensitive). To request the list of constellations, type 'list'. Constellations together with their abbreviations included in the quiz are:", formatted_names_str + ".")
print(f"You can enable or disable hints. If you enable them, you have a total of {max_hints} hints available for the entire quiz. To use them, simply type 'hint' during a question. You can only use one hint per question, but be careful: using a hint will cost you 1 point each!")
print(f"Time to finish the test is {duration} seconds. However, you get extra 2 points if you finish it before 30 seconds elapsed. Each correct answer is 2 points and the quiz contains maximum of {max_possible_score} points ({max_possible_score-3} if you disable hints).")
print(f"To exit the quiz, type 'exit' during the selection of difficulty and region.")
print()
input("Press Enter to start the quiz...\n")

#use_hints_input = False
def main():
    difficulties = []
    regions = []

    print("Choose difficulty:")
    print("1. Easy - the brightest stars in famous constellations (up to magnitude 1.5)")
    print("2. Medium - Fainter stars that are used in connecting lines (up to magnitude 3)")
    print("3. Hard - faint stars with magnitudes larger than 3 used in connecting lines)")
    print("4. Veteran - all named stars from 3 up to 6.5 magnitude that are not included in connecting lines)")
    print("5. All named stars")
    choice = input("Enter your choice (1-5): ").strip()
    print()

    while choice not in ["1", "2", "3", "4", "5", "exit"]:
        print("Invalid choice. Please choose from the options.")
        choice = input("Enter your choice (1-5): ")

    if choice == "exit":
        print("Quiz terminated.")
        sys.exit()

    difficulty_map = {
        "1": "E", "2": "M", "3": "H", "4": "V", "5": "All designated stars"
    }
    difficulties.append(difficulty_map[choice])

    print("Choose sky region:")
    print("1. North (declination from 40° to 90°)")
    print("2. Equator (declination  from -40° to 40°)")
    print("3. South (declination from -90° to -40°)")
    print("4. All constellations")
    print("5. North and equator (declinations from -40° to 90°)")
    print("6. South and equator (declinations from -90° to 40°)")
    region_choice = input("Enter your choice (1-6): ").strip()
    print()

    while region_choice not in ["1", "2", "3", "4", "5", "6", "exit"]:
        print("Invalid choice. Please choose from the options.")
        region_choice = input("Enter your choice (1-6): ")

    if region_choice == "exit":
        print("Quiz terminated.")
        sys.exit()

    region_map = {
        "1": "North", "2": "Equator", "3": "South",
        "4": "All", "5": "North and equator", "6": "South and equator"
    }
    regions.append(region_map[region_choice])
    
    while True:
        use_hints_input = input("Do you want to allow hints? (yes/no): ").strip().lower()
        if use_hints_input in ("yes", "no"):
            use_hints = use_hints_input == "yes"
            break
        else:
            print("Please enter 'yes' or 'no'.")

    while True:
        try:
            num_players = int(input("How many players? "))
            if num_players < 2:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid number (2 or more).")

    num_questions = 7
    max_hints = 3

    if difficulties[0] == "All designated stars":
        all_stars = [star for constellation in data for star in constellation['stars']]
    else:
        all_stars = filter_stars_by_difficulty(data, difficulties)

    region_stars = get_stars_for_region(region_map[region_choice], all_stars)

    if len(region_stars) < num_questions:
        print("Not enough stars to generate questions.")
        sys.exit()

    selected_questions = random.sample(region_stars, num_questions)

    results = []
    used_names = set()  
    for i in range(num_players):
        # Make sure this is defined before the player loop

        while True:
            full_name = input(f"\nPlayer {i + 1}, enter your name: ").strip()
            
            if not full_name:
                print("Please enter a valid name.")
            elif len(full_name) > 10:
                print("Please enter a name up to 10 characters.")
            elif full_name in used_names:
                print("This name is already taken. Please choose a different one.")
            else:
                used_names.add(full_name)
                print(f"Welcome, {full_name}!")
                break

        input("Press Enter to start your quiz...")
        score, correct, hints, elapsed = quiz(data, selected_questions, max_hints, use_hints)
        results.append({
            "name": full_name,
            "score": score,
            "correct": correct,
            "hints": hints,
            "time": elapsed
        })
        print(f"{full_name} finished with {score} points in {elapsed:.2f} seconds!\n")
        input("Press Enter to continue...")
        clear_top_lines(30)
        
    results.sort(key=lambda r: (-r['score'], r['time']))
    print(f"Results are coming...")
    time.sleep(2)
    winner = determine_winner(results)
    if winner:
        print("\n🏆 The winner is", end="", flush=True)
        time.sleep(2)  # 2-second pause for suspense
        print(f" {winner['name']}! 🎉 Congratulations!")
    else:
        print("\n🤝 It's a tie!")
        
    time.sleep(2)
    if use_hints_input == "yes":
        print("\n---------------------- FINAL RESULTS -----------------------")
        print(f"{'Rank':<5} {'Name':<12} {'Score':^7} {'Correct':^9} {'Hints used':^12} {'Time (s)':^8}")
        print("-" * 60)

        for idx, r in enumerate(results, start=1):
            print(f"{idx:<5} {r['name']:<12} {r['score']:^7} {r['correct']:^9} {r['hints']:^12} {r['time']:^8.2f}")
    else:
        print("\n--------------- FINAL RESULTS ----------------")
        print(f"{'Rank':<5} {'Name':<12} {'Score':^7} {'Correct':^9} {'Time (s)':^8}")
        print("-" * 46)

        for idx, r in enumerate(results, start=1):
            print(f"{idx:<5} {r['name']:<12} {r['score']:^7} {r['correct']:^9} {r['time']:^8.2f}")   

def get_stars_for_region(region, all_stars):
    if region == "All":
        return all_stars
    elif region in ["North and equator", "South and equator"]:
        target_regions = region.split(" and ")
        return [star for star in all_stars if any(
            constellation['sky_region'] in target_regions and star in constellation['stars']
            for constellation in data)]
    else:
        return [star for star in all_stars if any(
            constellation['sky_region'] == region and star in constellation['stars']
            for constellation in data)]

def quiz(data, questions, max_hints, use_hints=True):
    correct_answers = 0
    hints_used = 0
    score = 0
    start_time = time.time()

    for i, star in enumerate(questions):
        constellation = next((c for c in data if star in c['stars']), None)
        hint_used_for_question = False  # ✅ FIX: define before use

        while True:
            ans = input(f"Q{i+1}: Which constellation does the star '{star}' belong to? ").strip().lower()
            if ans == "hint":
                if not use_hints:
                    print("Hints are disabled for this quiz.")
                elif hints_used < max_hints and not hint_used_for_question:
                    hints_used += 1
                    hint_used_for_question = True
                    print(f"Hint ({hints_used}/{max_hints}): {constellation['hint']}")
                elif hint_used_for_question:
                    print("You've already used a hint for this question.")
                else:
                    print("You've used all available hints for this quiz.")
            elif ans in [name.lower() for name in constellation['name']]:
                print(f"✅ Correct, it is {constellation['name'][0]} ({constellation['name'][1]})!\n")
                correct_answers += 1
                score += 2
                break
            else:
                print(f"❌ Incorrect. The correct answer is {constellation['name'][0]} ({constellation['name'][1]}).\n")
                break

    elapsed_time = time.time() - start_time

    if elapsed_time < 30:
        score += 2
    score += (max_hints - hints_used)
    if use_hints == False:
        score=score-3
    return score, correct_answers, hints_used, elapsed_time

def determine_winner(results):
    sorted_results = sorted(results, key=lambda r: (-r['score'], r['time']))
    top_score = sorted_results[0]['score']
    top_players = [r for r in sorted_results if r['score'] == top_score]

    if len(top_players) == 1:
        return top_players[0]
    else:
        best_time = min(r['time'] for r in top_players)
        winners = [r for r in top_players if r['time'] == best_time]
        return winners[0] if len(winners) == 1 else None

if __name__ == "__main__":
    main()
