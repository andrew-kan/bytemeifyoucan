# tasks.py
from app import celery

@celery.task
def add(x, y):
    return x + y

# More tasks...
