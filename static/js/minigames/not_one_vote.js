const playersList = document.getElementById("playersList");

let hasVoted = false;

let lastStatus = null;

// ---------- SEND ----------

async function sendVote(targetId) {
    const clientId = localStorage.getItem("client_id");

    await fetch("/set_info", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_id: clientId,
            game_info: {
                vote: targetId
            }
        })
    });

    hasVoted = true;
    lastStatus = null;
}

// ---------- RENDER ----------

function renderPlayers(players, game_state) {
    playersList.innerHTML = "";

    const votes = game_state.votes || {};

    players.forEach(p => {
        const div = document.createElement("div");
        div.className = "player";

        div.innerHTML = `
            <img src="/static/avatars/${p.avatar}">
            <div class="player-name">${p.name}</div>
        `;

        // 🔥 klik tylko jeśli jeszcze nie głosował
        if (!hasVoted) {
            div.onclick = () => sendVote(p.id);
        } else {
            div.style.opacity = "0.5";
            div.style.cursor = "default";
        }

        // 🔥 pokaż wyniki jeśli są
        if (Object.keys(votes).length > 0) {
            const v = votes[p.id] || 0;

            const voteInfo = document.createElement("div");
            voteInfo.style.marginTop = "5px";
            voteInfo.style.fontSize = "12px";

            voteInfo.textContent = `Głosy: ${v}`;

            // 🔥 highlight kto pije
            if (v === 1) {
                div.style.border = "3px solid red";
            }

            div.appendChild(voteInfo);
        }

        playersList.appendChild(div);
    });
}

// ---------- MAIN ----------

function interprateGame(game_state) {
    const players = window.lastPlayers || [];

    renderPlayers(players, game_state);
}

// ---------- LOOP ----------

async function interprateState() {
    const clientId = localStorage.getItem("client_id");

    const res = await fetch(`/get_status?client_id=${clientId}`);
    const status = await res.json();

    if (lastStatus &&
        JSON.stringify(lastStatus) === JSON.stringify(status)) {
        return; // nic się nie zmieniło → nie renderujemy
    }
    lastStatus = status

    window.lastPlayers = status.players;

    if (status.lvl !== window.location.pathname) {
        window.location.href = status.lvl;
        return;
    }

    interprateGame(status.game_state);
}

setInterval(interprateState, 2000);
interprateState();
