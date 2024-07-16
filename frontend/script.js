document.getElementById('queryForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const gpa = document.getElementById('gpa').value;
    const zipCode = document.getElementById('zipCode').value;
    const gender = document.getElementById('gender').value;

    let url = '/api/students?';
    if (gpa) url += `gpa=${gpa}&`;
    if (zipCode) url += `zip_code=${zipCode}&`;
    if (gender) url += `gender=${gender}&`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<h2>Results:</h2>';
            data.forEach(student => {
                resultsDiv.innerHTML += `
                    <p>
                        Name: ${student.name}<br>
                        Gender: ${student.gender}<br>
                        GPA: ${student.gpa.toFixed(2)}<br>
                        Zip Code: ${student.zip_code}
                    </p>
                `;
            });
        })
        .catch(error => console.error('Error:', error));
});