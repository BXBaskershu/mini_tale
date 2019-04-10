from init import celery


@celery.task()
def test():
    print('this tale test')
