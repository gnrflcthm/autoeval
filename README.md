# Python Auto Evaluation Script for MyUSTE Prof Evaluation
Easily evaulate your profs with a press of a button. Hassle free.

# Requirements
1. You need to have `python` and `pip` installed in your system (atleast v3.8.x)
2. Chromium WebDriver (version may vary once the program is ran, download appropriate version [here](https://chromedriver.chromium.org/downloads) according to the error message)
    - This repo originally comes with a copy of the chromium web driver but its version may vary

# Setup
1. Install requirements using `pip install -r requirements.txt`
2. Add your credentials (Student Number and Password) in the `credentials.py` file
3. Optionally: You can change the evaluation strategy

# Evaluation Strategies
- RANDOM
    - Randomly selects a choice
- RANDOM_HIGH
    - Randomly selects between 4 or 3
- RANDOM_LOW
    - Randomly selected between 2 or 1
- ONES
    - Selects all 1
- PERFECT
    - Selects all 4

# How To Run
- After installing the requirements and configuring setup, you may run the program using
```
python eval.py
```
