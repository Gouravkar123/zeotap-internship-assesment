document.addEventListener('DOMContentLoaded', function() {
    // Handle cell updates
    document.querySelectorAll('.cell').forEach(cell => {
        cell.addEventListener('blur', function() {
            const cellId = this.getAttribute('data-cell');
            const value = this.innerText;

            // Basic validation: Check if the value is numeric
            if (isNaN(value) && value !== '') {
                alert('Please enter a valid number.');
                this.innerText = ''; // Clear the cell if invalid
                return;
            }

            fetch('/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ cell: cellId, value: value })
            });
        });
    });

    // Handle formula bar input
    document.getElementById('formula-bar').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const formula = this.value;
            const functionMatch = formula.match(/(\w+)\(([^)]+)\)/);
            if (functionMatch) {
                const functionName = functionMatch[1];
                const range = functionMatch[2].split(',').map(cell => cell.trim());
                fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ function: functionName, range: range })
                })
                .then(response => response.json())
                .then(data => {
                    alert(`Result: ${data.result}`);
                });
            }
            this.value = ''; // Clear the formula bar after execution
        }
    });

    // Handle data quality functions
    document.getElementById('data-quality-button').addEventListener('click', function() {
        const functionName = document.getElementById('data-quality-function').value;
        const range = document.getElementById('data-quality-range').value.split(',').map(cell => cell.trim());
        const findText = document.getElementById('find-text').value;
        const replaceText = document.getElementById('replace-text').value;

        const requestData = { function: functionName, range: range };
        if (functionName === 'FIND_AND_REPLACE') {
            requestData.find = findText;
            requestData.replace = replaceText;
        }

        fetch('/data_quality', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            alert(`Data Quality Result: ${data.result.join(', ')}`);
        });
    });

    // Drag functionality for cell selection
    let isDragging = false;
    let startCell;

    document.querySelectorAll('.cell').forEach(cell => {
        cell.addEventListener('mousedown', function() {
            isDragging = true;
            startCell = this;
            this.classList.add('selected');
        });

        cell.addEventListener('mouseover', function() {
            if (isDragging) {
                this.classList.add('selected');
            }
        });

        cell.addEventListener('mouseup', function() {
            isDragging = false;
        });
    });

    document.addEventListener('mouseup', function() {
        isDragging = false;
    });
});