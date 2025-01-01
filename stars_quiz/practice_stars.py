import pandas as pd
import sys

df = pd.read_csv("stars.txt", sep="\t")
df.drop(columns=['WDS_J', 'Approval Date', '#', 'Designation'], inplace=True)

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


constellation_mapping_regions = {
    'And': 'N', 'Ant': 'E', 'Aps': 'S', 'Aql': 'E', 'Aqr': 'E', 'Ara': 'S', 'Ari': 'N', 'Aur': 'N', 'Boo': 'N', 'Cae': 'S', 'Cam': 'N', 
    'Cap': 'E', 'Car': 'S', 'Cas': 'N', 'Cen': 'E', 'Cep': 'N', 'Cet': 'E', 'Cha': 'S', 'Cir': 'S', 'CMa': 'E', 'CMi': 'E', 'Cnc': 'E', 
    'Col': 'S', 'Com': 'N', 'CrA': 'S', 'CrB': 'N', 'Crt': 'E', 'Cru': 'S', 'Crv': 'E', 'CVn': 'N', 'Cyg': 'N', 'Del': 'N', 'Dor': 'S', 
    'Dra': 'N', 'Equ': 'E', 'Eri': 'S', 'For': 'S', 'Gem': 'N', 'Gru': 'S', 'Her': 'N', 'Hor': 'S', 'Hya': 'E', 'Hyi': 'S', 'Ind': 'S', 
    'Lac': 'N', 'Leo': 'N', 'Lep': 'E', 'Lib': 'E', 'LMi': 'N', 'Lup': 'S', 'Lyn': 'N', 'Lyr': 'N', 'Men': 'S', 'Mic': 'E', 'Mon': 'E', 
    'Mus': 'S', 'Nor': 'S', 'Oct': 'S', 'Oph': 'E', 'Ori': 'E', 'Pav': 'S', 'Peg': 'N', 'Per': 'N', 'Phe': 'S', 'Pic': 'S', 'PsA': 'E', 
    'Psc': 'E', 'Pup': 'S', 'Pyx': 'E', 'Ret': 'S', 'Scl': 'E', 'Sco': 'E', 'Sct': 'E', 'Ser': 'E', 'Sex': 'E', 'Sge': 'N', 'Sgr': 'E', 
    'Tau': 'N', 'Tel': 'S', 'Tri': 'N', 'TrA': 'S', 'Tuc': 'S', 'UMa': 'N', 'UMi': 'N', 'Vel': 'S', 'Vir': 'E', 'Vol': 'S', 'Vul': 'N'
}

sky_regions_mapping = {
    'N': 'North', 'E': 'Equator', 'S': 'South'
}

bayer_mapping = {
    'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta', 'θ': 'theta', 'ι': 'iota', 'κ': 'kappa', 
    'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron', 'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 
    'ϕ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega'
}

greek_mapping = {
    'alpha' : 'alf', 'beta': 'bet', 'gamma': 'gam', 'delta': 'del', 'epsilon': 'eps', 'zeta': 'zet', 'eta': 'eta', 'theta': 'tet', 
    'iota': 'iot', 'kappa': 'kap', 'lambda': 'lam', 'mu': 'mu', 'nu': 'nu', 'xi': 'xi', 'omicron': 'omi', 'pi': 'pi', 'rho': 'rho', 
    'sigma': 'sig', 'tau': 'tau', 'upsilon': 'ups', 'phi': 'phi', 'chi': 'chi', 'psi': 'psi', 'omega': 'ome'
}

df['constellation'] = df['Const.'].map(constellation_mapping)
df['bayer'] = df['ID'].str[0].map(bayer_mapping)
df['bayer_abbr'] = df['bayer'].map(greek_mapping)
df['sky_region_abbr'] = df['Const.'].map(constellation_mapping_regions)
df['sky_region'] = df['sky_region_abbr'].map(sky_regions_mapping)

print("Welcome to the practice quiz on IAU-named stars!")

print("\nAvailable sky regions: ")
print("1. North")
print("2. Equator")
print("3. South")
print("4. North and equator")
print("5. South and equator")
print("6. North and south")
print("7. The whole sky")

while True:
    user_input = input("\nEnter your sky region (a number from 1 to 7, or type 'exit' to quit): ")
    
    if user_input.lower().strip() == "exit":  # Check if the input is 'exit'
        sys.exit('Quiz exited.\n')
    
    try:
        region = int(user_input)  # Try converting input to an integer
        if 1 <= region <= 7:  # Check if the input is within the valid range (1 to 8)
            break  # Exit the loop if the input is valid
        else:
            print("Invalid region. Please enter a number from 1 to 7.")
    except ValueError:
        print("Invalid input. Please enter a valid number from 1 to 7 or 'exit' to quit.")

if region == 1:
    df = df[df['sky_region_abbr']=='N']
    unique_pairs = df[['constellation', 'Const.']].drop_duplicates().sort_values(by='constellation')
    formatted_pairs = [f"{row['constellation']} ({row['Const.']})" for _, row in unique_pairs.iterrows()]
    if len(formatted_pairs) > 1:
    	constellations_text = ", ".join(formatted_pairs[:-1]) + " and " + formatted_pairs[-1]
    else:
    	constellations_text = formatted_pairs[0]
    print("\nNorthern constellations used in the quiz are " + constellations_text + ".")

elif region == 2:
    df = df[df['sky_region_abbr']=='E']
    unique_pairs = df[['constellation', 'Const.']].drop_duplicates().sort_values(by='constellation')
    formatted_pairs = [f"{row['constellation']} ({row['Const.']})" for _, row in unique_pairs.iterrows()]
    if len(formatted_pairs) > 1:
    	constellations_text = ", ".join(formatted_pairs[:-1]) + " and " + formatted_pairs[-1]
    else:
    	constellations_text = formatted_pairs[0]
    print("\nEquatorial constellations used in the quiz are " + constellations_text + ".")
    
elif region == 3:
    df = df[df['sky_region_abbr']=='S']
    unique_pairs = df[['constellation', 'Const.']].drop_duplicates().sort_values(by='constellation')
    formatted_pairs = [f"{row['constellation']} ({row['Const.']})" for _, row in unique_pairs.iterrows()]
    if len(formatted_pairs) > 1:
    	constellations_text = ", ".join(formatted_pairs[:-1]) + " and " + formatted_pairs[-1]
    else:
    	constellations_text = formatted_pairs[0]
    print("\nSouthern constellations used in the quiz are " + constellations_text + ".")
elif region == 4:
    df = df[(df['sky_region_abbr']=='N') | (df['sky_region_abbr']=='E')]
    unique_pairs = df[['constellation', 'Const.']].drop_duplicates().sort_values(by='constellation')
    formatted_pairs = [f"{row['constellation']} ({row['Const.']})" for _, row in unique_pairs.iterrows()]
    if len(formatted_pairs) > 1:
    	constellations_text = ", ".join(formatted_pairs[:-1]) + " and " + formatted_pairs[-1]
    else:
    	constellations_text = formatted_pairs[0]
    print("\nNorthern and equatorial constellations used in the quiz are " + constellations_text + ".")
elif region == 5:
    df = df[(df['sky_region_abbr']=='S') | (df['sky_region_abbr']=='E')]
    unique_pairs = df[['constellation', 'Const.']].drop_duplicates().sort_values(by='constellation')
    formatted_pairs = [f"{row['constellation']} ({row['Const.']})" for _, row in unique_pairs.iterrows()]
    if len(formatted_pairs) > 1:
    	constellations_text = ", ".join(formatted_pairs[:-1]) + " and " + formatted_pairs[-1]
    else:
    	constellations_text = formatted_pairs[0]
    print("\nSouthern and equatorial constellations used in the quiz are " + constellations_text + ".")
elif region == 6:
    df = df[(df['sky_region_abbr']=='N') | (df['sky_region_abbr']=='S')]
    unique_pairs = df[['constellation', 'Const.']].drop_duplicates().sort_values(by='constellation')
    formatted_pairs = [f"{row['constellation']} ({row['Const.']})" for _, row in unique_pairs.iterrows()]
    if len(formatted_pairs) > 1:
    	constellations_text = ", ".join(formatted_pairs[:-1]) + " and " + formatted_pairs[-1]
    else:
    	constellations_text = formatted_pairs[0]
    print("\nNorthern and southern constellations used in the quiz are " + constellations_text + ".")
elif region == 7:
    unique_pairs = df[['constellation', 'Const.']].drop_duplicates().sort_values(by='constellation')
    formatted_pairs = [f"{row['constellation']} ({row['Const.']})" for _, row in unique_pairs.iterrows()]
    if len(formatted_pairs) > 1:
    	constellations_text = ", ".join(formatted_pairs[:-1]) + " and " + formatted_pairs[-1]
    else:
    	constellations_text = formatted_pairs[0]
    print("\nConstellations used in the quiz are " + constellations_text + ".")
    pass
        

df = df[df['Vmag'] != '-']
df['Vmag'] = df['Vmag'].astype(float)
while True:
    try:
        magnitude = input("\nChoose the magnitude interval of the stars: enter one magnitude for the upper limit, or two magnitudes separated by a space to define an interval (the limiting magnitude for the naked eye is 6.5): ").strip()
        magnitudes = magnitude.split()
        if magnitude.lower() == 'exit':
        	sys.exit('Quiz exited.')
        if len(magnitudes) == 1:
            magnitude = float(magnitudes[0])
            df = df[df['Vmag'] < magnitude]
            break
        elif len(magnitudes) == 2:
            magnitude = float(magnitudes[0])
            magnitude2 = float(magnitudes[1])
            if magnitude < magnitude2:
                df = df[(df['Vmag'] > magnitude) & (df['Vmag'] < magnitude2)]
            else:
                df = df[(df['Vmag'] < magnitude) & (df['Vmag'] > magnitude2)]
            break
        else:
            print("Please enter either one or two magnitudes.")
            #break  # Exit the loop if the input is valid
    except ValueError:
        print("Please enter a valid number(s).")


if len(df) == 0:
    print("Not enough stars, try again.\n")
    sys.exit()


while True:
    user_input = input(f"\nHow many stars would you like to practice with (maximum {len(df)} stars)?: ")

    if user_input.lower().strip() == "exit":  # Allow user to exit
        sys.exit('Quiz exited.\n')
    
    try:
        no_of_questions = int(user_input)  # Try to convert input to an integer
        if 1 <= no_of_questions <= len(df):  # Check if it's within the valid range
            print(f"Practicing with {no_of_questions} stars.")
            break  # Valid input, exit the loop
        else:
            print(f"Invalid input. Please enter a number between 1 and {len(df)}.")
    except ValueError:
        print("Invalid input. Please enter a valid number or type 'exit' to quit.")
df_sample = df.sample(no_of_questions)
counter = 0
no_of_q = 0
print("\nChoose the practice mode: ")
print("1. Guess the constellation based on star's name")
print("2. Guess the name of the star based on its Bayer designation")
print("3. Guess the name of the star based on its magnitude and constellation")
print("4. Guess the Bayer designation letter based on the star's name")
print("5. Guess the Bayer designation letter based on its magnitude and constellation")
print("6. Guess the magnitude based on the star's name")
print("7. Guess the magnitude of the star based on its Bayer designation")
print("8. Guess the spectral type based on star's name (not yet available)")
print("9. Guess the spectral type based on star's Bayer designation (not yet available)")
print("10. Guess the spectral type based on its magnitude and constellation (not yet available)")

while True:
    user_input = input("\nEnter your practice mode (choose a number from 1 to 10, or type 'exit' to quit): ")
    
    if user_input.lower().strip() == "exit":  # Check if the input is 'exit'
        sys.exit('Quit exited.\n')
    
    try:
        mode = int(user_input)  # Try converting input to an integer
        if 1 <= mode <= 10:  # Check if the input is within the valid range (1 to 8)
            break  # Exit the loop if the input is valid
        else:
            print("Invalid mode. Please enter a number from 1 to 8.")
    except ValueError:
        print("Invalid input. Please enter a valid number from 1 to 8 or 'exit' to quit.")
        
# constellation; name
if mode == 1:
    print("You chose to guess the constellation of a star based on its proper name. You can enter either the full name of the constellation or its abbreviation.")
    for index, row in df_sample.iterrows():
        answer = input(f"\nIn what constellation is {row.iloc[0]}? ")
        if answer.lower() == "exit":
        	print(f"\nYou answered {counter} out of {no_of_q} questions correctly before exit!")
        	sys.exit()
        if answer.lower() == row.iloc[2].lower() or answer.lower() == row.iloc[6].lower():
            print("Correct answer! It is in ", row.iloc[6], " (",row.iloc[2],").", sep="")
            counter += 1
        else:
            print("Incorrect! It is in ", row.iloc[6], " (",row.iloc[2],").", sep="")
        no_of_q += 1
    if counter == no_of_questions:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correct, congratulations!")
    else:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correctly!")
    
# bayer; name
elif mode == 4:
    print("You chose to guess the Bayer designation of a star based on its proper name. You can enter either the full Greek letter or its abbreviation.")
    items = [f"{key} ({value})" for key, value in greek_mapping.items()]

# Join the items with commas, adding "and" before the last one
    output = "\nGreek letters used are: " + ", ".join(items[:-1]) + ", and " + items[-1] + "."

    print(output)
    df_sample = df_sample[pd.notna(df_sample['bayer'])]
    for index, row in df_sample.iterrows():
        answer = input(f"\nWhat is the Bayer designation for the star {row.iloc[0]}? ")
        if answer.lower() == "exit":
        	print(f"\nYou answered {counter} out of {no_of_q} questions correctly before exit!")
        	sys.exit()
        if answer.lower() == row.iloc[7].lower() or answer.lower() == row.iloc[8].lower():
            print("Correct answer! It is ", row.iloc[7], " (",row.iloc[8],").", sep="")
            counter += 1
        else:
                print("Incorrect! It is ", row.iloc[7], " (",row.iloc[8],").", sep="")
        no_of_q += 1
    if counter == no_of_questions:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correct, congratulations!")
    else:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correctly!")
    
# name; bayer
elif mode == 2:
    print("You chose to guess the name of the star based on its Bayer designation.")
    df_sample = df_sample[pd.notna(df_sample['bayer'])]
    for index, row in df_sample.iterrows():
        answer = input(f"\nWhat is the name of the star {row.iloc[1]} {row.iloc[2]}? ")
        if answer.lower() == "exit":
        	print(f"\nYou answered {counter} out of {no_of_q} questions correctly before exit!")
        	sys.exit()
        if answer.lower() == row.iloc[0].lower():
            print(f"Correct answer! It is {row.iloc[0]}.", sep="")
            counter += 1
        else:
                print(f"Incorrect! It is {row.iloc[0]}.")
        no_of_q += 1
    if counter == no_of_questions:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correct, congratulations!")
    else:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correctly!")
    
# magnitude; name             
elif mode == 6:
    print("You chose to guess the apparent magnitude of the star based on its proper name. The magnitude is rounded to one decimal place.")
    
    for index, row in df_sample.iterrows():
        while True:  # Loop to ensure valid input
            user_input = input(f"\nWhat is the magnitude for the star {row.iloc[0]}? ")

            if user_input.lower() == "exit":
                print(f"\nYou answered {counter} out of {no_of_q} questions correctly before exit!")
                sys.exit()

            try:
                answer = float(user_input)  # Attempt to convert input to a float
                break  # Break loop on valid input
            except ValueError:
                print("Invalid input. Please enter a number or 'exit'.")
        
        # Check if the user's answer matches the star's magnitude
        if round(answer, 1) == round(row.iloc[3], 1):
            print(f"Correct answer! It is {row.iloc[3]} ({round(row.iloc[3], 1)}).", sep="")
            counter += 1
        else:
            print(f"Incorrect! It is {row.iloc[3]} ({round(row.iloc[3], 1)}).")
        
        no_of_q += 1  # Increment the question count

    # Summary of results
    if counter == no_of_questions:
        print(f"\nYou answered {counter} out of {no_of_questions} questions correct, congratulations!")
    else:
        print(f"\nYou answered {counter} out of {no_of_questions} questions correctly!")

# magnitude; bayer
elif mode == 7:
    print("You chose to guess the star's apparent magnitude based on its Bayer designation. The magnitude is rounded to one decimal place.")
    # Filter dataframe for non-null Bayer designation
    df_sample = df_sample[pd.notna(df_sample['bayer'])]
    
    for index, row in df_sample.iterrows():
        while True:  # Loop to handle invalid inputs
            user_input = input(f"\nWhat is the magnitude for the star {row.iloc[1]} {row.iloc[2]}? ")

            if user_input.lower() == "exit":
                print(f"\nYou answered {counter} out of {no_of_q} questions correctly before exit!")
                sys.exit()
            
            try:
                answer = float(user_input)  # Attempt to convert input to a float
                break  # Exit loop on valid input
            except ValueError:
                print("Invalid input. Please enter a number or 'exit'.")
        
        # Compare rounded values
        if round(answer, 1) == round(row.iloc[3], 1):
            print(f"Correct answer! It is {row.iloc[3]} ({round(row.iloc[3], 1)}).", sep="")
            counter += 1
        else:
            print(f"Incorrect! It is {row.iloc[3]} ({round(row.iloc[3], 1)}).")
        
        no_of_q += 1  # Increment question count
    
    # Final result
    if counter == no_of_questions:
        print(f"\nYou answered {counter} out of {no_of_questions} questions correctly, congratulations!")
    else:
        print(f"\nYou answered {counter} out of {no_of_questions} questions correctly!")

 
# name; constellation, magnitude                
elif mode == 3:
    print("You chose to guess the name of the star based on its constellation and apparent magnitude.")
    #print(df_sample)
    for index, row in df_sample.iterrows():
        answer = input(f"\nWhat is the name of the star in the constellation of {row.iloc[6]} with {round(row.iloc[3],2)} magnitude? ")
        if answer.lower() == "exit":
        	print(f"\nYou answered {counter} out of {no_of_q} questions correctly before exit!")
        	sys.exit()
        if answer.lower() == row.iloc[0].lower():
            print(f"Correct answer! It is {row.iloc[0]}.")
            counter += 1
        else:
            print(f"Incorrect! It is {row.iloc[0]}.")
        no_of_q += 1
    if counter == no_of_questions:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correct, congratulations!")
    else:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correctly!")
    
# bayer; constellation, magnitude
elif mode == 5:
    print("You chose to guess the Bayer designation of a star based on its constellation and apparent magnitude.")
    items = [f"{key} ({value})" for key, value in greek_mapping.items()]

# Join the items with commas, adding "and" before the last one
    output = "Greek letters used are: " + ", ".join(items[:-1]) + ", and " + items[-1] + "."

    print(output)
    df_sample = df_sample[pd.notna(df_sample['bayer'])]
    for index, row in df_sample.iterrows():
        answer = input(f"\nWhat is the Bayer designation of the star in the constellation of {row.iloc[6]} with {round(row.iloc[3],2)} magnitude? ")
        if answer.lower() == "exit":
        	print(f"\nYou answered {counter} out of {no_of_q} questions correctly before exit!")
        	sys.exit()
        if answer.lower() == row.iloc[7].lower() or answer.lower() == row.iloc[8].lower():
            print(f"Correct answer! It is {row.iloc[1]} ({row.iloc[7]}, {row.iloc[8]}).")
            counter += 1
        else:
            print(f"Incorrect! It is {row.iloc[1]} ({row.iloc[7]}, {row.iloc[8]}).")
        no_of_q += 1
    if counter == no_of_questions:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correct, congratulations!")
    else:
            print(f"\nYou answered {counter} out of {no_of_questions} questions correctly!")

# spectral classes; name            
elif mode == 8:
    print("You chose to guess the spectral class of a star based on its proper name. The spectral classes are O, B, A, F, G, K, and M.")
    print("\nThis mode is not yet available, sorry.")
    sys.exit()
    
# spectral classes; bayer    
elif mode == 9:
    df_sample = df_sample[pd.notna(df_sample['bayer'])]
    print("You chose to guess the spectral class of a star based on its Bayer designation. The spectral classes are O, B, A, F, G, K and M.")
    print("\nThis mode is not yet available, sorry.")
    sys.exit()
    
# spectral classes; constellation, magnitude    
elif mode == 9:
    print("You chose to guess the spectral class of a star based on its apparent magnitude and constellation. The spectral classes are O, B, A, F, G, K and M.")
    print("\nThis mode is not yet available, sorry.")
    sys.exit()
    