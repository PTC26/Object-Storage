from config import *
import random
import string

def create_random_data():
    data = ''.join(random.choices(string.ascii_letters + string.digits,k=DATA_SIZE))
    return data

def build_bucket_name():
    return f"{COMPANY}-{PROJECT}-{ENV}-{'hh'}"