
function showTab(tabIndex) {
    var contents = document.getElementsByClassName('content');
    for (var i = 0; i < contents.length; i++) {
        contents[i].style.display = 'none';
    }
    document.getElementById('content' + tabIndex).style.display = 'block';
}

function darkMode() {
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme === 'dark') {
        document.body.className = 'light-mode';
    } else {
        document.body.className = 'dark-mode';
    }
    const theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);

};

function renderView(page) {
    window.location.href = page;
};

async function createRoom() {
    let nick = document.getElementById("input_nick").value;
    let ws = window.ws;
    let ts_client = String(ws.ts_client);
    let client = { 
        'ts_client': ts_client,
        'id_client': 0,
        'name': nick,
        'ws': ""
    };
    await fetch('/api/v1/newRoom', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            client
        ),
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
            let room = {
                'id_room': data.id_room,
                'users': [],
                'opt': data.opt
            };
            fetch('/api/v1/room/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            body: JSON.stringify(room)
        })
            .then(response => {
                if (response.ok) {
                    document.user = data.client;
                    document.room = data.id_room;
                    return response.text();
                } else {
                    throw new Error('Error en la solicitud');
                }
            })
            .then(html => {
                document.open();
                document.write(html);
                document.close();
            })
            .catch(error => console.error('Error:', error));

        } catch (error) {
            console.log(error);
        }
    }).catch(error => console.error('Error:', error));
}

async function joinToRoom() {
    let idRoom = prompt('Insert ID room');
    let nick = document.getElementById("input_nick").value;
    let ws = window.ws;
    let ts_client = String(ws.ts_client);
    let client = { 
        'ts_client': ts_client,
        'id_client': 0,
        'name': nick,
        'ws': ""
    };
    await fetch('/api/v1/joinRoom', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'data': {
                id_room: idRoom,
                users: [client],
                opt: ""
            },
            'client': client
        }),
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
            let room = {
                'id_room': data.id_room,
                'users': [],
                'opt': data.opt
            };
            fetch('/api/v1/room/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            body: JSON.stringify(room)
            })
            .then(response => {
                if (response.ok) {
                    document.user = data.client;
                    document.room = data.id_room;
                    return response.text();
                } else {
                    throw new Error('Error en la solicitud');
                }
            })
            .then(html => {
                document.open();
                document.write(html);
                document.close();
            })
            .catch(error => console.error('Error:', error));

        } catch (error) {
            console.log(error);
        }
    }).catch(error => console.error('Error:', error));
}

export {showTab, darkMode, createRoom, joinToRoom};
