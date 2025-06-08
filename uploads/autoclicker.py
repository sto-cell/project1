import pyautogui
import time
import random
import time
from unidecode import unidecode
import pandas as pd  # Make sure to import pandas


french_first_names = [
    "Amélie", "Antoine", "Aurélie", "Benoît", "Camille", "Charles", "Chloé", "Claire", "Clément", "Dominique",
    "Élodie", "Émilie", "Étienne", "Fabien", "François", "Gabriel", "Hélène", "Henri", "Isabelle", "Jules",
    "Juliette", "Laurent", "Léa", "Léon", "Louise", "Lucas", "Madeleine", "Marc", "Margaux", "Marie",
    "Mathieu", "Nathalie", "Nicolas", "Noémie", "Olivier", "Pascal", "Philippe", "Pierre", "Raphaël", "René",
    "Sophie", "Stéphane", "Suzanne", "Théo", "Thomas", "Valentin", "Valérie", "Victor", "Vincent", "Yves",
    "Zoé", "Adèle", "Adrien", "Alexandre", "Alice", "Alix", "Anatole", "André", "Angèle", "Anne",
    "Baptiste", "Basile", "Bernard", "Brigitte", "Céleste", "Céline", "Christophe", "Cyril", "Denis", "Diane",
    "Édouard", "Éléonore", "Émile", "Félix", "Florence", "Georges", "Gérard", "Guillaume", "Hugo", "Inès",
    "Jacques", "Jean", "Jeanne", "Joséphine", "Julien", "Laure", "Lucie", "Maëlle", "Marcel", "Martine",
    "Maxime", "Michel", "Nina", "Océane", "Paul", "Perrine", "Quentin", "Romain", "Solène", "Thérèse"
]

french_last_names = [
    "Leroy", "Moreau", "Bernard", "Dubois", "Durand", "Lefebvre", "Mercier", "Dupont", "Fournier", "Lambert",
    "Fontaine", "Rousseau", "Vincent", "Muller", "Lefèvre", "Faure", "André", "Gauthier", "Garcia", "Perrin",
    "Robin", "Clement", "Morin", "Nicolas", "Henry", "Roussel", "Mathieu", "Garnier", "Chevalier", "François",
    "Legrand", "Gérard", "Boyer", "Gautier", "Roche", "Roy", "Noel", "Meyer", "Lucas", "Gomez",
    "Martinez", "Caron", "Da Silva", "Lemoine", "Philippe", "Bourgeois", "Pierre", "Renard", "Girard", "Brun",
    "Gaillard", "Barbier", "Arnaud", "Martins", "Rodriguez", "Picard", "Roger", "Schmitt", "Colin", "Vidal",
    "Dupuis", "Pires", "Renaud", "Renault", "Klein", "Coulon", "Grondin", "Leclerc", "Pires", "Marchand",
    "Dufour", "Blanchard", "Gillet", "Chevallier", "Fernandez", "David", "Bouquet", "Gilles", "Fischer", "Roy",
    "Besson", "Lemoine", "Delorme", "Carpentier", "Dumas", "Marin", "Gosselin", "Mallet", "Blondel", "Adam",
    "Durant", "Laporte", "Boutin", "Lacombe", "Navarro", "Langlois", "Deschamps", "Schneider", "Pasquier", "Renaud"
]

# Randomly select a first name and a last name
your_first_name = random.choice(french_first_names)
your_last_name = random.choice(french_last_names)

# Generate a random number
random_number = random.randint(1000, 9999)

# Retirer les accents des prénoms et nom de famille
your_first_name_normalized = unidecode(your_first_name).lower()
your_last_name_normalized = unidecode(your_last_name).lower()


your_username = f"{your_first_name_normalized}.{your_last_name_normalized}{random_number}"


your_birthday = "02 3 1989" #dd m yyyy exp : 24 11 2003
your_gender = "1" # 1:F 2:M 3:Not say 4:Custom
your_password = "x,nscldsj123...FDKZ"

def find_and_click_image(image_path):
    """
    Finds the specified image on the screen and clicks on it.

    Parameters:
    image_path (str): The path to the image to find and click on.

    Returns:
    bool: True if the image was found and clicked, False otherwise.
    """
    # Locate the image on the screen
    location = pyautogui.locateOnScreen(image_path, confidence=0.8)
    
    if location:
        # Get the center of the located image
        center = pyautogui.center(location)
        
        # Click the center of the image
        pyautogui.click(center)
        print(f"Clicked on the image at {center}.")
        return True
    else:
        print(f"Could not find the image '{image_path}' on the screen.")
        return False

def type_from_excel(file_path):
    """
    Reads text from an Excel file and types it after clicking the image.

    Parameters:
    file_path (str): The path to the Excel file.
    """
    # Read the Excel file
    df = french_first_names

    # Iterate over the rows in the DataFrame
    c=0
    for index, row in df.iterrows():
        text_to_type = row['text']
        pyautogui.typewrite(str(text_to_type))
        pyautogui.press('tab')
        if c==9:
            print("yes")
            for i in range(4):
                print("yes")
                pyautogui.press('tab')
            st=input()
            pyautogui.typewrite(str(st))
        # Optionally, add a delay between typing different rows
        time.sleep(1)
        c+=1

# Delay to give you time to prepare
delay_before_search = 5  # seconds
print(f"Waiting for {delay_before_search} seconds before searching for the image.")
time.sleep(delay_before_search)

# Path to the reference image and Excel file
image_path = 'fn.png'
def maino():
    pyautogui.typewrite('shubham')
    pyautogui.press('tab')
# Find and click the image before typing from Excel
if find_and_click_image(image_path):
    maino()
