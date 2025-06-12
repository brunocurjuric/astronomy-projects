import json
import pandas as pd
import random
from datetime import datetime
import time

with open('constellations.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Mapping abbreviation → full name
constellation_mapping = {
    'And': 'Andromeda', 'Ant': 'Antlia', 'Aps': 'Apus', 'Aql': 'Aquila', 'Aqr': 'Aquarius', 'Ara': 'Ara', 'Ari': 'Aries', 'Aur': 'Auriga', 
    'Boo': 'Bootes', 'Cae': 'Caelum', 'Cam': 'Camelopardalis', 'Cap': 'Capricornus', 'Car': 'Carina', 'Cas': 'Cassiopeia', 'Cen': 'Centaurus', 
    'Cep': 'Cepheus', 'Cet': 'Cetus', 'Cha': 'Chamaeleon', 'Cir': 'Circinus', 'CMa': 'Canis Major', 'CMi': 'Canis Minor', 'Cnc': 'Cancer', 
    'Col': 'Columba', 'Com': 'Coma Berenices', 'CrA': 'Corona Australis', 'CrB': 'Corona Borealis', 'Crt': 'Crater', 'Cru': 'Crux', 
    'Crv': 'Corvus', 'CVn':'Canes Venatici', 'Cyg': 'Cygnus','Del': 'Delphinus', 'Dor': 'Dorado', 'Dra': 'Draco', 'Equ': 'Equuleus', 
    'Eri': 'Eridanus', 'For': 'Fornax', 'Gem': 'Gemini', 'Gru': 'Grus', 'Her': 'Hercules', 'Hor': 'Horologium', 'Hya': 'Hydra', 'Hyi': 'Hydrus', 
    'Ind': 'Indus', 'Lac': 'Lacerta', 'Leo': 'Leo', 'Lep': 'Lepus', 'Lib': 'Libra', 'LMi': 'Leo Minor', 'Lup': 'Lupus', 'Lyn': 'Lynx', 
    'Lyr': 'Lyra', 'Men': 'Mensa', 'Mic': 'Microscopium', 'Mon': 'Monoceros', 'Mus': 'Musca', 'Nor': 'Norma', 'Oct': 'Octans', 'Oph': 'Ophiuchus', 
    'Ori': 'Orion', 'Pav': 'Pavo', 'Peg': 'Pegasus', 'Per': 'Perseus', 'Phe': 'Phoenix', 'Pic': 'Pictor', 'PsA': 'Piscis Austrinus', 
    'Psc': 'Pisces', 'Pup': 'Puppis', 'Pyx': 'Pyxis', 'Ret': 'Reticulum', 'Scl': 'Sculptor', 'Sco': 'Scorpius', 'Sct': 'Scutum', 'Ser': 'Serpens', 
    'Sex': 'Sextans', 'Sge': 'Sagitta', 'Sgr': 'Sagittarius', 'Tau': 'Taurus', 'Tel': 'Telescopium', 'Tri': 'Triangulum', 
    'TrA': 'Triangulum Australe', 'Tuc': 'Tucana', 'UMa': 'Ursa Major', 'UMi': 'Ursa Minor', 'Vel': 'Vela', 'Vir': 'Virgo', 'Vol': 'Volans', 'Vul': 'Vulpecula'
}
name_to_abbr = {v: k for k, v in constellation_mapping.items()}

def show_intro():
    print("""
🌟 Welcome to the constellations quiz - gauntlet mode! 🌟

Test your knowledge of the night sky in this fast-paced quiz where you identify constellations from star names.

How to play:
- Choose your sky region: north (declinations from 40° to 90°), equator (from -40° to 40°) or south (from -90° to -40°).
- You will be asked the name of a star and your task is to name the constellation it belongs to. 
- You can answer with the full constellation name or its common abbreviation (e.g., 'Ori' for Orion). It is case insensitive.
- Questions come in four difficulty levels: easy, medium, hard, and veteran.
- Each correct answer earns you points based on difficulty - 1 for easy, 2 for medium, 3 for hard and 4 for veteran.
- Be quick — your total time to complete the quiz will be recorded.
- After 5 rounds, your score and accuracy will be saved to the highscore table for your chosen sky region.
- Try to beat your own best time and climb the leaderboard!

Ready to prove you’re a true stargazer? Let’s begin! ⭐
""")


show_intro()

valid_regions = {"N", "S", "E"}

while True:
    region_input = input("🌍 Choose region(s) - N (North), S (South), E (Equator), or combinations (e.g., NE, SE, NSE): ").strip().upper()
    region_set = set(region_input)

    if region_set.issubset(valid_regions) and region_set:
        break
    else:
        print("❌ Invalid input. Please use only N, S, E or their combinations (e.g., NE, SE, NSE).")

normalized_region = ''.join(sorted(region_set))
filename_key = "all" if region_set == valid_regions else normalized_region.lower()
highscore_file = f"highscores_{filename_key}.txt"


print("\n✨ Available constellations in your chosen region(s):\n")

selected_regions = set(normalized_region)
constellations_in_region = set()

for constellation in data['constellations']:
    region = constellation['sky_region'][0].upper()
    if region in selected_regions:
        full_name = constellation['name'][0]
        abbr = name_to_abbr.get(full_name, "N/A")
        constellations_in_region.add((full_name.capitalize(), abbr.capitalize()))

sorted_constellations = sorted(constellations_in_region, key=lambda x: x[0])

formatted_list = ", ".join(f"{name} ({abbr})" for name, abbr in sorted_constellations)
formatted_list += "."
print(formatted_list)
print("\nGood luck!\n")

data_records = []
for constellation in data['constellations']:
    full_name = constellation['name'][0]
    region = constellation['sky_region']
    if region[0].upper() not in region_input.upper():
        continue
    stars = constellation['stars']
    difficulties = constellation['difficulty']

    for star, difficulty in zip(stars, difficulties):
        data_records.append({
            "star": star,
            "constellation": full_name,
            "region": region,
            "difficulty": difficulty,
            "abbreviation": name_to_abbr.get(full_name, None)
        })

df = pd.DataFrame(data_records)

difficulty_order = ["E", "M", "H", "V"]
difficulty_points = {"E": 1, "M": 2, "H": 3, "V": 4}
correct_counts = {"E": 0, "M": 0, "H": 0, "V": 0}
asked_counts = {"E": 0, "M": 0, "H": 0, "V": 0}
score = 0
asked_stars = set()


start_time = time.time()
round_max = 5
for round_num in range(1, round_max+1):
    print(f"\n\U0001F501 Round {round_num}/{round_max}")
    for difficulty in difficulty_order:
        candidates = df[(df['difficulty'] == difficulty) & (~df['star'].isin(asked_stars))]
        if not candidates.empty:
            question = candidates.sample(1).iloc[0]
            star_name = question['star']
            correct_full = question['constellation']
            correct_abbr = question['abbreviation']

            user_answer = input(f"\u2b50 What constellation does the star '{star_name}' belong to? ").strip().lower()

            is_correct = user_answer == correct_full.lower() or (correct_abbr and user_answer == correct_abbr.lower())

            asked_counts[difficulty] += 1
            if is_correct:
                earned = difficulty_points[difficulty]
                score += earned
                correct_counts[difficulty] += 1
                print(f"\u2705 Correct! (+{earned} point{'s' if earned > 1 else ''})")
            else:
                print(f"\u274c Incorrect. The correct answer is {correct_full} ({correct_abbr})")

            asked_stars.add(star_name)
        else:
            print(f"(No more stars available for difficulty '{difficulty}')")

end_time = time.time()
elapsed_time = end_time - start_time

total_possible = sum(asked_counts[d] * difficulty_points[d] for d in difficulty_order)
percent = (score / total_possible * 100) if total_possible else 0

print(f"\n\U0001F31F Quiz complete! Your total score: {score} out of {total_possible} points")
print(f"(Correct answers: Easy={correct_counts['E']}, Medium={correct_counts['M']}, Hard={correct_counts['H']}, Veteran={correct_counts['V']})")
print(f"(Accuracy: {percent:.1f}%)")

while True:
    name = input("\nEnter your name for the highscore table (max 9 characters): ").strip()
    if len(name) < 10:
        break
    else:
        print("⚠️ Name too long. Please enter a name with fewer than 10 characters.")

random_id = random.randint(1000, 9999)
unique_name = f"{name} #{random_id}"
highscore_entry = {
    "Name": unique_name,
    "Score": score,
    "Percent": f"{percent:.2f}%",
    "Easy": correct_counts["E"],
    "Medium": correct_counts["M"],
    "Hard": correct_counts["H"],
    "Veteran": correct_counts["V"],
    "Time": f"{elapsed_time:.2f}",  
    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

line = '\t'.join(str(highscore_entry[col]) for col in ["Name", "Score", "Percent", "Easy", "Medium", "Hard", "Veteran", "Time", "Date"])

with open(highscore_file, "a", encoding="utf-8") as f:
    f.write(line + "\n")


try:
    highscores = pd.read_csv(highscore_file, sep='\t', header=None, 
                         names=['Name', 'Score', 'Percentage', 'E', 'M', 'H', 'V', 'Time', 'Datetime'])
except Exception as e:
    print(f"Could not load high scores: {e}")
    highscores = pd.DataFrame(columns=['Name', 'Score', 'Percentage', 'E', 'M', 'H', 'V', 'Time', 'Datetime'])

if not highscores.empty:
    highscores['Score'] = pd.to_numeric(highscores['Score'], errors='coerce').fillna(0)

    highscores['Time'] = highscores['Time'].astype(float)

    highscores_sorted = highscores.sort_values(by=['Score', 'Time'], ascending=[False, True])

    print("\n🏆 Top 10 High Scores:")
    print(highscores_sorted.head(10)[['Name', 'Score', 'Percentage', 'E', 'M', 'H', 'V', 'Time', 'Datetime']].to_string(index=False))

else:
    print("\nNo high scores yet.")