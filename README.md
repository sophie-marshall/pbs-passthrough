# PBS Passthrough
**Hack Day | Spring 2024**


Flask demo app to show how open source facial regonition tools can help retrieve person specific metadata for a video in near real-time

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Installation
Clone the git repository
```bash
git clone https://github.com/srmarshall-pbs/pbs-passthrough.git
```

Navigate to the application directory 
```bash
cd pbs_passthrough
```

Create and activate a virtual environment 
```bash
python3 -m venv venv
source venv/bin/activate
```

Install required packages
```bash
pip install -r requirements.txt
```

## Usage

Run the flask app
```bash
python app.py
```

## Configuration 
Create a `.env` file in the root of the `pbs_passthrough` directory and define the following variables.

```python
PG_HOST = ""
PG_USER = ""
PG_PASSWORD = ""
PG_DB = ""

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
```
