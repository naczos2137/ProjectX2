const questionDiv = document.getElementById("question");

const guessSection = document.getElementById("guessSection");
const guessInput = document.getElementById("guessInput");
const sendGuessBtn = document.getElementById("sendGuessBtn");

const statusInfo = document.getElementById("statusInfo");
const resultsDiv = document.getElementById("results");

let hasGuessed = false;

let lastStatus = null;

// ---------- SEND ----------

async function sendGuess(value) {
    const clientId = localStorage.getItem("client_id");

    await fetch("/set_info", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_id: clientId,
            game_info: {
                guess: value
            }
        })
    });

    hasGuessed = true;
}

// ---------- BUTTON ----------

sendGuessBtn.onclick = () => {
    const val = parseInt(guessInput.value);
    if (isNaN(val)) return;

    sendGuess(val);
};

// ---------- MAIN ----------

function interprateGame(game_state) {
    const clientId = localStorage.getItem("client_id");
    const players = window.lastPlayers || [];

    questionDiv.innerHTML = game_state.question || "";

    const guesses = game_state.guesses || {};
    const correctAnswer = game_state.answer;

    // ---------- PRZED ODPOWIEDZIĄ ----------
    if (!hasGuessed) {
        resultsDiv.innerHTML = "";
        statusInfo.textContent = "Podaj swoją odpowiedź";

        guessSection.style.display = "block";
        return;
    }

    // ---------- PO ODPOWIEDZI ----------
    guessSection.style.display = "none";

    statusInfo.textContent = `Poprawna odpowiedź: ${correctAnswer}`;

    resultsDiv.innerHTML = "";

    // sortuj graczy po odpowiedziach rosnąco
    const sortedPlayers = players
        .filter(p => guesses[p.id] !== undefined)
        .sort((a, b) => guesses[a.id] - guesses[b.id]);

    sortedPlayers.forEach(p => {
        const div = document.createElement("div");
        div.className = "result";

        const guess = guesses[p.id];

        div.textContent = `${p.name}: ${guess}`;

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