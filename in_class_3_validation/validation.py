import pandas as pd
import pandas_schema
import math
import datetime

#returns true if not null, false if null
def check_not_null(value):
    result = False
    # print("check_not_null")
    # print(type(value))
    if(math.isnan(value)):
        result =  False
    else:
        result = True
    
    # print("end check_not_null")
    return result

def check_number(value):
    result = False
    # print("check_int")
    if(isinstance(value, int) or isinstance(value, float)):
        result = True
    else:
        result = False

    # print("end check_int")
    return result

def check_crash_id(data):
    errors = 0
    for item in data["Crash ID"]:
        if(not check_not_null(item)):
            print(item)
            errors += 1
        elif(not check_number(item)):
            print(item)
            errors += 1
    
    return errors

def check_record_type(data):
    errors = 0
    for item in data["Record Type"]:
        if(not check_not_null(item)):
            print("null:", item)
            print(item)
            errors += 1
        elif(not check_number(item)):
            print("not int or float:", item)
            print(item)
            errors += 1
        elif(item != 1 and item != 2 and item != 3):
            print("not 1, 2, or 3:", item)
            print("type:", type(item))
            print(item)
            errors += 1

    return errors

def check_hour_bounds(data):
    # should only exist for record type 1
    errors = 0
    for item in data["Crash Hour"]:
        if(not check_not_null(item)):
            print("null:", item)
            print(item)
            errors += 1
        elif(not check_number(item)):
            print("not int or float:", item)
            print(item)
            errors += 1
        elif(not (item >= 1 or item <= 24)):
            print(" between 1 and 24", item)
            print(item)
            errors += 1

    return errors

def check_highway_number(data):
    # should only exist for record type 1
    errors = 0
    for item in data["Highway Number"]:
        if(not check_not_null(item)):
            print("null:", item)
            print(item)
            errors += 1
        elif(not check_number(item)):
            print("not int or float:", item)
            print(item)
            errors += 1
        elif(not item == 26):
            print("is not 26", item)
            print(item)
            errors += 1

    return errors

def check_day_code(data):
    # does the day of the week match what the date should be
    # should only exist for record type 1 

    errors = 0
    year_list = data["Crash Year"]
    month_list = data["Crash Month"]
    day_list = data["Crash Day"]
    week_code_list = data["Week Day Code"]

    # count = 0

    for (year_float, month_float, day_float, week_code_float) in zip(year_list, month_list, day_list, week_code_list):
        year = int(year_float)
        month = int(month_float)
        day = int(day_float)
        week_code = int(week_code_float)
        
        # week_code goes from 1 to 7, while datetime goes from 0 to 6
        # week_code's week starts on a sunday, while datetime starts on a monday
        date_to_week_code = (datetime.date(year, month, day).weekday() + 2)
        if(date_to_week_code == 8):
            date_to_week_code = 1 

        # print("date: " + str(year) + ", " + str(month) + ", " + str(day))


        if(not check_not_null(week_code)):
            print("null:", week_code)
            print(item)
            errors += 1
        elif(not check_number(week_code)):
            print("not int or float:", week_code)
            print(week_code)
            errors += 1
        elif(not week_code in [1, 2, 3, 4, 5, 6, 7]):
            print("not 1 to 7", week_code)
            print(week_code)
            errors += 1
        elif(not week_code == date_to_week_code):
            print("week code not match")
            print("date_to_week_code:", date_to_week_code)
            print("week_code", week_code)
            print("")
            errors += 1
            count += 1
        
        # if(count > 5):
        #     return 0

    return errors

def check_month_number(data):
    # should only apply to record type 1
    errors = 0
    for item in data["Crash Month"]:
        if(not check_not_null(item)):
            print("null:", item)
            print(item)
            errors += 1
        elif(not check_number(item)):
            print("not int or float:", item)
            print(item)
            errors += 1
        elif(not (item <= 31 and item >= 1)):
            print("is not between 0 and 31", item)
            print(item)
            errors += 1

    return errors
        
def check_vehicle_id_exist(data):
    # should only apply to record type 2 and 3
    errors = 0
    for item in data["Vehicle ID"]:
        if(not check_not_null(item)):
            print("null:", item)
            print(item)
            errors += 1
        elif(not check_number(item)):
            print("not int or float:", item)
            print(item)
            errors += 1

    return errors

def check_unique_crash_id_participant(data):
    # should only apply to record 3
    errors = 0
    combined = data[["Crash ID", "Participant ID"]].values.tolist()
    # set(combined)

    # if(not len(set(combined)) == len(combined)):
    #     return 1
    # else:
    #     return 0

    # print(combined[0])
    for i in range(1, len(combined)):
        for j in range(i, len(combined)):
            if(not i == j):
                if(combined[i][0] == combined[j][0]):
                    if(combined[i][1] == combined[j][1]):
                        errors += 1

    return errors

def check_gender(data):
    # only applies to record type 3
    errors = 0
    for item in data["Sex"]:
        if(not check_not_null(item)):
            print("null:", item)
            print(item)
            errors += 1
        elif(not check_number(item)):
            print("not int or float:", item)
            print(item)
            errors += 1

    return errors

def check_age(data):
    # only applies to record type 3

    errors = 0
    for item in data["Age"]:
        if(not check_not_null(item)):
            # print("null:", item)
            # print(item)
            errors += 1
        elif(not check_number(item)):
            print("not int or float:", item)
            print(item)
            errors += 1

    return errors



df = pd.read_csv("Oregon Hwy 26 Crash Data for 2019 - Crashes on Hwy 26 during 2019.csv")

grouped = df.groupby(['Record Type'])

# for col in df.columns:
#     print(" pandas_schema.column.Column('" + col + "', ),")

# print(grouped.head())

record_1 = grouped.get_group(1)
record_2 = grouped.get_group(2)
record_3 = grouped.get_group(3)

total_errors = 0

total_errors += check_crash_id(record_1)
total_errors += check_crash_id(record_2)
total_errors += check_crash_id(record_3)

print("total_errors 1:", total_errors)

total_errors += check_record_type(record_1)
total_errors += check_record_type(record_2)
total_errors += check_record_type(record_3)

print("total_errors 2:", total_errors)

total_errors += check_hour_bounds(record_1) 

print("total_errors 3:", total_errors)

total_errors += check_highway_number(record_1)

print("total_errors 4:", total_errors)

total_errors += check_day_code(record_1)

print("total_errors 5:", total_errors)

total_errors += check_month_number(record_1)

print("total_errors 6:", total_errors)

total_errors += check_vehicle_id_exist(record_2)
total_errors += check_vehicle_id_exist(record_3)

print("total_errors 7:", total_errors)

total_errors += check_unique_crash_id_participant(record_3)

print("total_errors 8:", total_errors)

total_errors += check_gender(record_3)

print("total_errors 9:", total_errors)

total_errors += check_age(record_3)

print("total_errors 10:", total_errors)



# resources
# https://medium.com/@bogdan.cojocar/how-to-do-column-validation-with-pandas-bbeb38f88990
# https://www.datacamp.com/community/tutorials/pandas-read-csv