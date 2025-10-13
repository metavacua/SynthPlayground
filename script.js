// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    // Get references to the HTML elements
    const formulaInput = document.getElementById('formula-input');
    const refuteButton = document.getElementById('refute-button');
    const resultOutput = document.getElementById('result-output');
    // Separate status message area for refutation results
    const refutationStatusMessage = document.getElementById('refutation-status-message');

    // Get references to the new server control buttons
    const stopServerButton = document.getElementById('stop-server-button');
    const restartServerButton = document.getElementById('restart-server-button');
    // Separate status message area for server control actions
    const serverStatusMessage = document.getElementById('server-status-message');


    // Define the back-end API endpoint URLs
    const REFUTE_API_ENDPOINT = '/refute';
    const STOP_SERVER_API_ENDPOINT = '/stop-server'; // Endpoint for stopping the server
    const RESTART_SERVER_API_ENDPOINT = '/restart-server'; // Endpoint for restarting the server


    // --- Refutation Button Logic ---
    // Add an event listener to the refute button
    refuteButton.addEventListener('click', async () => {
        const formulaString = formulaInput.value.trim();

        if (formulaString === '') {
            // Use the correct variable name refutationStatusMessage
            refutationStatusMessage.textContent = 'Please enter a formula.';
            resultOutput.value = ''; // Clear previous result
            return; // Exit the function
        }

        // Use the correct variable name refutationStatusMessage
        refutationStatusMessage.textContent = 'Processing...';
        resultOutput.value = '';

        try {
            // Send a POST request to the refutation API endpoint
            const response = await fetch(REFUTE_API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Indicate that the body is JSON
                },
                // Send the formula string in a JSON object
                body: JSON.stringify({ formula: formulaString }),
            });

            // Check if the HTTP response was not OK (status code outside 200-299)
            if (!response.ok) {
                const errorText = await response.text(); // Get the error message from the response body
                // Throw an error with status and message
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            // Parse the JSON response from the back-end
            const result = await response.json();

            // Process the result based on the 'status' field
            if (result && result.status === 'success') {
                 // If refutation was successful
                 if (result.refuted) {
                     resultOutput.value = result.refuted_formula; // Display the refuted formula
                     refutationStatusMessage.textContent = 'Formula refuted.'; // Update status
                 } else {
                     // If formula was not refuted
                     resultOutput.value = result.non_refuted_state; // Display the non-refuted state
                     refutationStatusMessage.textContent = 'Formula not refuted.'; // Update status
                 }
            } else if (result && result.status === 'error') {
                 // If the back-end returned an error status
                 resultOutput.value = `Error: ${result.message}`; // Display the error message from the back-end
                 refutationStatusMessage.textContent = 'An error occurred during processing.'; // Update status
             }
            else {
                 // Handle unexpected response formats
                 resultOutput.value = 'Error: Unexpected response format from back-end.';
                 refutationStatusMessage.textContent = 'An unexpected error occurred.';
            }


        } catch (error) {
            // Catch any errors during the fetch or processing
            console.error('Error sending formula to back-end:', error); // Log error to console
            refutationStatusMessage.textContent = `Error: ${error.message}`; // Display error message to user
            resultOutput.value = 'Could not connect to the refuter back-end or an error occurred.'; // Generic error message
        }
    });

    // --- Server Control Button Logic ---

    // Generic asynchronous function to send a server control request
    async function sendServerControlRequest(endpoint, actionName) {
        // Use the correct variable name serverStatusMessage
        serverStatusMessage.textContent = `${actionName} requested...`;
        try {
            // Send a POST request to the specified server control endpoint
            const response = await fetch(endpoint, {
                method: 'POST', // Using POST is common for actions that change state
                headers: {
                    'Content-Type': 'application/json', // Indicate JSON content type
                },
                body: JSON.stringify({}), // Sending an empty JSON object as the body
            });

            // Check if the HTTP response was not OK
            if (!response.ok) {
                 const errorText = await response.text();
                 throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            // Parse the JSON response from the back-end
            const result = await response.json();

            // Process the result based on the 'status' field
            if (result && result.status === 'success') {
                // If the back-end reported success
                serverStatusMessage.textContent = `${actionName} successful: ${result.message}`;
            } else if (result && result.status === 'error') {
                // If the back-end reported an error
                serverStatusMessage.textContent = `${actionName} failed: ${result.message}`;
            } else {
                 // Handle unexpected response format
                 serverStatusMessage.textContent = `${actionName} failed: Unexpected response format.`;
            }

        } catch (error) {
            // Catch any errors during the fetch or processing
            console.error(`Error during ${actionName}:`, error); // Log error to console
            serverStatusMessage.textContent = `Error during ${actionName}: ${error.message}`; // Display error message to user
        }
    }

    // Add event listener for the Stop button
    stopServerButton.addEventListener('click', () => {
        // Call the generic request function with the stop endpoint and action name
        sendServerControlRequest(STOP_SERVER_API_ENDPOINT, 'Server Stop');
    });

    // Add event listener for the Restart button
    restartServerButton.addEventListener('click', () => {
        // Call the generic request function with the restart endpoint and action name
        sendServerControlRequest(RESTART_SERVER_API_ENDPOINT, 'Server Restart');
    });

});

