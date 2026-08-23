const playersDiv = document.getElementById("players");
const taskDiv = document.getElementById("task");

let lastStatus = null;

function interpretGame(game_state) {

    playersDiv.innerHTML = "";

    if (!game_state.players) return;

    game_state.players.forEach(player => {

        const div = document.createElement("div");

        div.className = "player";

        div.innerHTML = `
            <div class="avatar">${player.avatar}</div>
            <div class="name">${player.name}</div>
        `;

        playersDiv.appendChild(div);
    });

    taskDiv.textContent = game_state.task || "";
}

async function interpretState() {

    const clientId = localStorage.getItem("client_id");

    const res = await fetch(
        `/get_status?client_id=${clientId}`
    );

    if (res.status === 401) {
        window.location.href = "/";
        return;
    }

    const status = await res.json();

    if (
        lastStatus &&
        JSON.stringify(lastStatus) === JSON.stringify(status)
    ) {
        return;
    }

    lastStatus = status;

    if (status.lvl !== window.location.pathname) {
        window.location.href = status.lvl;
        return;
    }

    interpretGame(status.game_state);
}

setInterval(interpretState, 2000);
interpretState();