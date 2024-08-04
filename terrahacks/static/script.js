document.getElementById('search-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get the value from the input field
    const inputData = document.getElementById('search-input').value;

    try {
        // Send POST request to the server
        const response = await fetch('/process-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input: inputData })
        });

        // Check if the response is ok (status in the range 200-299)
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // Parse the JSON response
        const result = await response.json();

        // Log the processed data
        console.log(result.message);

        //window.location.href = 'terrahacks/templates/pages/query.html'; // Adjust the path as needed

        // Optionally update the HTML with the result
        // document.getElementById('result').innerText = result.message;
    } catch (error) {
        // Log any errors
        console.error('There has been a problem with your fetch operation:', error);
    }
});
