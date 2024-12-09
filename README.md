# PyEmail Assistant

**Version:** 0.1

**OS:** Linux

**Author:** Brent Bradford

## Description

PyEmail Assistant is a class project that uses an XGBClassifier machine learning model to
detect email phishing attempts.

## Note

Machine learning models can make mistakes with classification analysis. To stay safe:

1. Avoid Clicking on any links or downloading attachments from emails classified as
safe by the model, unless you are certain of the sender.
2. If you're unsure, contact the sender (e.g. your financial institution or the business)
using their official website or phone number to verify the email.

### Model

**XGBClassifier**

- [XGBClassifier](https://xgboost.readthedocs.io/en/latest/python/python_api.html)

## Requirements

### Poetry

- [Poetry 1.8.2+](https://python-poetry.org/)

### Python

- [Python 3.10 - 3.13](https://www.python.org/downloads/)

#### Packages

1. pyyaml
2. scikit-learn
3. xgboost
4. pyqt6
5. pandas
6. matplotlib
7. tensorflow
8. tqdm
9. torch

## Installation - Linux

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to your Path
export Path="$HOME/.local/bin:$PATH"

# Verify Poetry Installation
poetry --version

# Install PyQT6 Dependencies (Ubuntu Example)
sudo apt install libgl1 libxkbcommon-x11-0 libegl1-mesa libxcb-xinerama0 libxcb-cursor0 libx11-xcb1 libglu1-mesa qtwayland5

# Clone the repository and change your directory
git clone https://github.com/bcbradford/PyEmailAssistant.git
cd PyAssistant

# Install PyEmailAssistant
poetry install
```
## Usage

```bash
poetry run pyemailassistant
```

## Alternative Run: Running app.py

```bash
# Start Poetry Shell
poetry shell

# Change Directory to App.py Directory
cd src/pyemailassistant/

# Run App
python3 app.py
```

## License

### PyEmail Assistant
Copyright (c) 2024 Brent Bradford

This product is licensed under the Apache License 2.0 (see LICENSE.md for details).
