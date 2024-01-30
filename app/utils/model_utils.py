from uuid import uuid4
from datetime import datetime

def generate_id():
    return str(uuid4())

def generate_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return str(dt_string)