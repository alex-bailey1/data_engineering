import pandas as pd
import math
import json

def read_data(filename):

    data = pd.read_csv(filename)

    return data

#group the rows into a dictionary, where each tract id is a list 
def group_census_rows(data):
    county_dict = {}

    is_first = True

    # print("data:")
    # print(data)

    for index, row  in data.iterrows():
        # if(is_first):
        #     break
        
        # print(index)

        state = row[1]
        county = row[2]
        new_item = {}
        new_item["pop"] = row[3]
        new_item["poverty"] = row[17] #percentage of population in poverty
        new_item["income"] = row[13]
        new_item["per_cap_income"] = row[15]

        # if(county == "Bristol Bay Borough"):
        #     print(row)
        #     print(new_item)


        if(math.isnan(new_item["pop"])):
            continue
        elif(math.isnan(new_item["income"])):
            continue
        elif(math.isnan(new_item["poverty"])):
            continue
        elif(math.isnan(new_item["per_cap_income"])):
            continue

        if state not in county_dict:
            county_dict[state] = {}

        if county in county_dict[state]:
            county_dict[state][county].append(new_item)
        else:
            county_dict[state][county] = [new_item]

    return county_dict

def combine_census_counties(data):
    # print(type(data))
    # print(data["Alabama"])
    new_data = {}
    #structure {"state"}{"county"}[{pop, poverty, per_cap_income}, ... }

    for state_key, state_value in data.items():
        # print(type(item))
        # print(item)

        for county_key, county_value in state_value.items():
            pop_count = 0
            poverty_pop = 0

            total_income = 0 #income per cap * population of county
            
            
            for item in county_value:
                
                pop_count += item["pop"]
                poverty_pop += item["poverty"] * item["pop"]
                total_income += item["pop"] * item["per_cap_income"]
            
            # print(county_key)
            # print(county_value)
            
            if state_key in new_data:
                new_data[state_key][county_key] = {"pop": pop_count, "poverty": poverty_pop/pop_count, "income_per_cap": total_income/pop_count}
            else:
                new_data[state_key] = {}
                new_data[state_key][county_key] = {"pop": pop_count, "poverty": poverty_pop/pop_count, "income_per_cap": total_income/pop_count}
            

            

    return new_data


def write_data(data, filename):

    with open(filename, "w") as out_file:
        json.dump(data, out_file)

def read_json_file(filename):

    with open(filename, "r") as in_file:
        data = json.load(in_file)

    return data

def create_condense_census():

    data = read_data("acs2017_census_tract_data.csv")

    sub_county_dict = group_census_rows(data)

    county_data = combine_census_counties(sub_county_dict)

    write_data(county_data, "condensed_census.json")


def group_covid(data):

    new_data = {}

    for index, row in data.iterrows():

        # if(math.isnan(row["date"])):
        #     continue
        # if(math.isnan(row["state"])):
        #     continue
        # if(math.isnan(row["county"])):
            # continue
        if(math.isnan(row["cases"])):
            continue
        if(math.isnan(row["deaths"])):
            continue


        state = row["state"]
        county = row["county"]
        new_item = {"date": row["date"], "cases": row["cases"], "deaths": row["deaths"]}


        if state not in new_data:
            new_data[state] = {}

        if county in new_data[state]:
            new_data[state][county].append(new_item)
        else:
            new_data[state][county] = [new_item]

    return new_data


def combine_covid(data):

    # new_data = pd.DataFrame(data={"state": ["state_key"], "county": ["county_key"], "total_cases": ["total_cases"], "total_deaths": ["total_deaths"], "dec_2020_cases": ["dec_cases"], "dec_2020_deaths": ["dec_deaths"]}, columns=["state", "county", "total_cases", "total_deaths", "dec_2020_cases", "dec_2020_deaths"])

    new_data = pd.DataFrame(columns=["state", "county", "total_cases", "total_deaths", "dec_2020_cases", "dec_2020_deaths"])

    # print(new_data)

    for state_key, state_value in data.items(): 
        # print(state_key)
        for county_key, county_value in state_value.items():
            total_cases = 0
            total_deaths = 0
            dec_cases = 0
            dec_deaths = 0

            for item in county_value:
                total_cases += item["cases"]
                total_deaths += item["deaths"]

                if(item["date"][5:7] == "12"):
                    dec_cases += item["cases"]
                    dec_deaths += item["deaths"]

            # new_data = new_data.append(pd.DataFrame({"state": [state_key], "county": [county_key], "total_cases": [total_cases], "total_deaths": [total_deaths], "dec_2020_cases": [dec_cases], "dec_2020_deaths": [dec_deaths]}))
            new_data = new_data.append({"state": state_key, "county": county_key, "total_cases": total_cases, "total_deaths": total_deaths, "dec_2020_cases": dec_cases, "dec_2020_deaths": dec_deaths}, ignore_index=True)

            # print(new_data)

    return new_data

def create_condense_covid():
    
    raw_data = read_data("COVID_county_data.csv")

    grouped_data = group_covid(raw_data)

    df = combine_covid(grouped_data)

    df.to_csv("condensed_covid.csv")

    # print(df)

    
df = pd.read_csv("condensed_covid.csv")

value = df.loc[(df["state"] == "Oregon") & (df["county"] == "Malheur")]
print(value.set_index("state").to_dict("list"))



