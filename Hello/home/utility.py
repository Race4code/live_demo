
from django.db import connection

def fetch_data(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        data=cursor.fetchall()
    return data