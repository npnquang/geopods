// Making a POST request
function query() {
  fetch('http://localhost:5000/stream', {
    method: 'POST', // Specify the request method
    headers: {
      'Content-Type': 'application/json' // Set the content type to JSON
    },
    body: JSON.stringify({
      uid: Math.floor(Math.random() * 100000),
      timestamp: Date.now()/1000,
      msg_type: 'PROCESS',
      data: {
        x: parseFloat((Math.random() * 180 - 90).toFixed(6)),
        y: parseFloat((Math.random() * 360 - 180).toFixed(6)),
      }
    }) // Convert the data to a JSON string
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Parse the JSON from the response
    })
    .then(data => {
      console.log(data); // Handle the data from the response
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    }
  );
}

setInterval(query, 1000)