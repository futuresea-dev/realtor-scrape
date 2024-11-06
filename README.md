# Scraping Script for Real Estate Agents Data

This repository contains a Python script that uses Selenium to scrape data on real estate agents from [Realtor.com](https://www.realtor.com/). The script retrieves important information about real estate agents based on a specified location.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.x
- SeleniumBase

## Installation

Follow these steps to set up your environment:

1. **Install Python** (if you haven't already):
   - Download and install Python from the [official website](https://www.python.org/downloads/).
   ![Download and install Python](images/screenshot_1.png)
   - Ensure that Python is added to your system's PATH. You can check this by running the following command in your terminal or command prompt:
     ```bash
     python --version
     ```

2. **Install SeleniumBase**:
   ![install seleniumbase](images/screenshot_2.png)
   - Open your terminal or command prompt and run the following command:
     ```bash
     pip install seleniumbase
     ```

## Usage

To run the script and scrape real estate agents' data, follow these steps:

1. Clone the repository (if applicable):
   ```bash
   git clone <repository-url>

2. Navigate to the directory where the script is located:
    ```
    cd <your-script-directory>
    ```
3. Run the script with the URL for the desired location:
![run script](images/screenshot_3.png)
```
python main.py https://www.realtor.com/realestateagents/trenton_nj
```

Output Format
The script will output the scraped data to a file named agents_data.csv in the same directory. The CSV file will contain the following columns:

Agent Name
Company
Phone Number
Website
Other relevant details