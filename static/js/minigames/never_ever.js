const selectorInfo = document.getElementById("selectorInfo");
const categorySection = document.getElementById("categorySection");
const questionSection = document.getElementById("questionSection");

let categoryChosen = false;
let lastStatus = null;

// ---------- SEND CATEGORY ----------

async function sendCategory(category) {
    const clientId = localStorage.getItem("client_id");

    await fetch("/set_info", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_id: clientId,
            game_info: {
                category: category
            }
        })
    });

    categoryChosen = true;
}

// ---------- GAME ----------

function interprateGame(game_state) {

    const clientId = localStorage.getItem("client_id");
    const players = window.lastPlayers || [];

    const selectorId = game_state.selector;
    const question = game_state.question;
    const categories = game_state.categories || [];

    // ==========================
    // WYBIERANIE KATEGORII
    // ==========================

    if (question === null) {

        questionSection.innerHTML = "";

        // SELECTOR
        if (selectorId === clientId) {

            selectorInfo.innerHTML =
                "<h3>Wybierz kategorię</h3>";

            if (!categoryChosen) {

                categorySection.innerHTML = "";

                categories.forEach(category => {

                    const btn = document.createElement("button");

                    btn.className = "category-btn";
                    btn.textContent = category;

                    btn.onclick = () => {
                        sendCategory(category);
                        categorySection.innerHTML =
                            "<p>Oczekiwanie na pytanie...</p>";
                    };

                    categorySection.appendChild(btn);
                });
            }

        }

        // POZOSTALI
        else {

            categorySection.innerHTML = "";

            const selector = players.find(
                p => p.id === selectorId
            );

            if (!selector) return;

            selectorInfo.innerHTML = `
                <h3>Wybiera kategorię:</h3>

                <img src="static/avatars/${selector.avatar}">

                <div class="selector-name">
                    ${selector.name}
                </div>
            `;
        }

        return;
    }

    // ==========================
    // PYTANIE
    // ==========================

    selectorInfo.innerHTML = "";
    categorySection.innerHTML = "";

    questionSection.innerHTML = `
        <div class="question">
            Nigdy, przenigdy nie ${question}.
        </div>

        <div class="drink-info">
            Jeśli to robiłeś to pijesz.
        </div>
    `;
}

// ---------- LOOP ----------

async function interprateState() {

    const clientId = localStorage.getItem("client_id");

    const res = await fetch(
        `/get_status?client_id=${clientId}`
    );

    const status = await res.json();

    if (
        lastStatus &&
        JSON.stringify(lastStatus) === JSON.stringify(status)
    ) {
        return;
    }

    lastStatus = status;

    window.lastPlayers = status.players;

    if (status.lvl !== window.location.pathname) {
        window.location.href = status.lvl;
        return;
    }

    interprateGame(status.game_state);
}

setInterval(interprateState, 2000);
interprateState();
