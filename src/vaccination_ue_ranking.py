import pandas as pd
import json

COUNTRIES_UE = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden"
]

def import_data():
    return pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')

def get_ue_data(df):
    return df[df["location"].isin(COUNTRIES_UE)].reset_index()

def get_data_last_date(df):
    max_date = df["date"].max()
    return df[df["date"]==max_date].reset_index()

def get_people_vaccinated_per_hundred_lastdate(df):
    return df["people_vaccinated_per_hundred"].values[0]

def get_speed_people_vaccinated_per_hundred_lastdate(df):
    df = df.sort_values(by="date")
    return round(df["people_vaccinated_per_hundred"].values[-1] - df["people_vaccinated_per_hundred"].values[-7], 1)

def get_dict_vaccination_per_ue_country(df):
    dict_people_vaccinated = {}
    for country in COUNTRIES_UE:
        df_country = df[df["location"]==country]
        df_lastdate = get_data_last_date(df_country)
        people_vaccinated_per_hundred = get_people_vaccinated_per_hundred_lastdate(df_lastdate)
        speed_people_vaccinated_per_hundred = get_speed_people_vaccinated_per_hundred_lastdate(df_country)
        dict_people_vaccinated[country] = {"people_vaccinated_per_hundred": people_vaccinated_per_hundred,
                                           "speed_people_vaccinated_per_hundred": speed_people_vaccinated_per_hundred}
    return dict_people_vaccinated

def export_dict_people_vaccinated(dict_people_vaccinated):
    with open("../data/output/vaccination_ue_ranking.json", "w") as file:
        file.write(json.dumps(dict_people_vaccinated))

df = import_data()
df_ue = get_ue_data(df)
dict_people_vaccinated = get_dict_vaccination_per_ue_country(df_ue)
export_dict_people_vaccinated(dict_people_vaccinated)
