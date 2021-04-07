import pandas as pd

# John Hopkins raw csv paths
url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"

# mark originals
df_original_confirmed = pd.read_csv(url_confirmed)
df_original_deaths = pd.read_csv(url_deaths)
df_original_recovered = pd.read_csv(url_recovered)

# output csv
confirmed_out = "data/df_confirmed.csv"
deaths_out = "data/df_deaths.csv"
recovered_out = "data/df_recovered.csv"

# export to csv
df_original_confirmed.to_csv(confirmed_out)
df_original_deaths.to_csv(deaths_out)
df_original_recovered.to_csv(recovered_out)