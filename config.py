import os
from dotenv import load_dotenv
from pathlib import Path
import logging


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
NAME = os.environ["NAME"]
API_KEY = os.environ["API_KEY"]
file_log = logging.FileHandler(BASE_DIR/'sample.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out), 
                    format='[%(asctime)s]|%(levelname)s|%(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S', 
                    level=logging.INFO)
logger = logging.getLogger("logger")