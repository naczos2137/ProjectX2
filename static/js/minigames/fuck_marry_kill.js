const personsDiv = document.getElementById("persons");

const fuckSelect = document.getElementById("fuckSelect");
const marrySelect = document.getElementById("marrySelect");
const killSelect = document.getElementById("killSelect");

const voteBtn = document.getElementById("voteBtn");
const voteSection = document.getElementById("voteSection");
const statusInfo = document.getElementById("statusInfo");

let initialized = false;
let hasVoted = false;
let lastStatus = null;

// -----------------
// SEND
// -----------------

async function sendVote(vote) {

    const clientId = localStorage.getItem("client_id");

    await fetch("/set_info", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_id: clientId,
            game_info: {
                vote: vote
            }
        })
    });

    hasVoted = true;
}

// -----------------
// INIT
// -----------------

function addOptions(select, persons) {

    select.innerHTML = "";

    persons.forEach(person => {

        const option = document.createElement("option");

        option.value = person;
        option.textContent = person;

        select.appendChild(option);
    });
}

function initializePersons(persons) {

    if (initialized) return;

    personsDiv.innerHTML = "";

    persons.forEach(person => {

        const div = document.createElement("div");

        div.className = "person";
        div.textContent = person;

        personsDiv.appendChild(div);
    });

    addOptions(fuckSelect, persons);
    addOptions(marrySelect, persons);
    addOptions(killSelect, persons);

    initialized = true;
}

// -----------------
// BUTTON
// -----------------

voteBtn.onclick = async () => {

    const fuck = fuckSelect.value;
    const marry = marrySelect.value;
    const kill = killSelect.value;

    const unique = new Set([
        fuck,
        marry,
        kill
    ]);

    if (unique.size !== 3) {

        statusInfo.textContent =
            "Każda osoba musi mieć inną rolę.";

        return;
    }

    await sendVote({
        fuck: fuck,
        marry: marry,
        kill: kill
    });

    voteSection.style.display = "none";

    statusInfo.textContent =
        "Głos oddany. Oczekiwanie na innych graczy...";
};

// -----------------
// GAME
// -----------------

function interpretGame(game_state) {

    initializePersons(game_state.persons);

    if (game_state.finished) {

        voteSection.style.display = "none";

        let html = "<h3>Wyniki</h3>";

        for (const player of window.lastPlayers) {

            const result = game_state.results[player.id];

            if (!result) continue;

            html += `
                <div class="result">
                    <b>${player.name}</b><br>
                    ❤️ ${result.vote.fuck}<br>
                    💍 ${result.vote.marry}<br>
                    🔪 ${result.vote.kill}<br>
                    💰 +${result.money}
                </div>
            `;
        }

        statusInfo.innerHTML = html;

        return;
    }

    if (hasVoted) {
        voteSection.style.display = "none";
    }
}

// -----------------
// LOOP
// -----------------

async function interprateState() {

    const clientId =
        localStorage.getItem("client_id");

    const res = await fetch(
        `/get_status?client_id=${clientId}`
    );

    if (res.status === 401) {
        window.location.href = "/";
        return;
    }

    const status = await res.json();

    window.lastPlayers = status.players;

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

async function loop() {
    await interprateState();
    setTimeout(loop, 2000);
}

loop();