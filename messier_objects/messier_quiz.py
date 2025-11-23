import pandas as pd
import sys

table = pd.read_excel('messier_objects.xlsx', index_col=None)

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

abbr_from_full = {full: abbr for abbr, full in constellation_mapping.items()}
table["Constellation_abbr"] = table["Constellation"].map(abbr_from_full)

def mode_guess_constellation_by_number(df_sample):
    print("\nYou will be shown a random selection of Messier objects numbers. Your task is to name the constellation they belong to. Take as much time as you wish.")
    print("You may either type the full constellation name or its abbreviation (e.g. Canes Venatici or CVn). The quiz is case-insensitive and it does not matter how many spaces appear in the answer — e.g. CVN, C V  n are all treated as the same.\n")
    counter = 0
    no_of_q = 0

    for _, row in df_sample.iterrows():
        answer = input(f"\nIn which constellation is {row['Name']}? ").strip().replace(" ", "").lower()

        if answer == "exit":
            print(f"\nYou answered {counter} out of {no_of_q} questions correctly.")
            sys.exit()

        correct_full  = row["Constellation"].lower()
        correct_abbr  = row["Constellation_abbr"].lower()

        if answer in (correct_full, correct_abbr):
            print(f"Correct! It is in {row['Constellation']} ({row['Constellation_abbr']}).")
            counter += 1
        else:
            print(f"Incorrect. It is in {row['Constellation']} ({row['Constellation_abbr']}).")

        no_of_q += 1

    return counter

used_leo_triplet_answers = set()

def mode_guess_messier_by_altname(df_sample):
    print("\nYou will be shown a random selection of Messier objects common names. Your task is to type the Messier object's number based on its common name. Take as much time as you wish.")
    print("You may either type wth the preceding M or just the number (e.g. M13 or 13). The quiz is case-insensitive, and it does not matter how many spaces appear in the answer — e.g. M13, m13, m 13, M 1 3, 1  3 are all treated as the same.")
    global used_leo_triplet_answers

    counter = 0
    no_of_q = 0

    def clean(s):
        return s.lower().strip().replace(" ", "").lstrip("m")

    leo_valid_raw = {"65", "66"}  # Leo Triplet degeneracy

    for _, row in df_sample.iterrows():
        alt = row["Alternate name"]
        answer = input(f"\nWhich Messier object is {alt}? ").strip()

        if answer.lower() == "exit":
            print(f"\nYou answered {counter} out of {no_of_q} questions correctly.")
            sys.exit()

        a = clean(answer)
        correct_raw = clean(row["Name"])

        if correct_raw in leo_valid_raw:

            available_answers = leo_valid_raw - used_leo_triplet_answers

            if not available_answers:
                available_answers = leo_valid_raw

            if a in available_answers:
                print(f"Correct! It is M{a}.")
                counter += 1
                used_leo_triplet_answers.add(a)
            else:
                remaining = (available_answers - {a})
                if remaining:
                    correct_val = remaining.pop()
                else:
                    correct_val = correct_raw 

                print(f"Incorrect. The correct answer is M{correct_val}.")
            no_of_q += 1
            continue

        if a == correct_raw:
            print(f"Correct! It is {row['Name']}.")
            counter += 1
        else:
            print(f"Incorrect. The correct answer is {row['Name']}.")

        no_of_q += 1

    return counter


def mode_guess_constellation_from_common_name(df_sample):
    print("\nYou will be shown a random selection of Messier objects common names. Your task is to name the constellation they belong to. Take as much time as you wish.")
    print("You may either type the full constellation name or its abbreviation (e.g. Canes Venatici or CVn). The quiz is case-insensitive and it does not matter how many spaces appear in the answer — e.g. CVN, C V  n are all treated as the same.\n")
    counter = 0
    no_of_q = 0

    for _, row in df_sample.iterrows():
        answer = input(f"\nIn which constellation is {row['Alternate name']}? ").strip().replace(" ", "").lower()

        if answer == "exit":
            print(f"\nYou answered {counter} out of {no_of_q} questions correctly.")
            sys.exit()

        correct_full  = row["Constellation"].lower()
        correct_abbr  = row["Constellation_abbr"].lower()

        if answer in (correct_full, correct_abbr):
            print(f"Correct! It is in {row['Constellation']} ({row['Constellation_abbr']}).")
            counter += 1
        else:
            print(f"Incorrect. It is in {row['Constellation']} ({row['Constellation_abbr']}).")

        no_of_q += 1

    return counter

def main():
    print("Welcome to the Messier Objects Practice Quiz!\n")
    
    print("Choose a quiz mode below. You may exit the quiz at any time by typing 'exit'.\n")

    print("Modes:")
    print("1 — Guess the constellation from the Messier object number")
    print("2 — Guess the Messier object from its common name")
    print("3 — Guess the constellation from the Messier object common name")

    while True:
        mode = input("\nEnter mode number: ").strip().lower()

        if mode == "exit":
            sys.exit("\nQuiz exited.")

        if mode in {"1", "2", "3"}:
            break

        print("Invalid mode. Please try again.")


    if mode == "1":
        filtered_table = table  
    elif mode == "2":
        filtered_table = table.dropna(subset=["Alternate name"])
        if filtered_table.empty:
            print("No entries with Alternate Name available. Exiting.")
            sys.exit()
    elif mode == "3":
        exclude_names = ["Great Hercules Cluster", "Great Pegasus Cluster", "Great Sagittarius Cluster", "Small Sagittarius Star Cloud", "Andromeda Galaxy", "Triangulum Galaxy", "Great Orion Nebula", "Leo Triplet"]
        filtered_table = table.dropna(subset=["Alternate name"])
        filtered_table = filtered_table[~filtered_table["Alternate name"].isin(exclude_names)]
        
    max_q = len(filtered_table)

    while True:
        user_input = input(f"\nHow many objects would you like to practice with (max {max_q})?: ").strip().lower()

        if user_input == "exit":
            sys.exit("\nQuiz exited.")

        try:
            n = int(user_input)
            if 1 <= n <= max_q:
                break
            else:
                print(f"Please enter a number between 1 and {max_q}.")
        except ValueError:
            print("Invalid input. Enter a number or type 'exit'.")

    df_sample = filtered_table.sample(n)

    if mode == "1":
        score = mode_guess_constellation_by_number(df_sample)
    elif mode == "2":
        score = mode_guess_messier_by_altname(df_sample)
    elif mode == "3":
        score = mode_guess_constellation_from_common_name(df_sample)

    if n == 1:
        print(f"\nYou answered {score} out of {n} question correctly!")
    else:
        print(f"\nYou answered {score} out of {n} questions correctly!")


if __name__ == "__main__":
    main()
