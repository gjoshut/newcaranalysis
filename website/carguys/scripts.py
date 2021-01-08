import os, requests, lxml.html
from datetime import timedelta, datetime, date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from math import sqrt
import io
from .models import Postsales, Presale
from django_pandas.io import read_frame
from pandas.io.parsers import ParserError


def add_new_to_database(Model):
    if Model == Postsales:
        data = database_update()
    if Model == Presale:
        data = price_estimator()
    old_data = read_frame(Model.objects.all())
    old_data = old_data.drop(['id'], axis = 1)
    new_data = data[~data.isin(old_data)].dropna()
    if Model == Postsales:
        to_database_postsale(new_data)
    if Model == Presale:
        Presale.objects.exclude(Day = date.today()).delete()
        to_database_presale(new_data)

def to_database_postsale(data_table):
    df = data_table
    records = df.to_records()
    for record in records:
        report = Postsales(
        Picture_Count = record[1],
        CR = record[2],
        Year = record[3],
        Make = record[4],
        Model = record[5],
        Style =  record[6],
        Odometer = record[7],
        Color = record[8],
        Stock = record[9],
        Grade = record[10],
        Sale_Date = record[11],
        Lane = record[12],
        Run_number = record[13],
        Price = record[14],
        )
        report.save()

def to_database_presale(data_table):
    df = data_table
    records = df.to_records()
    for record in records:
        report = Presale(
        Picture_Count = record[1],
        CR = record[2],
        Year = record[3],
        Make = record[4],
        Model = record[5],
        Style = record[6],
        Odometer = record[7],
        Color = record[8],
        Stock = record[9],
        Grade = record[10],
        Sale_Date = record[11],
        Run_number = record[12],
        Lane = record[13],
        Lot = record[14],
        VIN = record[15],
        Day = record[16],
        Predicted_Price = record[17],
        )
        report.save()

# def site_login(url_to_login, url_to_post):
#     s= requests.session()
#     login = s.get(url_to_login)
#     login_html = lxml.html.fromstring(login.text)
#     hidden_inputs = login_html.xpath(r'//form//input[@type = "hidden"]')
#     form = {x.attrib['name']: x.attrib['value'] for x in hidden_inputs}
#     form['username'] = 'ethan123'
#     form['password'] = 'Owasso918'
#     response = s.post(url_to_post, data = form)
#     return response

def database_update():
    s= requests.session()
    site_login('https://www.edgepipeline.com/components/login','https://www.edgepipeline.com/components/login/attempt')
    result = s.get('https://www.edgepipeline.com/components/report/postsale/csv/z66aa-all').content
    data = pd.read_csv(io.StringIO(result.decode('utf-8')))
    return data

# def next_possible_date(start_date = datetime.now()):
#     date = start_date
#     while True:
#         if date.weekday() == 2:
#             return date
#         elif date.weekday() == 4:
#             return date
#         else:
#             date += timedelta(1)
#     return date
#
#
# def next_sale_date():
#     d = next_possible_date()
#     s = requests.session()
#     while True:
#         presale_list = s.get('https://www.edgepipeline.com/components/report/presale/csv/z66aa-all/%s/%s/%s' % (d.year, d.month, d.day)).content
#         try:
#             presale_list = pd.read_csv(io.StringIO(presale_list.decode('utf-8')))
#             presale_list = presale_list.assign(Day = date.today())
#             return presale_list
#         except ParserError:
#             d = next_possible_date(d + timedelta(1))
#
def price_estimator():
    def site_login(url_to_login, url_to_post):
        login = s.get(url_to_login)
        login_html = lxml.html.fromstring(login.text)
        hidden_inputs = login_html.xpath(r'//form//input[@type = "hidden"]')
        form = {x.attrib['name']: x.attrib['value'] for x in hidden_inputs}
        form['username'] = 'ethan123'
        form['password'] = 'Owasso918'
        response = s.post(url_to_post, data = form)
        return response
    def prep_data_presale(data_frame):
        data_frame['Year']=pd.to_numeric(data_frame['Year'], errors='coerce')
        data_frame['Odometer']=pd.to_numeric(data_frame['Odometer'], errors='coerce')
        data_frame['Grade']=pd.to_numeric(data_frame['Grade'], errors='coerce')
        data_frame['Sale Date']=pd.to_datetime(data_frame['Sale Date'], errors='coerce')
        data_frame = data_frame.dropna()
        return data_frame
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
    presale_list = prep_data_presale(presale_list)
    data = read_frame(Postsales.objects.all())
    data = data.drop(['id'], axis = 1)
    data['sqrt_price']=[sqrt(x) for x in data['Price']]
    regr = LinearRegression()
    predicted_list = []
    for car in range(len(presale_list['Year'])):
        subset=data.query("Model==@presale_list['Model'].iloc[@car]")
        if subset.empty:
                predicted_list.append(np.nan)
        else:
            X=subset[['Year', 'Odometer']]
            y=subset[['sqrt_price']]
            to_predict=regr.fit(X,y)
            to_add=np.round(to_predict.predict([[presale_list['Year'].iloc[car],presale_list['Odometer'].iloc[car]]])**2, 2)
            predicted_list.append(float(to_add))
    presale_list['Predicted']=predicted_list
    return presale_list
# def price_estimator():
#     def prep_data_presale(data_frame):
#         data_frame['Year']=pd.to_numeric(data_frame['Year'], errors='coerce')
#         data_frame['Odometer']=pd.to_numeric(data_frame['Odometer'], errors='coerce')
#         data_frame['Grade']=pd.to_numeric(data_frame['Grade'], errors='coerce')
#         data_frame['Sale Date']=pd.to_datetime(data_frame['Sale Date'], errors='coerce')
#         return data_frame
#     s= requests.session()
#     site_login('https://www.edgepipeline.com/components/login','https://www.edgepipeline.com/components/login/attempt')
#     presale_list = next_sale_date()
#     presale_list = prep_data_presale(presale_list)
#     data = read_frame(Postsales.objects.all())
#     data = data.drop(['id'], axis = 1)
#     data['sqrt_price']=[sqrt(x) for x in data['Price']]
#     regr = LinearRegression()
#     predicted_list = []
#     for car in range(len(presale_list['Year'])):
#         subset=data.query("Model==@presale_list['Model'].iloc[@car]")
#         if subset.empty:
#                 predicted_list.append(np.nan)
#         else:
#             X=subset[['Year', 'Odometer']]
#             y=subset[['sqrt_price']]
#             to_predict=regr.fit(X,y)
#             to_add=np.round(to_predict.predict([[presale_list['Year'].iloc[car],presale_list['Odometer'].iloc[car]]])**2, 2)
#             predicted_list.append(float(to_add))
#     presale_list['Predicted']=predicted_list
#     return presale_list

def market_tracker():
    def prev_wednesday(adate):
        adate-= timedelta(days=1)
        while adate.weekday()!=2:
            adate-= timedelta(days=1)
        return adate
    def prev_friday(adate):
        adate-= timedelta(days=1)
        while adate.weekday()!=4:
            adate-= timedelta(days=1)
        return adate
    def day_checker():
        check=0
        dates=[]
        add=prev_friday(datetime.now())
        dates.append(add)
        add=prev_wednesday(add)
        dates.append(add)
        while check<=4:
            add=prev_friday(add)
            dates.append(add)
            check+=1
            add=prev_wednesday(add)
            dates.append(add)
            check+1
        return dates
    def site_login(url_to_login, url_to_post):
        login = s.get(url_to_login)
        login_html = lxml.html.fromstring(login.text)
        hidden_inputs = login_html.xpath(r'//form//input[@type = "hidden"]')
        form = {x.attrib['name']: x.attrib['value'] for x in hidden_inputs}
        form['username'] = 'ethan123'
        form['password'] = 'Owasso918'
        response = s.post(url_to_post, data = form)
        return response
    def prep_data_data(data_frame):
        data_frame['Year']=pd.to_numeric(data_frame['Year'], errors='coerce')
        data_frame['Odometer']=pd.to_numeric(data_frame['Odometer'], errors='coerce')
        data_frame['Price']=pd.to_numeric(data_frame['Price'], errors='coerce')
        data_frame['Grade']=pd.to_numeric(data_frame['Grade'], errors='coerce')
        data_frame['Sale Date']=pd.to_datetime(data_frame['Sale Date'], errors='coerce')
        data_frame = data_frame.dropna()
        return data_frame
    def prep_data_presale(data_frame):
        data_frame['Year']=pd.to_numeric(data_frame['Year'], errors='coerce')
        data_frame['Odometer']=pd.to_numeric(data_frame['Odometer'], errors='coerce')
        data_frame['Grade']=pd.to_numeric(data_frame['Grade'], errors='coerce')
        data_frame['Sale Date']=pd.to_datetime(data_frame['Sale Date'], errors='coerce')
        data_frame = data_frame.dropna()
        return data_frame
    s= requests.session()
    site_login('https://www.edgepipeline.com/components/login','https://www.edgepipeline.com/components/login/attempt')
    data=pd.DataFrame()
    dates=day_checker()
    urls=['https://www.edgepipeline.com/components/report/postsale/csv/z66aa-all/%s/%s/%s' % (x.year, x.month, x.day) for x in dates]
    for i in urls:
        result=s.get(i).content
        try:
            result = pd.read_csv(io.StringIO(result.decode('utf-8')))
        except:
            result = pd.DataFrame()
        data= data.append(result)
    def car_search(point,database,path):
        fig=plt.figure()
        ax=fig.add_subplot(1,1,1)
        for i in range(len(point['Year'])):
            ax.clear()
            year=point.loc[i,"Year"]
            odometer=point.loc[i,"Odometer"]
            model=point.loc[i,"Model"]
            data=database.query('Model==@model and Year==@year')
            data_sorted=data.sort_values(by=['Sale Date'])
            dates=data_sorted['Sale Date']
            dates_sorted=['%s-%s' % (x.month, x.day) for x in dates]
            price=data_sorted['Price']
            y_pos=np.arange(len(dates))
            p=ax.bar(y_pos, price)
            ax.set_xticks(y_pos)
            ax.set_ylabel('Price')
            ax.set_xticklabels(dates_sorted)