import json
import os
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load settings from settings.json
settings_file = os.path.join(os.path.dirname(__file__), "settings.json")
try:
    with open(settings_file, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    logging.info(f"Settings loaded from {settings_file}")
except Exception as e:
    logging.exception("Error loading settings file.")
    exit(1)

# Load configurations from settings
CHROME_OPTIONS = settings["chrome_options"]
USER_AGENT = settings["user_agent"]
LANGUAGE = settings["language"]
TIMEOUT = settings["timeout"]
DELAY_RANGE = settings["delay_range"]
NUM_QUESTIONS = settings.get("num_questions", 5)  # Number of questions to retrieve per query

# Setup Chrome options
chrome_options = Options()
for option in CHROME_OPTIONS:
    chrome_options.add_argument(option)
chrome_options.add_argument(f'user-agent={USER_AGENT}')

# Initialize Selenium WebDriver with error handling
driver = None
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    time.sleep(2)  # Allow time for the driver to initialize
    logging.info("Selenium WebDriver initialized successfully.")
except Exception as e:
    logging.exception("Error initializing Selenium WebDriver:")
    exit(1)

def wait_for_manual_captcha_resolution():
    """Wait for the user to manually solve the CAPTCHA."""
    logging.info("CAPTCHA detected! Please solve it manually in the browser.")
    # Wait until the CAPTCHA form is no longer present
    while driver.find_elements(By.ID, "captcha-form"):
        logging.info("Waiting for CAPTCHA to be solved...")
        time.sleep(5)
    logging.info("CAPTCHA appears to be solved.")

def get_google_questions(query):
    """Retrieve questions from Google using Selenium."""
    logging.info(f"Searching for questions: {query}")
    search_url = f"https://www.google.com/search?q={query}&hl={LANGUAGE}"
    driver.get(search_url)
    time.sleep(random.uniform(DELAY_RANGE[0], DELAY_RANGE[1]))  # Random delay
    
    # If CAPTCHA is detected, wait for manual resolution
    if driver.find_elements(By.ID, "captcha-form"):
        wait_for_manual_captcha_resolution()

    questions = []
    try:
        elements = driver.find_elements(By.CLASS_NAME, "related-question-pair")
        for element in elements:
            question = element.text.strip()
            if question:
                questions.append(question)
        
        if not questions:
            logging.info(f"Skipping {query}, no questions found.")
        
        # Return the specified number of questions from settings
        return questions[:NUM_QUESTIONS] if questions else None
    except Exception as e:
        logging.exception(f"Error retrieving questions for '{query}':")
        return None

def parse_output_file(input_file, output_file, done_file):
    logging.info(f"Reading input file: {input_file}")
    
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            try:
                parsed_data = json.load(f)
                if not isinstance(parsed_data, list):
                    parsed_data = []
            except json.JSONDecodeError:
                parsed_data = []
    else:
        parsed_data = []
    
    existing_ids = {entry["id"] for entry in parsed_data}
    done_queries = set()
    
    if os.path.exists(done_file):
        with open(done_file, 'r', encoding='utf-8') as f:
            done_queries.update(line.strip() for line in f.readlines())
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        search_query = line.strip()
        if not search_query or search_query in existing_ids or search_query in done_queries:
            logging.info(f"Skipping {search_query}, already processed or empty.")
            continue
        
        questions = get_google_questions(search_query)
        
        with open(done_file, 'a', encoding='utf-8') as f:
            f.write(search_query + "\n")
        
        if questions is None:
            continue
        
        parsed_data.append({
            "id": search_query,
            "questions": questions
        })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)
        
        time.sleep(random.uniform(TIMEOUT, TIMEOUT + 10))  # Random delay between requests
    
    logging.info(f"All data saved to {output_file}")
    driver.quit()

if __name__ == "__main__":
    input_txt = os.path.join(os.path.dirname(__file__), "keywords.txt")
    output_json = os.path.join(os.path.dirname(__file__), "google_questions.json")
    done_txt = os.path.join(os.path.dirname(__file__), "done.txt")
    parse_output_file(input_txt, output_json, done_txt)
