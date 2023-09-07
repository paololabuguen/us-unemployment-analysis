let link = "http://127.0.0.1:5000/api/v1.0/unemployment_rate/"
let yearsUrl = "http://127.0.0.1:5000/api/v1.0/year_data_list"

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

    for (let i=0; i<filterKeys.length; i++){
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
//------------------- Function that graphs the overall unemployment rates ----------------------------------------------
//----------------------------------------------------------------------------------------------------------------------

function overallUnemployment(startDate = "1948", endDate = "2023", filter = "overall_rate") {

    // Define the url string
    let url_string = `${link}y/${startDate}/${endDate}/${filter}`;

    d3.json(url_string).then(data => {

        // Store the Objects into variables to graph later
        let overallData = data[0].overall;
        let menData = data[0].men;
        let womenData = data[0].women;


        // We are using Plotly to graph the data
        // We define 3 traces for overall, men and women unemployment rate
        let trace1 = {
            x: Object.keys(overallData),
            y: Object.values(overallData),
            type: 'bar',
            name: 'Overall Unemployment rate'
        };

        let trace2 = {
            x: Object.keys(menData),
            y: Object.values(menData),
            type: 'bar',
            name: 'Men Overall Unemployment rate'
        };

        let trace3 = {
            x: Object.keys(womenData),
            y: Object.values(womenData),
            type: 'bar',
            name: 'Women Overall Unemployment rate'
        };

        let trace = [trace1, trace2, trace3]

        // Define the layout
        let layout = {
            title: data[0].title,
            yaxis: {
                title: 'Unemployment Rate'
            },
            xaxis: {
                title: 'Year(s)'
            }
        };
        
        // Graph the data
        Plotly.newPlot('bar-graph', trace, layout)
    })
}

//----------------------------------------------------------------------------------------------------------------------
//------------------- Function that graphs all the visualizations ------------------------------------------------------
//----------------------------------------------------------------------------------------------------------------------

function plotOverallUnemployment() {
    startYear = d3.select("#dropdown-list-st-year").property("value");
    endYear = d3.select("#dropdown-list-end-year").property("value");
    filterData = d3.select("#dropdown-list-data").property("value");
    if (startYear > endYear) {
        alert("Error: Start Year must be less than End Year")
    }
    overallUnemployment(startYear, endYear, filterData);
}


d3.json(yearsUrl).then(data => {
    console.log(data)
    // Initialize by filling the dropdown list
    fillDropdown(data[0].year, data[0].data);

    // Initialize the overall unemployment graph
    initStartYear = d3.select("#dropdown-list-st-year").property("value");
    initEndYear = d3.select("#dropdown-list-end-year").property("value");
    initData = d3.select("#dropdown-list-data").property("value");


    overallUnemployment(initStartYear, initEndYear, initData);

    // Change the graphs depending on the selected items in the dropdown list
    d3.selectAll("#dropdown-list-st-year").on("change", plotOverallUnemployment);
    d3.selectAll("#dropdown-list-end-year").on("change", plotOverallUnemployment);
    d3.selectAll("#dropdown-list-data").on("change", plotOverallUnemployment);
})





