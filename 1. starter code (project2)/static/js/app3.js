// from data.js
var tableData = data;


// Identify the table and tbody
var tbody = d3.select('#ufo-tbody');

// Create function to generate and populate the table
function buildTable(tableData){

    // Dynamically build table
    tableData.forEach(record => {
        var row = tbody.append('tr');

////logic: if checked -- identify the status as checked and if not set status to unchecked; add a status true or flase to records pulled from API

            row.append('td').append('input').attr("type", "checkbox");    
            row.append('td').text(record['datetime']);
            row.append('td').text(record['city']);
            row.append('td').text(record['state']);
            row.append('td').text(record['country'])    
            row.append('td').text(record['shape']);
            row.append('td').text(record['durationMinutes']);
            row.append('td').text(record['comments']);

        /* // Use Object.values as an alternate method
            Object.values(record).forEach(col => {
                row.append('td').text(col);        
            });
        */
    })
}

/// This would updated checked data (as checked/unchecked) to table when a second search is initiated, as well as, store in variable, 
///when clicking next page

function addcheckeddata(){
   
    var checkeddata = [];


}


function filterTable(){
    // Create a copy of tableData specifically for filtering
   
    var filteredData = tableData;

    // capture value for all search fields */
    var datetime = d3.select('#datetime').property('value');
    var city = d3.select('#city').property('value');
    var state = d3.select('#state').property('value');
    var country = d3.select('#country').property('value');
    var shape = d3.select('#shape').property('value');

    // Build an object of fields to run through 
    var filterFields = {
        'datetime': datetime,
        'city': city,
        'state': state, 
        'country': country,
        'shape': shape
    }

    // Remove empty keys from the list of filters to search
    Object.entries(filterFields).forEach(([key, val]) => {
        
        // Use !val to check for empty strings or nulls
        if(!val) { 
            delete filterFields[key];
        }
    });

    // Loop through each of the filter keys and return records from filteredData that match 
    Object.entries(filterFields).forEach(([key, value]) => {
        // Continue to refine the filteredData array 
        filteredData = filteredData.filter(row => row[key] == value);
      });    

    // Clear out the tbody
    tbody.html('');

////  then add checked rows back in

    // Rebuild the filtered table using the buildTable function 
    buildTable(filteredData);    
}

// Identify web elements on the page
btn = d3.select('#filter-btn');
datetimefield = d3.select('#datetime')

// Add event listeners to the web elements
btn.on('click', filterTable);
datetimefield.on('change', filterTable);

// Attach an event listener to the fields attached to the .filter class 
d3.selectAll('.filter').on('change', filterTable);

// Call the function to initially load the table
buildTable(tableData);