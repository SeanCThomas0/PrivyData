document.getElementById('queryForm').addEventListener('submit', function(e) {
    e.preventDefault();
    fetchData('/api/students?' + new URLSearchParams(new FormData(e.target)));
});

document.getElementById('statForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const params = new URLSearchParams(formData);
    fetchData('/api/students/stat?' + params.toString());
    fetchData('/api/students/stats?' + params.toString());
});

function fetchData(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (url.includes('/stat')) {
                displayStats(data, false);
            } else if (url.includes('/stats')) {
                displayStats(data, true);
            } else {
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '<h2>Query Results:</h2>';
                if (Array.isArray(data)) {
                    displayTable(data);
                } else {
                    displayObject(data);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML += '<p>An error occurred while fetching the data. Please check the console for more details.</p>';
        });
}

function displayTable(data) {
    if (data.length === 0) {
        document.getElementById('results').innerHTML += '<p>No results found.</p>';
        return;
    }

    const table = document.createElement('table');
    table.className = 'table table-striped';
    
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    Object.keys(data[0]).forEach(key => {
        const th = document.createElement('th');
        th.textContent = key;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    data.forEach(item => {
        const row = document.createElement('tr');
        Object.values(item).forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    document.getElementById('results').appendChild(table);
}

function displayObject(data) {
    const ul = document.createElement('ul');
    ul.className = 'list-group';
    for (const [key, value] of Object.entries(data)) {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = `${key}: ${value}`;
        ul.appendChild(li);
    }
    document.getElementById('results').appendChild(ul);
}

function displayStats(data, isDP) {
    const resultsDiv = document.getElementById('results');
    const title = isDP ? 'Differentially Private Statistics:' : 'Normal Statistics:';
    
    if (!resultsDiv.innerHTML.includes('Statistics Results:')) {
        resultsDiv.innerHTML = '<h2>Statistics Results:</h2>';
    }
    
    const statDiv = document.createElement('div');
    statDiv.innerHTML = `<h3>${title}</h3>`;
    
    if (data.count === 0) {
        statDiv.innerHTML += '<p>No results found for the given criteria.</p>';
    } else {
        const ul = document.createElement('ul');
        ul.className = 'list-group';
        for (const [key, value] of Object.entries(data)) {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = `${key}: ${value === null ? 'N/A' : (typeof value === 'number' ? value.toFixed(2) : value)}`;
            ul.appendChild(li);
        }
        statDiv.appendChild(ul);
    }
    
    resultsDiv.appendChild(statDiv);
}

function toggleDarkMode() {
    var body = document.body;
    var resultsContainer = document.getElementById('results');
    var button = document.getElementById("darkModeToggle");
    
    body.classList.toggle("dark-mode");
    if (resultsContainer) {
        resultsContainer.classList.toggle("dark-mode");
    }
    
    button.textContent = body.classList.contains("dark-mode") ? "Toggle Light Mode" : "Toggle Dark Mode";
}
