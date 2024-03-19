from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from dotenv import dotenv_values
import os

# Charger les valeurs du fichier .env dans un dictionnaire
config = dotenv_values(".env")

# Affecter les valeurs à username et password
username = config.get("USERNAME")
password = config.get("PASSWORD")

# Initialisation
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.g-4.education/")
time.sleep(2)  # Attend que la page charge

# Connexion
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "passwordinput").send_keys(password)
driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-primary.btn-block.mt-3").click()
time.sleep(2)  # Attend que la session commence

# Navigation
driver.get("https://www.g-4.education/PHP_Course/cours_suivre.php?recid=51&idc=506")
time.sleep(2)  # Attend que la page charge

driver.find_element(By.ID, "jqxButtonColonne").click()

# Récupération de la durée de la vidéo
video = driver.find_element(By.CSS_SELECTOR, ".jw-video.jw-reset")
video_duration = driver.execute_script("return arguments[0].duration", video)
print(f"Durée de la vidéo: {video_duration} secondes")

# Joue la vidéo
driver.execute_script("arguments[0].play()", video)
# Vous pouvez remplacer le temps d'attente fixe par la durée de la vidéo récupérée plus haut
time.sleep(video_duration + 5)  # Ajoutez un peu de temps pour s'assurer que la vidéo a fini de jouer

# Clique sur le bouton "Contenu suivant" tant qu'il est présent
while True:
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-original-title='Contenu suivant']"))
        )
        next_button.click()
        time.sleep(2)  # Attend que la page suivante se charge
    except (NoSuchElementException, TimeoutException):
        print("Fin de la navigation des contenus.")
        break
