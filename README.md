# google-analytics-api-pandas
simple python script to save [google analytics api](https://github.com/googleapis/google-api-python-client) query responses as a [pandas](https://github.com/pandas-dev/pandas) dataframe

# How To
install all the requirements with `pip install -r pip_req`

run the analytics_template.py

## Example Usage

```python
query = report.build_report(analytics,
                      view_id='1234567890',
                      start_date='2020-01-01',
                      end_date=dt.date.today().strftime('%F'),
                      metrics=[{'expression':'ga:sessions'},{'expression':'ga:users'}],
                      dimensions=[{'name':'ga:date'}]
                     )

ga_report=report.get_report(query)

ga_report_dataframe=report.ga_to_df(ga_report)

```

find your dimensions and metrics [here](https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/)
