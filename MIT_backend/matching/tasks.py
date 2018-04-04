from celery import shared_task


@shared_task
def add(a, b):
    import time
    time.sleep(3)
    return a+b
