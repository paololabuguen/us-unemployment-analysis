# Import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
            "/api/v1.0/unemployment_rate_s/(year)/(sex) (Returns unemployment rate of (sex) depending on (year) by month)<br/><br/>"
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
            "20plus<br/>"
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

    session = Session(engine)
 
    results = session.query(Unemployment_Rate.date, Unemployment_Rate.overall_rate, Unemployment_Rate.age_16_17_rate, Unemployment_Rate.age_16_19_rate, Unemployment_Rate.age_18_19_rate, Unemployment_Rate.age_16_24_rate, Unemployment_Rate.age_20_24_rate, 
                            Unemployment_Rate.age_25_34_rate, Unemployment_Rate.age_25_54_rate, Unemployment_Rate.age_35_44_rate, Unemployment_Rate.age_45_54_rate, Unemployment_Rate.age_20plus_rate, Unemployment_Rate.age_25plus_rate, 
                            Unemployment_Rate.age_55plus_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

    session.close()

    # List of all column names
    all_columns = ['date', 'overall_rate', 'age_16_17_rate', 'age_16_19_rate', 'age_18_19_rate', 'age_16_24_rate', 'age_20_24_rate',
                    'age_25_34_rate', 'age_25_54_rate', 'age_35_44_rate', 'age_45_54_rate', 'age_20plus_rate', 'age_25plus_rate', 'age_55plus_rate']
    
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

    ######## Returns overall unemployment rate ########
    if data == 'overall_rate':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.overall_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Overall unemployment rate data for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:

            # Convert the date entry to datetime dtype to access month
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.overall_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 16-17 ########
    elif data == '16_17':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_16_17_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 16-17 for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_16_17_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 16-19 ########
    elif data == '16_19':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_16_19_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 16-19 for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_16_19_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 18-19 ########
    elif data == '18_19':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_18_19_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 18-19 for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_18_19_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 16-24 ########
    elif data == '16_24':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_16_24_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 16-24 for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_16_24_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 20-24 ########
    elif data == '20_24':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_20_24_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 20-24 for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_20_24_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 25-34 ########
    elif data == '25_34':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_25_34_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 25-34 for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_25_34_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 25-54 ########
    elif data == '25_54':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_25_54_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 25-54 for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_25_54_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 35-44 ########
    elif data == '35_44':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_35_44_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 35-44 for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_35_44_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 45-54 ########
    elif data == '45_54':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_45_54_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 45-54 for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_45_54_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 20+ ########
    elif data == '20plus':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_20plus_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 20+ for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_20plus_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 25+ ########
    elif data == '25plus':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_25plus_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 25+ for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_25plus_rate

        return jsonify(unemp_rate)
    
    ######## Returns unemployment rate for 55+ ########
    elif data == '55plus':
        session = Session(engine)
    
        results = session.query(Unemployment_Rate.date, Unemployment_Rate.age_55plus_rate).filter(Unemployment_Rate.date.like(f"{year}%")).all()

        session.close()

        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment rate data for age 55+ for the year {year} by month"}]

        # Loop through the results list to add to unemp_rate to jsonify
        for row in results:
            # Convert the date entry to datetime dtype
            date = pd.to_datetime(row.date)
            
            # Add the current row (which is the month) to the dictionary in unemp_rate
            unemp_rate[0][month_dict[date.month]] = row.age_55plus_rate

        return jsonify(unemp_rate)
    
    else:
        return jsonify("error")
    
########################################################
######                                            ######
######   Route for data depending on year (Men)   ######
######                                            ######
########################################################
@app.route("/api/v1.0/unemployment_rate_s/<year>/<sex>")
def all_data_men(year, sex):
    print(sex)
    if sex == "men":
        session = Session(engine)
    
        results = session.query(Unemployment_Rate_S.date, 
                                Unemployment_Rate_S.men_rate,
                                Unemployment_Rate_S.men_16_17_rate, 
                                Unemployment_Rate_S.men_16_19_rate, 
                                Unemployment_Rate_S.men_18_19_rate, 
                                Unemployment_Rate_S.men_16_24_rate, 
                                Unemployment_Rate_S.men_20_24_rate, 
                                Unemployment_Rate_S.men_25_34_rate, 
                                Unemployment_Rate_S.men_25_54_rate, 
                                Unemployment_Rate_S.men_35_44_rate, 
                                Unemployment_Rate_S.men_45_54_rate, 
                                Unemployment_Rate_S.men_25plus_rate, 
                                Unemployment_Rate_S.men_55plus_rate)\
                                    .filter(Unemployment_Rate_S.date.like(f"{year}%")).all()

        session.close()

        # List of all column names
        all_columns = ['date', 'men_rate', 'men_16_17_rate', 'men_16_19_rate', 'men_18_19_rate', 'men_16_24_rate', 'men_20_24_rate',
                        'men_25_34_rate', 'men_25_54_rate', 'men_35_44_rate', 'men_45_54_rate', 'men_25plus_rate', 'men_55plus_rate']
        
        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment data for the year {year} by month (Male)"}]

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
    
    elif sex == "women":
        session = Session(engine)
    
        results = session.query(Unemployment_Rate_S.date, 
                                Unemployment_Rate_S.women_rate,
                                Unemployment_Rate_S.women_16_17_rate, 
                                Unemployment_Rate_S.women_16_19_rate, 
                                Unemployment_Rate_S.women_18_19_rate, 
                                Unemployment_Rate_S.women_16_24_rate, 
                                Unemployment_Rate_S.women_20_24_rate, 
                                Unemployment_Rate_S.women_25_34_rate, 
                                Unemployment_Rate_S.women_25_54_rate, 
                                Unemployment_Rate_S.women_35_44_rate, 
                                Unemployment_Rate_S.women_45_54_rate,  
                                Unemployment_Rate_S.women_25plus_rate, 
                                Unemployment_Rate_S.women_55plus_rate)\
                                    .filter(Unemployment_Rate_S.date.like(f"{year}%")).all()

        session.close()

        # List of all column names
        all_columns = ['date', 'women_rate', 'women_16_17_rate', 'women_16_19_rate', 'women_18_19_rate', 'women_16_24_rate', 'women_20_24_rate',
                        'women_25_34_rate', 'women_25_54_rate', 'women_35_44_rate', 'women_45_54_rate', 'women_25plus_rate', 'women_55plus_rate']
        
        # Define a list to jsonify unemployment rate
        unemp_rate = [{"title": f"Unemployment data for the year {year} by month (Female)"}]

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
    
    else:
        return jsonify("error")

if __name__ == "__main__":
    app.run(debug=True)