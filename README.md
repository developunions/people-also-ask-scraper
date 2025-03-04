# Google "People Also Ask" Scraper

This script extracts related questions from Google’s "People Also Ask" section using Selenium. It supports **manual CAPTCHA solving** and saves results in JSON format.

## Features

* Extracts related questions ("People also ask") from Google.
* Configurable number of questions per keyword via num_questions in the settings.
* Uses Selenium WebDriver with Chrome.
* Provides detailed logging for debugging.
* Waits for manual CAPTCHA resolution if detected.
* Saves results in a JSON file and logs processed keywords in a separate file.

## Requirements

* Python 3.6+
* Google Chrome browser installed
* ChromeDriver (automatically managed using webdriver_manager)
* Required Python packages:
    * `selenium`
    * `webdriver_manager`
    * `requests` (if needed)

```
pip install selenium webdriver_manager requests
```
## Installation

1. Clone the repository:
```
git clone https://github.com/developunions/people-also-ask-scraper.git
cd people-also-ask-scraper
```
2. Make sure Python and pip are installed.
3. Install the required dependencies (see above).

## Installation

The script uses a `settings.json` file for its configuration. Below is an example of a settings file:

```
{
    "chrome_options": [
        "--start-maximized",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-popup-blocking",
        "--disable-notifications",
        "--disable-dev-shm-usage"
    ],
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "language": "en",
    "timeout": 5,
    "delay_range": [1, 3],
    "num_questions": 5
}
```

* *chrome_options:* A list of Chrome options. Note that removing `--headless` will open the browser window, allowing you to manually solve CAPTCHAs.
* *user_agent:* The User-Agent string used for the requests.
* *language:* The language parameter used in Google searches (e.g., `"en"` for English).
* *timeout:* A base timeout (in seconds) used between actions.
* *delay_range:* A range (in seconds) for random delays between requests.
* *num_questions:* Number of questions to extract per keyword.

## Usage

1. **Prepare Keywords**

Create a keywords.txt file in the same directory as the script. Each line should contain a keyword or query for which you want to extract questions. For example:

```
how to plant raspberries
how to plant an apple tree
```

2. **Run the Script**

Execute the script with Python:

```
python paa.py
```

The script will:

* Read keywords from `keywords.txt`.
* Query Google for each keyword.
* Wait for manual CAPTCHA resolution if detected. Typically, one solution is required to continue the session without interruption. Frequent CAPTCHA occurrences may indicate low `delay_range` in `settings.json`.
* Extract the specified number of related questions.
* Save results to `google_questions.json`.
* Record processed queries in `done.txt`.

## Example Output

The output file `(google_questions.json)` will have a structure similar to:

```
[
    {
        "id": "how to plant raspberries",
        "questions": [
            "How to plant raspberries correctly?",
            "How to care for raspberries?",
            "When is the best time to plant raspberries?",
            "Which raspberry varieties grow best in my region?",
            "How to combat raspberry diseases?"
        ]
    },
    {
        "id": "how to plant an apple tree",
        "questions": [
           "When to plant an apple tree?",
            "How to care for an apple tree?",
            "Which apple varieties are suitable for a garden plot?",
            "How to combat apple tree diseases?",
            "How to prune an apple tree for a better harvest?"
        ]
    }
]
```

## Troubleshooting

* **CAPTCHA Handling:**
If a CAPTCHA appears, the script will log a message and wait for you to solve it manually in the browser window. Once the CAPTCHA is solved, the script will continue automatically.
* **Logging:**
Detailed logs are displayed in the console. Use these logs to debug any issues.
* **Driver Issues:**
Ensure that your Chrome version is compatible with the version of ChromeDriver installed by `webdriver_manager`.

## Contributing

Contributions and suggestions are welcome! Feel free to fork the repository, make improvements, and submit pull requests. If you encounter any issues, please open an issue in the repository. 
