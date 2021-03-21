// from data.js
var tableData = data;


// Identify the table and tbody
var tbody = d3.select('#ufo-tbody');

// test

//d3.json("/api/recipemetadata").then((recipes) => {
   //console.log(recipes)
//});

d3.json("/api/recipemetadata", function(recipes){
    console.log(recipes)
});

// Create function to generate and populate the table
function buildTable(tableData){

    // Dynamically build table
    tableData.forEach(record => {
        var row = tbody.append('tr');

////logic: if checked -- identify the status as checked and if not set status to unchecked; add a status true or flase to records pulled from API

            row.append('td').append('input').attr("type", "checkbox");    
            row.append('td').text(record['recipe_id']);
            row.append('td').text(record['recipe_title']);
            row.append('td').text(record['cooking_minutes']);
            row.append('td').text(record['health_score'])    
            row.append('td').text(record['source_url']);
            row.append('td').text(record['likes']);
            row.append('td').text(record['carbohydrates_serving']);
            row.append('td').text(record['servings']);
            row.append('td').text(record['calories_serving']);

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
    var query = d3.select('#query').property('value');
    var cusine = d3.select('#cusine').property('value');
    var type_of_recipe = d3.select('#type_of_recipe').property('value');
    var calories = d3.select('#calories').property('value');
    var cookingMinutes = d3.select('#cookingMinutes').property('value');

    // Build an object of fields to run through 
    var filterFields = {
        'query': query,
        'cuisine': cusine,
        'type_of_recipe': type_of_recipe, 
        'calories': calories,
        'cookingMinutes': cookingMinutes
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
queryfield = d3.select('#query')

// Add event listeners to the web elements
btn.on('click', filterTable);
queryfield.on('change', filterTable);

// Attach an event listener to the fields attached to the .filter class 
d3.selectAll('.filter').on('change', filterTable);

// Call the function to initially load the table
buildTable(tableData);