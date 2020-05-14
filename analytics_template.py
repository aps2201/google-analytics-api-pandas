#!/usr/bin/env python
# coding: utf-8

# In[4]:


from apiclient.discovery import build
import google.auth
import pandas as pd
from pandas import DataFrame as df
import re
import datetime as dt


# In[5]:


from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'apsweb-07ed3c8c3585.json')
credentials = credentials.with_scopes(['https://www.googleapis.com/auth/analytics.readonly'])

analytics = build('analyticsreporting', 'v4', credentials=credentials)
VIEW_ID='136660919'


# In[10]:


class report:
    def build_report(analytics,view_id,start_date,end_date,metrics=[],dimensions=[]): # create a query to build report
        return analytics.reports().batchGet(
            body={
                "reportRequests":
                [
                    {
                        "viewId":view_id,
                        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
                        "metrics": metrics,
                        "dimensions": dimensions,
                        "samplingLevel":  "LARGE"
                    }
                ]
            })
    def get_report(report_build):
        return report_build.execute()
    
    def ga_to_df(ga): # google analytics report from get_report()
        # split into dicts
        kv=ga.get('reports')[0] 
        
        # get headers
        dimensions=[re.sub('ga:','',dim) for dim in kv.get('columnHeader').get('dimensions')] # list comprehension, re.sub each element and make list        
        metric_headers=kv.get('columnHeader').get('metricHeader').get('metricHeaderEntries')
        metrics=[]
        for metrics_ in metric_headers:
            metrics.append(re.sub('ga:','',metrics_['name']))
        
        # get data, dimensions labels and metric values
        data=kv.get('data').get('rows') 
        labels=[]
        for dimension_labels in data:
            labels.append(dimension_labels.get('dimensions'))
            values=[]
        for metric_values in data:
            for values_ in metric_values.get('metrics'):
                values.append(values_.get('values'))
        
        # dataframing    
        values=df.from_dict(values)
        values=values.rename(columns=dict(zip(values.columns.to_list(),metrics)))
        
        labels=df.from_dict(labels)
        labels=labels.rename(columns=dict(zip(labels.columns.to_list(),dimensions)))
        
        x=pd.concat([labels,values],axis=1)
        return x


# In[11]:


q = report.build_report(analytics,
                      view_id='136660919',
                      start_date='2020-04-01',
                      end_date=dt.date.today().strftime('%F'),
                      metrics=[{'expression':'ga:sessions'},{'expression':'ga:users'},{'expression':'ga:totalEvents'}],
                      dimensions=[{'name':'ga:date'},{'name':'ga:deviceCategory'},{'name':'ga:eventCategory'},{'name':'ga:eventLabel'}]
                     )


# In[12]:


ga=report.get_report(q)


# In[13]:


x=report.ga_to_df(ga)
report.ga_to_df(ga)


# In[60]:


x.dtypes


# In[36]:


dt.datetime.today().strftime("%F %H%M%S")


# In[ ]:




