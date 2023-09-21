# U.S. Unemployment Analysis

## Summary
The goal of this project was to create a dynamic HTML dashboard to analyze the unemployment rates in the U.S. from years 1948 to 2023. The visualizations 
included are a bar graph that shows the average unemployment rate per year based on  the selected start year, end year and filter (These are either the overall rate or an age range).
I also included a line graph showing the change of unemployment rate per year compared to the previous year. I also have a list of top months with the highest unemployment rate depending on the starting, ending and
filter (age range). The line graph and bar graph are plotted using Chart.js

## How to Use
In order to run the project, you would need an internet browser (I use Chrome), Python (I have version 3.10.13 installed) and Allow CORS browser extension (https://mybrowseraddon.com/access-control-allow-origin.html) 
1. Clone the repo into your computer.
2. Run app.py (This initializes the Flask app to access the API for the data. What I do is open a terminal in the us-unemployment-analysis directory and run the python file)
3. Run index.html and make sure the Allow CORS extension is toggled on.

After this, everything else should be self explanatory. There would be three dropdowns at the top of the page and you can choose the start year, end year and the age range and the graphs change based on your options.

## Dataset

The dataset I used can be found here:
https://www.kaggle.com/datasets/guillemservera/us-unemployment-rates?select=df_unemployment_rates.csv

## Credits
As this is my first solo project, there was a lot of information I had to learn making it. Credits to developers of Chart.js, contributors of stackoverflow as I had to lookup solutions on how to make Chart.js work and how CSS and HTML work together.
Also, I took some code from the UofT data bootcamp lectures when I was taking them to help create app.py.
