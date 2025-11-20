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

print("Welcome to the Messier Objects Practice Quiz!\n")
print("Currently, only one mode is implemented, where you guess the constellation based on Messier number. This only serves as a practice, for now, as no highscores are provided.\n")
print("You will be shown a random selection of Messier objects. Your task is to name the constellation they belong to. Take as much time as you wish.")
print("You may either type the full constellation name or its abbreviation (e.g. Canes Venatici or CVn).")
print("The quiz is case-insensitive.\n")


unique_const = table[['Constellation', 'Constellation_abbr']].drop_duplicates()

unique_const = unique_const.sort_values(by='Constellation')

formatted = [
    f"{row['Constellation']} ({row['Constellation_abbr']})"
    for _, row in unique_const.iterrows()]
result_string = ", ".join(formatted)

print(f"Constellations containing Messier objects are {result_string}.\n")
print("To exit anytime, type 'exit' as an answer.")
print("Good luck!")

while True:
    user_input = input(f"\nHow many objects would you like to practice with (maximum {len(table)})?: ")

    if user_input.lower().strip() == "exit":  # Allow user to exit
        sys.exit('Quiz exited.\n')
    
    try:
        no_of_questions = int(user_input)  # Try to convert input to an integer
        if 1 <= no_of_questions <= len(table):  # Check if it's within the valid range
            if no_of_questions==1:
                print(f"Practicing with {no_of_questions} Messier object.")
                break  # Valid input, exit the loop
            else:
                print(f"Practicing with {no_of_questions} Messier objects.")
                break  # Valid input, exit the loop
        else:
            print(f"Invalid input. Please enter a number between 1 and {len(table)}.")
    except ValueError:
        print("Invalid input. Please enter a valid number or type 'exit' to quit.")

df_sample = table.sample(no_of_questions)   
   
mode = 1    
counter = 0
no_of_q = 0
if mode == 1:
    for index, row in df_sample.iterrows():
        answer = input(f"\nIn which constellation is {row['Name']}? ")
        user_ans = answer.strip().lower()
        
        correct_full = row["Constellation"].strip().lower()
        correct_abbr = row["Constellation_abbr"].strip().lower()
        
        if user_ans == "exit":
        	print(f"\nYou answered {counter} out of {no_of_q} questions correctly before exit!")
        	sys.exit()
        if user_ans in (correct_full, correct_abbr):
            print(f"Correct answer! It is in {row['Constellation']} ({row['Constellation_abbr']}).")
            counter += 1
        else:
            print(f"Incorrect! It is in {row['Constellation']} ({row['Constellation_abbr']}).")
        no_of_q += 1
    if counter == no_of_questions:
            if no_of_questions==1:
                print(f"\nYou answered {counter} out of {no_of_questions} question correct, congratulations!")
            else:
                print(f"\nYou answered {counter} out of {no_of_questions} questions correct, congratulations!")
    else:
        if no_of_questions==1:
            print(f"\nYou answered {counter} out of {no_of_questions} question correctly!")
        else:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correctly!")