# Import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import pandas as pd

from flask import Flask, jsonify
import json

#####################################################
##############                        ###############
##############     Database Setup     ###############
##############                        ###############
#####################################################
engine = create_engine("sqlite:///data/unemployment.db")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Create an app
app = Flask(__name__)
# Do not sort keys
app.json.sort_keys = False

# Save the tables into variables
Unemployment_Rate = Base.classes.unemployment_rate
Unemployment_Rate_S = Base.classes.unemployment_rate_sex

# Create a dictionary to translate month numbers to month names
month_dict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
              8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}


# List out all columns in Unemployment_Rate
inspector = inspect(Unemployment_Rate)
all_columns = [columns.key for columns in inspector.mapper.column_attrs]

# all_columns = ['date', 'overall_rate', 'age_16_17_rate', 'age_16_19_rate', 'age_18_19_rate', 'age_16_24_rate', 'age_20_24_rate',
#                'age_25_34_rate', 'age_25_54_rate', 'age_35_44_rate', 'age_45_54_rate', 'age_25plus_rate', 'age_55plus_rate']

# Short form of the columns 
all_columns_short = ["overall_rate", "16_17", "16_19", "16_24", "18_19", "20_24", "25_34", "25_54", "35_44", "45_54", "25plus", "55plus"]

# List of all column names for data for men
all_columns_m = ['date', 'men_rate', 'men_16_17_rate', 'men_16_19_rate', 'men_18_19_rate', 'men_16_24_rate', 'men_20_24_rate',
                       'men_25_34_rate', 'men_25_54_rate', 'men_35_44_rate', 'men_45_54_rate', 'men_25plus_rate', 'men_55plus_rate']

# List of all column names for data for women
all_columns_w = ['date', 'women_rate', 'women_16_17_rate', 'women_16_19_rate', 'women_18_19_rate', 'women_16_24_rate', 'women_20_24_rate',
                       'women_25_34_rate', 'women_25_54_rate', 'women_35_44_rate', 'women_45_54_rate', 'women_25plus_rate', 'women_55plus_rate']


# List of all the years available
session = Session(engine)
results = session.query(Unemployment_Rate.date).distinct().all()
session.close()

# List of all the dates' years
years = [pd.to_datetime(date[0]).year for date in results]

# Remove the duplicates and save it in year_list
year_list = []
for year in years:
    if year not in year_list:
        year_list.append(year)



##################################################
##############                     ###############
##############     Index route     ###############
##############                     ###############
##################################################
@app.route("/")
def home():
    return ("Welcome to the homepage<br/><br/>"
            "Available routes:<br/>"
            "/api/v1.0/unemployment_rate/(year) (Returns unemployment rate depending on (year) by month)<br/>"
            "/api/v1.0/unemployment_rate/(year)/(data) (Returns unemployment rate of age range (data) depending on (year) by month)<br/>"
            "/api/v1.0/unemployment_rate/s/(year)/(sex) (Returns unemployment rate of (sex) depending on (year) by month)<br/><br/>"
            "Available options for (data):<br/>"
            "overall_rate<br/>"
            "16_17<br/>"
            "16_19<br/>"
            "16_24<br/>"
            "18_19<br/>"
            "20_24<br/>"
            "25_34<br/>"
            "25_54<br/>"
            "35_44<br/>"
            "45_54<br/>"
            "25plus<br/>"
            "55plus<br/>"
            )


##################################################
######                                      ######
######   Route for data depending on year   ######
######                                      ######
##################################################
@app.route("/api/v1.0/unemployment_rate/<year>")
def all_data(year):

    # Check if the year selected is available
    if year not in year_list:
        return jsonify("Error: The (year) you have selected is not in the available options")
    
    # Create a Session to connect to DB
    session = Session(engine)

    # List of columns for all data to query
    columns = [getattr(Unemployment_Rate, col) for col in all_columns]

    # Query the wanted results
    results = session.query(*columns).filter(Unemployment_Rate.date.like(f"{year}%")).all()

    # Close the session
    session.close()

    # Define a list to jsonify unemployment rate
    unemp_rate = [{"title": f"Unemployment data for the year {year} by month"}]

    # Loop through the results list to add to unemp_rate to jsonify
    for row in results:
        # Convert the date entry to datetime dtype
        date = pd.to_datetime(row.date)

        # Add the current row (which is the month) to the dictionary in unemp_rate
        unemp_rate[0][month_dict[date.month]] = {}

        for i in range(1, len(all_columns)):

            # Looks like "January": value in the dictionary
            unemp_rate[0][month_dict[date.month]][all_columns[i]] = row[i]

    return jsonify(unemp_rate)


###########################################################
######                                               ######
######   Route for data depending on year and data   ######
######                                               ######
###########################################################

@app.route("/api/v1.0/unemployment_rate/<year>/<data>")
def year_data(year, data):

    # Check if the data selected exists
    if data =="overall_rate":

        # These are the strings to input for the column name later on
        data_str = "overall_rate"
        title = f"Overall unemployment rate from in {year} by month"
    
    elif data in all_columns_short[1:]:

        # These are the strings to input for the column name later on
        data_str = "age_" + data + "_rate"
        title = f"Unemployment rate for {data} in {year} by month"
    
    else:
        return jsonify("Error: The (data) you have selected is not in the available options")

    # Check if the year selected is available
    if year not in year_list:
        return jsonify("Error: The (year) you have selected is not in the available options")
    
    # Query the wanted results
    session = Session(engine)

    results = session.query(Unemployment_Rate.date, getattr(Unemployment_Rate, data_str)).filter(
        Unemployment_Rate.date.like(f"{year}%")).all()

    session.close()

    # Define a list to jsonify unemployment rate
    unemp_rate = [{"title": title}]

    # Loop through the results list to add to unemp_rate to jsonify
    for row in results:

        # Convert the date entry to datetime dtype to access month
        date = pd.to_datetime(row.date)

        # Add the current row (which is the month) to the dictionary in unemp_rate
        unemp_rate[0][month_dict[date.month]] = row[1]

    return jsonify(unemp_rate)


##########################################################
######                                              ######
######   Route for data depending on year and sex   ######
######                                              ######
##########################################################

@app.route("/api/v1.0/unemployment_rate/s/<year>/<sex>")
def data_year_sex(year, sex):

    # Check if the year selected is available
    if year not in year_list:
        return jsonify("Error: The (year) you have selected is not in the available options")
    
    # Options for sex category
    men_names = ["men", "male", "m"]
    women_names = ["women", "female", "f", "w"]

    # This section queries for men's results
    if sex in men_names:

        # Create a Session to connect to DB
        session = Session(engine)

        # List of all columns for data for women
        men_columns = [getattr(Unemployment_Rate_S, col) for col in all_columns_m]

        # Query the wanted results
        results = session.query(*men_columns).filter(Unemployment_Rate_S.date.like(f"{year}%")).all()

        # Close the session
        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [
            {"title": f"Unemployment data for the year {year} by month (Male)"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)

            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = {}

            for i in range(1, len(all_columns_m)):

                # Looks like "January": value in the dictionary
                unemp_rate[0][month_dict[date.month]][all_columns_m[i]] = row[i]

        return jsonify(unemp_rate)

    # This section queries for women's results
    elif sex in women_names:

        # Create a Session to connect to DB
        session = Session(engine)

        # List of all columns for data for women
        women_columns = [getattr(Unemployment_Rate_S, col) for col in all_columns_w]

        # Query the wanted results
        results = session.query(*women_columns).filter(Unemployment_Rate_S.date.like(f"{year}%")).all()
        
        # Close the session
        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [
            {"title": f"Unemployment data for the year {year} by month (Female)"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)

            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = {}

            for i in range(1, len(all_columns_w)):

                # Looks like "January": value in the dictionary
                unemp_rate[0][month_dict[date.month]][all_columns_w[i]] = row[i]

        return jsonify(unemp_rate)

    else:
        return jsonify("error")


################################################################
######                                                    ######
######   Route for data depending on start and end year   ######
######                                                    ######
################################################################

@app.route("/api/v1.0/unemployment_rate/y/")
@app.route("/api/v1.0/unemployment_rate/y/<start_year>/")
@app.route("/api/v1.0/unemployment_rate/y/<start_year>/<end_year>")
@app.route("/api/v1.0/unemployment_rate/y/<start_year>/<end_year>/<data>")
def all_data_st_end_year(start_year="1948", end_year="2023", data="overall_rate"):

    # Check if the data selected exists
    if data =="overall_rate":

        # These are the strings to input for the column name later on
        data_str_m = "men_rate"
        data_str_w = "women_rate"
        title = f"Average overall unemployment rate from {start_year} to {end_year}"
    
    elif data in all_columns_short[1:]:

        # These are the strings to input for the column name later on
        data_str_m = "men_" + data + "_rate"
        data_str_w = "women_" + data + "_rate"
        title = f"Average unemployment rate for {data} from {start_year} to {end_year}"
    
    else:
        return jsonify("Error: The (data) you have selected is not in the available options")

    # Check if the year selected is available
    if start_year not in year_list:
        return jsonify("Error: The (start_year) you have selected is not in the available options")
    elif end_year not in year_list:
        return jsonify("Error: The (end_year) you have selected is not in the available options")
    
    # Dictionary to jsonify with title
    unemp_rate_m_w = [{'title': title}]

    # Dictionary for men and women data to jsonify
    unemp_rate_m_w[0]['men'] = {}
    unemp_rate_m_w[0]['women'] = {}

    # Create a Session Object to Connect to DB
    session = Session(engine)

    # Loop through the years starting from start_year to end_year
    for i in range(int(start_year), int(end_year)+1):

        # The date string is formatted yyyy-mm-dd so we define the strings below to use to filter dates
        start_date = str(i) + "-01-01"
        end_date = str(i) + "-12-01"

        # Query the data based on the starting year and the ending year and data
        results_men = session.query(func.avg(getattr(Unemployment_Rate_S, data_str_m)))\
            .filter(Unemployment_Rate_S.date >= start_date).filter(Unemployment_Rate_S.date <= end_date).all()[0][0]

        results_women = session.query(func.avg(getattr(Unemployment_Rate_S, data_str_w)))\
            .filter(Unemployment_Rate_S.date >= start_date).filter(Unemployment_Rate_S.date <= end_date).all()[0][0]
        
        # Add the current data to the initial dictionary to jsonify
        unemp_rate_m_w[0]["men"][str(i)] = results_men
        unemp_rate_m_w[0]["women"][str(i)] = results_women

    # Close the session
    session.close()

    return jsonify(unemp_rate_m_w)
    # # You can use start_year, end_year, and data in your function
    # return f"Start Year: {start_year}, End Year: {end_year}, Data: {data}"



if __name__ == "__main__":
    app.run(debug=True)
