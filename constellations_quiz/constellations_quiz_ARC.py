import json
import random
import sys
import argparse

parser = argparse.ArgumentParser(description='Learn named stars in this arcade mode by guessing the constellations for a chosen region of the sky while climbing the ranks through difficulties.')

args = parser.parse_args()

print("Welcome to constellations quiz - arcade mode! In this quiz you will guess the constellations from stars on four levels: easy, medium, hard, and veteran. It takes 4 correct answers to level from easy to medium, 7 from medium to hard, 10 from hard to veteran, and 15 to finish it. You can use either the full name of the constellation or its abbreviation (case insensitive).")
print("You can choose which sky region you want: north (from 40° to 90° declination), equator (from 40° to -40° declination) or south (from -90° to -40° declination).")

# Load constellations data from JSON
with open("constellations.json", "r") as file:
    data = json.load(file)

# Function to get questions based on the selected region
def get_questions(region):
    questions = []
    for constellation in data["constellations"]:
        if constellation["sky_region"].lower() == region.lower():
            for i, star in enumerate(constellation["stars"]):
                questions.append({
                    "constellation": constellation["name"],
                    "star": star,
                    "difficulty": constellation["difficulty"][i],
                    "hint": constellation["hint"]
                })
    return questions

# Ask a single question
def ask_question(remaining_needed, question, lives, hints_remaining, hint_used):
    while True:
        
        print(f"Which constellation does the star {question['star']} belong to?")
        user_answer = input("Your answer: ")

        if user_answer.lower() == "hint":
            if not hint_used and hints_remaining > 0:
                hints_remaining -= 1
                hint_used = True
                print(f"Hint: {question['hint']}  |  Hints remaining: {hints_remaining}")
                continue  # Re-ask the question
            else:
                print("Hint already used for this question!")
                continue  # Re-ask without penalty
        if user_answer.lower() == "exit":
            print("Quiz terminated.")
            sys.exit()
        if user_answer.lower() in [name.lower() for name in question['constellation']]:
            if remaining_needed==2:
                print("Correct! Only one correct answer left to reach next stage!\n")
            else:
                print(f"Correct! {remaining_needed-1} correct answers left to reach the next level.\n")
            return True, lives, hints_remaining
        else:
            lives -= 1
            print(f"Wrong! The correct answer was: {', '.join(question['constellation'])}")
            print(f"Lives remaining: {lives}\n")
            return False, lives, hints_remaining

# Main quiz function
def quiz():
    print("You get 3 lives and 3 hints per level. Each incorrect answer costs you one life. Hints can be used by typing 'hint', and only one hint can be used per question. There is no time limit on this quiz.")
    print("To exit the quiz, just type 'exit'.\n")
    region = input("Choose your sky region (North / Equator / South): ").capitalize()
    if region not in ["North", "Equator", "South"]:
        print("Invalid region. Exiting.")
        return

    # Gather and sort constellation names for the chosen region
    region_constellations = []
    for constellation in data["constellations"]:
        if constellation["sky_region"].lower() == region.lower():
            full_name = constellation["name"][0]
            abbreviation = constellation["name"][1]
            region_constellations.append(f"{full_name} ({abbreviation})")

    # Sort and format the list into a proper sentence
    region_constellations.sort()
    if len(region_constellations) > 1:
        constellations_sentence = ", ".join(region_constellations[:-1])
        constellations_sentence += f", and {region_constellations[-1]}."
    else:
        constellations_sentence = f"{region_constellations[0]}."
    print(f"\nConstellations included in the {region.lower()} region are {constellations_sentence}")

    all_questions = get_questions(region)
    random.shuffle(all_questions)

    difficulty_order = ['E', 'M', 'H', 'V']
    difficulty_names = {'E': 'Easy', 'M': 'Medium', 'H': 'Hard', 'V': 'Veteran'}
    required_correct = {'E': 4, 'M': 7, 'H': 10, 'V': 15}
    questions_by_difficulty = {d: [q for q in all_questions if q['difficulty'] == d] for d in difficulty_order}

    for difficulty in difficulty_order:
        level_questions = questions_by_difficulty[difficulty]
        random.shuffle(level_questions)
        total_needed = required_correct[difficulty]

        if difficulty != 'V':
            print(f"\nStarting {difficulty_names[difficulty]} level! You need {total_needed} correct answers to advance to the next level.\n")
        else:
            print(f"\nFinal challenge, the {difficulty_names[difficulty]} level! You need {total_needed} correct answers to complete the quiz.\n")
        lives = 3
        hints_remaining = 3
        correct_count = 0

        for question in level_questions:
            if correct_count >= total_needed:
                break
            if lives <= 0:
                print("You ran out of lives. Game Over!")
                return

            hint_used = False
            remaining_needed = total_needed - correct_count
            correct, lives, hints_remaining = ask_question(
                remaining_needed, question, lives, hints_remaining, hint_used
            )
            if correct:
                correct_count += 1

        if correct_count >= total_needed:
            print("=============================================================================")
            print(f"\nCongratulations! You've completed the {difficulty_names[difficulty]} level!")
            print("Leveled up to the next difficulty! Your lives and hints have been reset to 3.\n")
            print("=============================================================================")
        else:
            print("You did not pass this level. Game over.")
            return

    print("Amazing! You've completed all levels. You are a star master!\n")

if __name__ == "__main__":
    quiz()
