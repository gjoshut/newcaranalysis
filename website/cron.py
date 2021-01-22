from carguys.scripts import database_update, to_database_presale, to_database_postsale, add_new_to_database
import pandas as pd
import io
from datetime import timedelta, datetime, date
from carguys.models import Postsales, Presale
from django_pandas.io import read_frame
import os, requests, lxml.html
from pandas.io.parsers import ParserError
import django

def my_scheduled_job():
    if not Postsales.objects.all():
        data = database_update()
        to_database_postsale(data)
    else:
        add_new_to_database(Postsales)

def presale_list_grabber():
    def site_login(url_to_login, url_to_post):
        login = s.get(url_to_login)
        login_html = lxml.html.fromstring(login.text)
        hidden_inputs = login_html.xpath(r'//form//input[@type = "hidden"]')
        form = {x.attrib['name']: x.attrib['value'] for x in hidden_inputs}
        form['username'] = 'ethan123'
        form['password'] = 'Owasso918'
        response = s.post(url_to_post, data = form)
        return response
    # def prep_data_presale(data_frame):
    #     data_frame['Year']=pd.to_numeric(data_frame['Year'], errors='coerce')
    #     data_frame['Odometer']=pd.to_numeric(data_frame['Odometer'], errors='coerce')
    #     data_frame['Grade']=pd.to_numeric(data_frame['Grade'], errors='coerce')
    #     data_frame['Sale Date']=pd.to_datetime(data_frame['Sale Date'], errors='coerce')
    #     data_frame = data_frame.dropna()
    #     return data_frame
    def next_possible_date(start_date = datetime.now()):
        date = start_date
        while True:
            if date.weekday() == 2:
                return date
            elif date.weekday() == 4:
                return date
            else:
                date += timedelta(1)
        return date
    def next_sale_date():
        d = next_possible_date()
        while True:
            presale_list = s.get('https://www.edgepipeline.com/components/report/presale/csv/z66aa-all/%s/%s/%s' % (d.year, d.month, d.day)).content
            try:
                presale_list = pd.read_csv(io.StringIO(presale_list.decode('utf-8')))
                presale_list = presale_list.assign(Day = date.today())
                return presale_list
            except (ParserError, AttributeError):
                d = next_possible_date(d + timedelta(1))
    s= requests.session()
    site_login('https://www.edgepipeline.com/components/login','https://www.edgepipeline.com/components/login/attempt')
    presale_list = next_sale_date()
    if not Presale.objects.all():
        to_database_presale(presale_list)
    else:
        # old_data = read_frame(Presale.objects.all())
        # old_data = old_data.drop(['id'], axis = 1)
        # new_data = presale_list[~presale_list.isin(old_data)].dropna()
        Presale.objects.exclude(Day = date.today()).delete()
        to_database_presale(presale_list)
        for row in Presale.objects.all().reverse():
            if Presale.objects.filter(VIN = row.VIN).count() > 1:
                row.delete()


if __name__ == "__main__":
    import django
    django.setup()
    presale_list_grabber()
