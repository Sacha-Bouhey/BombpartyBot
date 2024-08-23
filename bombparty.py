from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_word_with_syllable(syllable, file_path='dict.txt'):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file if syllable in line]
    return random.choice(words) if words else None


room_number = input("Your room number: ")
username = input("Your username: ")
typing_speed_ms = int(input("Enter typing speed (milliseconds per letter): "))

# Convert milliseconds to seconds
typing_speed = typing_speed_ms / 1000.0

browser = webdriver.Firefox()
browser.implicitly_wait(5)

browser.get(f"https://jklm.fun/{room_number}")

username_input = browser.find_element(By.CLASS_NAME, "styled")
username_input.send_keys(username)
sleep(1)
username_input.send_keys(Keys.ENTER)

sleep(5)

try:
    # Switch to the iframe
    iframe = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    browser.switch_to.frame(iframe)

    while True:
        try:
            # Get the syllable text
            syllable_element = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "syllable"))
            )
            syllable = syllable_element.text

            # Retrieve a word with the syllable from dict.txt
            word = get_word_with_syllable(syllable.lower())
            if word:
                # Find the input field and enter the word
                input_field = WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @class='styled']"))
                )
                for letter in word:
                    input_field.send_keys(letter)
                    sleep(typing_speed)
                input_field.send_keys(Keys.ENTER)
            else:
                print(f"No word found with syllable: {syllable}")
        except Exception as e:
            print("Waiting for the input element to appear...")
        sleep(1)  # Adjust sleep time as needed



    game_input.send_keys(Keys.ENTER)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    browser.quit()
