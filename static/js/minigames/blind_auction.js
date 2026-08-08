const taskDiv = document.getElementById("task");

const bidSection = document.getElementById("bidSection");
const bidInput = document.getElementById("bidInput");
const sendBidBtn = document.getElementById("sendBidBtn");

const statusInfo = document.getElementById("statusInfo");
const resultsDiv = document.getElementById("results");

let hasBid = false;

let lastStatus = null;

// ---------- SEND ----------

async function sendBid(value) {
    const clientId = localStorage.getItem("client_id");

    await fetch("/set_info", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_id: clientId,
            game_info: {
                bid: value
            }
        })
    });

    hasBid = true;
}

// ---------- BUTTON ----------

sendBidBtn.onclick = () => {
    const val = parseInt(bidInput.value);
    if (isNaN(val)) return;

    sendBid(val);
};

// ---------- MAIN ----------

function interprateGame(game_state) {
    const clientId = localStorage.getItem("client_id");
    const players = window.lastPlayers || [];

    // pokaż zadanie
    taskDiv.innerHTML = game_state.task || "";

    const bids = game_state.bids || {};
    const bidsCount = Object.keys(bids).length;

    // ---------- FAZA LICYTACJI ----------
    if (bidsCount < players.length) {
        resultsDiv.innerHTML = "";

        if (!hasBid) {
            bidSection.style.display = "block";
            statusInfo.textContent = `Oddano głosów: ${bidsCount}/${players.length}`;
        } else {
            bidSection.style.display = "none";
            statusInfo.textContent = "Zalicytowałeś, czekaj na innych...";
        }

        return;
    }

    // ---------- FAZA WYNIKÓW ----------
    bidSection.style.display = "none";
    statusInfo.textContent = "Wyniki:";

    resultsDiv.innerHTML = "";

    // znajdź najmniejszą ofertę
    let minBid = Infinity;
    let winnerId = null;

    for (const [pid, bid] of Object.entries(bids)) {
        if (bid < minBid) {
            minBid = bid;
            winnerId = pid;
        }
    }

    players.forEach(p => {
        const div = document.createElement("div");
        div.className = "result";

        const bid = bids[p.id];

        div.textContent = `${p.name}: ${bid}`;

        if (p.id === winnerId) {
            div.style.border = "3px solid yellow";
            div.textContent += " 👑";
        }

        resultsDiv.appendChild(div);
    });
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

    window.lastPlayers = status.players;

    if (status.lvl !== window.location.pathname) {
        window.location.href = status.lvl;
        return;
    }

    interprateGame(status.game_state);
}

setInterval(interprateState, 2000);
interprateState();
