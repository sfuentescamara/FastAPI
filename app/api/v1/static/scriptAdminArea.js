function renderData(data, container) {
    Object.entries(data).forEach(([key, value]) => {
        const dataItem = document.createElement('div');
        dataItem.classList.add('data-item');

        const dataKey = document.createElement('div');
        dataKey.classList.add('data-key');
        dataKey.textContent = key;

        const dataValue = document.createElement('div');
        dataValue.classList.add('data-value');

        if (typeof value === 'object' && value !== null) {
            if (Array.isArray(value)) {
                // Handle arrays
                value.forEach((item, index) => {
                    renderData({ [`${key} [${index}]`]: item }, container);
                });
            } else {
                // Handle nested objects
                renderData(value, container);
            }
        } else {
            // Display simple values (strings, numbers, etc.)
            dataValue.textContent = value;
            dataItem.appendChild(dataKey);
            dataItem.appendChild(dataValue);
            container.appendChild(dataItem);
        }
    });
}

async function fetchDataAndRender() {
        await fetch('/api/v1/room_info', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        }).then((response) => {
            if (response.status === 200) {
                console.log("Status OK");
                return response.json();
            } else {
                console.log("Error");
            }
        }).then(data => {
            try {
                console.log(data);
                const dataContent = document.getElementById('dataContent');
                dataContent.innerHTML = '';
                for (const [key, value] of Object.entries(data.data)) {
                    const dataRoom = document.createElement('div');
                    dataRoom.classList.add('data-room');
                    renderData(value, dataRoom);
                    dataContent.appendChild(dataRoom);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }).catch(error => console.error('Error:', error));
}