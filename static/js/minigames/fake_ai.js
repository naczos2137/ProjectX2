const roleInfo = document.getElementById("roleInfo");

const questionSection = document.getElementById("questionSection");
const questionInput = document.getElementById("questionInput");
const sendQuestionBtn = document.getElementById("sendQuestionBtn");

const currentQuestionDiv = document.getElementById("currentQuestion");
const answerSection = document.getElementById("answerSection");
const answerInput = document.getElementById("answerInput");
const sendAnswerBtn = document.getElementById("sendAnswerBtn");

const answersList = document.getElementById("answersList");

let lastStatus = null;

// ---------- SEND ----------

async function sendGameInfo(game_info) {
    const clientId = localStorage.getItem("client_id");

    await fetch("/set_info", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_id: clientId,
            game_info: game_info
        })
    });
}

// ---------- BUTTONS ----------

sendQuestionBtn.onclick = () => {
    const q = questionInput.value;
    if (!q) return;

    sendGameInfo({
        set_question: q
    });
};

sendAnswerBtn.onclick = () => {
    const a = answerInput.value;
    if (!a) return;

    sendAnswerBtn.style.display = "none";
    sendGameInfo({
        set_answers: a
    });
};

// ---------- MAIN LOGIC ----------

function interprateGame(game_state) {
    const clientId = localStorage.getItem("client_id");

    const players = window.lastPlayers || [];

    // znajdź detektora
    const detector = players.find(p => p.id === game_state.ai_detector_id);

    // ustaw info o roli
    if (game_state.ai_detector_id === clientId) {
        roleInfo.textContent = "Jesteś detektorem 🤖";
    } else {
        roleInfo.textContent = `Detektor: ${detector ? detector.name : "..."}`;
    }

    // RESET VISIBILITY
    questionSection.style.display = "none";
    answerSection.style.display = "none";

    // ---------- FAZA PYTANIA ----------
    if (!game_state.question) {
        if (game_state.ai_detector_id === clientId) {
            questionSection.style.display = "block";
        }
        answersList.innerHTML = "";
        return;
    }

    // ---------- FAZA ODPOWIEDZI ----------
    if (game_state.question && (!game_state.answers || game_state.answers.length === 0)) {
        if (game_state.ai_detector_id !== clientId) {
            answerSection.style.display = "block";
            currentQuestionDiv.textContent = `Pytanie: ${game_state.question}`;
        } else {
            currentQuestionDiv.textContent = "";
        }
        answersList.innerHTML = "";
        return;
    }

    // ---------- FAZA WYBORU ----------
    if (game_state.answers && game_state.answers.length > 0) {
        answersList.innerHTML = "";
        const isReveal = game_state.chosen_answer_autor !== null;

        game_state.answers.forEach(a => {
            const div = document.createElement("div");
            div.className = "answer";
            div.textContent = a[1];

            // tylko detektor może wybierać
            if (isReveal) {
                if (a[0] === 'ai') {
                    div.textContent = '🤖AI: ' + a[1]
                } else {
                    const autor = players.find(p => p.id === a[0])
                    div.textContent = '🧑' + autor.name + ': ' + a[1]
                }
                if (a[0] === game_state.chosen_answer_autor) {
                    div.style.border = "5px solid yellow";
                }
            } else if (game_state.ai_detector_id === clientId) {
                div.onclick = () => {
                    sendGameInfo({
                        chosen_answer: a[0]
                    });
                };
            } else {
                div.style.cursor = "default";
            }

            answersList.appendChild(div);
        });
    }
}

// ---------- LOOP (TWOJE) ----------

async function interprateState() {
    const clientId = localStorage.getItem("client_id");

    const res = await fetch(`/get_status?client_id=${clientId}`);

    const status = await res.json();

    if (lastStatus &&
        JSON.stringify(lastStatus) === JSON.stringify(status)) {
        return; // nic się nie zmieniło → nie renderujemy
    }

    lastStatus = status;

    window.lastPlayers = status.players;

    if (status.lvl !== window.location.pathname) {
        window.location.href = status.lvl
        return
    }

    const game_state = status.game_state;
    interprateGame(game_state);
}

setInterval(interprateState, 2000);
interprateState();