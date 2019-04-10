from init import celery, pg_engine


@celery.task()
def calulate_achievement():
    """ 调用pg.func生成业绩表 """
    conn = pg_engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.callproc('calculate_achievement')
        cursor.close()
        conn.commit()
    finally:
        conn.close()
