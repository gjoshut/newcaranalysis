from .scripts import database_update, to_database_postsale, add_new_to_database
import pandas as pd
import io
from .models import Postsales, Presale
from django_pandas.io import read_frame
import os, requests, lxml.html
from pandas.io.parsers import ParserError

def my_scheduled_job():
    if not Postsales.objects.all():
        data = database_update()
        to_database_postsale(data)
    else:
        add_new_to_database(Postsales)
