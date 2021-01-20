import os, requests, lxml.html
from datetime import timedelta, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import io


def to_implement():
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
