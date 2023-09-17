
let link = "http://127.0.0.1:5000/api/v1.0/unemployment_rate/"
let yearsUrl = "http://127.0.0.1:5000/api/v1.0/year_data_list"

// Initial parameters for graphing functions
initParams = ["2000", "2023", "overall_rate"]


// optionChanged function that just returns that value
function optionChanged(value) {
    return value
};

//----------------------------------------------------------------------------------------------------------------------
//------------------- Function to fill the dropdown list ---------------------------------------------------------------
//----------------------------------------------------------------------------------------------------------------------

function fillDropdown(years, filter) {

    // Strings to add to html code for the start
    let optionsStart = "";
    let optionsEnd = "";
    let optionsData = ""

    // Store the keys and values in filter to variables
    let filterKeys = Object.keys(filter)
    let filterVals = Object.values(filter)

    // Add options to the dropdown list
    years.map((op) => {
        if (op === "2000") {

            // Want 2000 to be the initial selected value for the start year dropdown list
            optionsStart += `<option value="${op}" selected>${op}</option>`
        }
        else {

            // Else, add the option normally
            optionsStart += `<option value="${op}">${op}</option>`
        }
    });

    years.map((op) => {
        if (op === "2023") {

            // Want 2023 to be the initial selected value for the end year dropdown list
            optionsEnd += `<option value="${op}" selected>${op}</option>`
        }
        else {

            // Else, add the option normally
            optionsEnd += `<option value="${op}">${op}</option>`
        }
    });

    for (let i = 0; i < filterKeys.length; i++) {
        if (filterVals[i] === "Overall Rate") {

            // Want Overall Rate to be the initial selected value for the data dropdown list
            optionsData += `<option value="${filterKeys[i]}" selected>${filterVals[i]}</option>`
        }
        else {

            // Else, add the option normally
            optionsData += `<option value="${filterKeys[i]}">${filterVals[i]}</option>`
        }

    }

    // Add the lists to their respective dropdown list
    document.getElementById("dropdown-list-st-year").innerHTML = optionsStart;
    document.getElementById("dropdown-list-end-year").innerHTML = optionsEnd;
    document.getElementById("dropdown-list-data").innerHTML = optionsData;
};

//----------------------------------------------------------------------------------------------------------------------
//------------------- Function that graphs the overall unemployment rates (Plotly) -------------------------------------
//----------------------------------------------------------------------------------------------------------------------

// Originally, the bar graph was made with Plotly then transferred over the Chart.js
// function overallUnemployment(startDate = initParams[0], endDate = initParams[1], filter = initParams[2]) {

//     // Define the url string
//     let urlString = `${link}y/${startDate}/${endDate}/${filter}`;

//     d3.json(urlString).then(data => {

//         // Store the Objects into variables to graph later
//         let overallData = data[0].overall;
//         let menData = data[0].men;
//         let womenData = data[0].women;


//         // We are using Plotly to graph the data
//         // We define 3 traces for overall, men and women unemployment rate
//         let trace1 = {
//             x: Object.keys(overallData),
//             y: Object.values(overallData),
//             type: 'bar',
//             name: 'Overall Unemployment rate'
//         };

//         let trace2 = {
//             x: Object.keys(menData),
//             y: Object.values(menData),
//             type: 'bar',
//             name: 'Men Overall Unemployment rate'
//         };

//         let trace3 = {
//             x: Object.keys(womenData),
//             y: Object.values(womenData),
//             type: 'bar',
//             name: 'Women Overall Unemployment rate'
//         };

//         let trace = [trace1, trace2, trace3]

//         // Define the layout
//         let layout = {
//             title: data[0].title,
//             yaxis: {
//                 title: 'Unemployment Rate'
//             },
//             xaxis: {
//                 title: 'Year(s)'
//             }
//         };

//         // Graph the data
//         Plotly.newPlot('graph-2', trace, layout)
//     })
// }

//----------------------------------------------------------------------------------------------------------------------
//------------------- Function that graphs overall unemployment rate (Chart.js) ----------------------------------------
//----------------------------------------------------------------------------------------------------------------------

function overallUnemploymentChart(startDate = initParams[0], endDate = initParams[1], filter = initParams[2], oldChart) {

    // Get the bar-chart element from the html
    const ctx = document.getElementById('bar-chart');

    // Define the url for the data
    let urlString = `${link}y/${startDate}/${endDate}/${filter}`;

    // Font sizes for title and x and y labels
    let xyFontSize = 15
    let titleFontSize = 25

    // Deletes the oldChart if the parameter was passed
    // This would make it so that the newly created charts dont stack on each other
    if (oldChart !== undefined) {
        oldChart.destroy();
    }

    // Set up a new Chart.js bar graph
    barChart = new Chart(ctx, {
        type: 'bar',
        data: {},
        options: {
            // Want the graph to stay inside the container
            responsive: true,
            maintainAspectRatio: false,

            plugins: {

                // Configurations for the title
                title: {
                    color: 'black',
                    font: {
                        size: titleFontSize
                    },
                    display: true,
                    text: ''
                },

                legend: {
                    labels: {
                        color: 'black'
                    }
                }
            },

            scales: {

                // Configurations for y axis
                y: {
                    title: {
                        color: 'black',
                        font: {
                            size: xyFontSize
                        },
                        display: true,
                        text: 'Unemployment Rate (%)'
                    },
                    beginAtZero: true,

                    ticks: {
                        color: 'black'
                    }
                },

                // Configurations for x axis
                x: {

                    // Labels
                    title: {
                        color: 'black',
                        font: {
                            size: xyFontSize
                        },
                        display: true,
                        text: 'Year(s)'
                    },
                    // We do not want to display the x gridlines
                    grid: {
                        display: false
                    },

                    ticks: {
                        color: 'black'
                    }
                }
            },
        }
    });

    // Here, we access the data from the url then fill in the data we need for the bar graph
    d3.json(urlString).then(data => {

        // Store the Objects into variables to graph later
        let overallData = data[0].overall;
        let menData = data[0].men;
        let womenData = data[0].women;
        let title = data[0].title;

        dataGraph = {

            // Keys are just the years so we use the keys from ovarallData
            labels: Object.keys(overallData),
            datasets: [{

                // Overall data
                label: 'Overall Unemployment rate',
                data: Object.values(overallData),
                borderWidth: 1,
                borderColor: '#077557',
                backgroundColor: '#077557'
            },
            {
                // Men data
                label: 'Men Unemployment rate',
                data: Object.values(menData),
                borderWidth: 1,
                borderColor: '#0369ad',
                backgroundColor: '#0369ad'
            },
            {
                // Women data
                label: 'Women Unemployment rate',
                data: Object.values(womenData),
                borderWidth: 1,
                borderColor: '#fa3754',
                backgroundColor: '#fa3754'
            }
            ]
        }

        // Update the bar graph with the initial data
        barChart.options.plugins.title.text = title;
        barChart.data = dataGraph;
        barChart.update();

    })

    // Return the newly created chart
    // This is so that we can delete this chart when we call the function again to graph a new chart 
    return barChart
}

//----------------------------------------------------------------------------------------------------------------------
//------------------- Function that lists top 10 months with the highest unemployment rate -----------------------------
//----------------------------------------------------------------------------------------------------------------------

function top10UnemploymentRate(startDate = initParams[0], endDate = initParams[1], filter = initParams[2]) {
    // Define the url link for the top10 data
    let urlString = `${link}top10/${startDate}/${endDate}/${filter}`;


    d3.json(urlString).then(data => {
        
        // List of top 10 months for the years and data chosen for overall, men and women
        let top10OverallDates = Object.keys(data[0].overall);
        let top10OverallRates = Object.values(data[0].overall);

        let top10MenDates = Object.keys(data[0].men);
        let top10MenRates = Object.values(data[0].men);

        let top10WomenDates = Object.keys(data[0].women);
        let top10WomenRates = Object.values(data[0].women);

        // These are to add to the html code on the right side of the screen
        // This would show the list of top 10 overall, men and women unemployment rates
        // The list header has class top-10-overall-header
        let dataListOverall = "<p class=\"top-10-overall-header\">Overall: </p>";
        let dataListMen = "<p class=\"top-10-overall-header\">Men: </p>";
        let dataListWomen = "<p class=\"top-10-overall-header\">Women: </p>";

        for (let i=0; i < top10OverallDates.length; i++) {
            dataListOverall += `<p class=\"top-10-list-element\">${top10OverallDates[i]}: ${top10OverallRates[i]}%</p>`;
        };
        objList=  dataListOverall;
        document.getElementById("top-10-left").innerHTML = objList;

        for (let i=0; i < top10OverallDates.length; i++) {
            dataListMen += `<p class=\"top-10-list-element\">${top10MenDates[i]}: ${top10MenRates[i]}%</p>`;
        };
        objList =  dataListMen;
        document.getElementById("top-10-right").innerHTML = objList;

        for (let i=0; i < top10OverallDates.length; i++) {
            dataListWomen += `<p class=\"top-10-list-element\">${top10WomenDates[i]}: ${top10WomenRates[i]}%</p>`;
        };
        objList =  dataListWomen;
        document.getElementById("top-10-right").innerHTML += objList;
    })
}

//----------------------------------------------------------------------------------------------------------------------
//------------------- Function that graphs all the visualizations ------------------------------------------------------
//----------------------------------------------------------------------------------------------------------------------

function plotOverallUnemployment() {

    // Collect the values selected from the dropdowns
    startYear = d3.select("#dropdown-list-st-year").property("value");
    endYear = d3.select("#dropdown-list-end-year").property("value");
    filterData = d3.select("#dropdown-list-data").property("value");

    // Error in case the selected end year is less than the selected start year
    if (startYear > endYear) {
        alert("Error: Start Year must be less than End Year");
    }

    // Update the graphs
    // overallUnemployment(startYear, endYear, filterData);
    overallUnemploymentChart(startYear, endYear, filterData, barChart);
    top10UnemploymentRate(startYear, endYear, filterData);
}


d3.json(yearsUrl).then(data => {
    // Initialize by filling the dropdown list
    fillDropdown(data[0].year, data[0].data);

    // Initialize the overall unemployment graph
    initStartYear = d3.select("#dropdown-list-st-year").property("value");
    initEndYear = d3.select("#dropdown-list-end-year").property("value");
    initData = d3.select("#dropdown-list-data").property("value");


    // // Initial plot for the bar graph

    // overallUnemployment(initStartYear, initEndYear, initData);
    barChart = overallUnemploymentChart(initStartYear, initEndYear, initData);
    top10UnemploymentRate(initStartYear, initEndYear, initData);

    // Change the graphs depending on the selected items in the dropdown list
    d3.selectAll("#dropdown-list-st-year").on("change", plotOverallUnemployment);
    d3.selectAll("#dropdown-list-end-year").on("change", plotOverallUnemployment);
    d3.selectAll("#dropdown-list-data").on("change", plotOverallUnemployment);
})
