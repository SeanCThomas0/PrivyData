document.getElementById('queryForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const params = new URLSearchParams();

    for (const [key, value] of formData.entries()) {
        if (value) {
            params.append(key, value);
        }
    }

    fetch(`/api/students?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<h2>Results:</h2>';
            if (data.length === 0) {
                resultsDiv.innerHTML += '<p>No results found.</p>';
            } else {
                const table = document.createElement('table');
                table.className = 'table table-striped';
                
                // Create table header
                const thead = document.createElement('thead');
                const headerRow = document.createElement('tr');
                Object.keys(data[0]).forEach(key => {
                    const th = document.createElement('th');
                    th.textContent = key;
                    headerRow.appendChild(th);
                });
                thead.appendChild(headerRow);
                table.appendChild(thead);

                // Create table body
                const tbody = document.createElement('tbody');
                data.forEach(student => {
                    const row = document.createElement('tr');
                    Object.values(student).forEach(value => {
                        const td = document.createElement('td');
                        td.textContent = value;
                        row.appendChild(td);
                    });
                    tbody.appendChild(row);
                });
                table.appendChild(tbody);

                resultsDiv.appendChild(table);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<p>An error occurred while fetching the data.</p>';
        });
});