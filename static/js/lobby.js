const playersList = document.getElementById("playersList");

const clientId = localStorage.getItem("client_id");

let players = [];
let lastStatus = null;
let shopRendered = false;

function renderPlayers() {
    const existing = new Map();

    document.querySelectorAll(".player").forEach(el => {
        existing.set(el.dataset.id, el);
    });

    const currentIds = new Set();

    players.forEach(p => {
        currentIds.add(p.id);

        if (!existing.has(p.id)) {
            const div = document.createElement("div");
            div.className = "player";
            div.dataset.id = p.id;

            div.innerHTML = `
                <img src="/static/avatars/${p.avatar}">
                <div class="player-name">${p.name}</div>
                <div class="player-score"></div>
            `;

            playersList.appendChild(div);
        }
        const el = playersList.querySelector(`[data-id="${p.id}"]`);
        let score_text = p.money + '💰'
        if (p.beer || p.beer > 0) {
            score_text += ' Pij ' + p.beer + '🍺'
        }
        el.querySelector(".player-score").textContent = score_text ;

    });

    existing.forEach((el, id) => {
        if (!currentIds.has(id)) {
            el.remove();
        }
    });
}

const shopItems = [
    {
        name: "you_drink",
        cost: 200,
        require_target: true,
        view_name: "Pijesz TY 🍺",
        image: "/static/shop/beer.png"
    },
    {
        name: "workout_20",
        cost: 400,
        require_target: true,
        view_name: "20 pompek/przysiadów 🏋️",
        image: "/static/shop/gym.webp"
    },
    {
        name: "everyone_drink",
        cost: 500,
        require_target: false,
        view_name: "Wszyscy piją 🍺🍺",
        image: "/static/shop/beer.png"
    },
    {
        name: "question_master",
        cost: 500,
        require_target: false,
        view_name: "Kto odpowie na Twoje pytanie - pije ❓ (max 1 osoba z tym, jak 2 kupi to 1 przestaje być)",
        image: "/static/shop/question_master.gif"
    },
    {
        name: "new_rule",
        cost: 999,
        require_target: false,
        view_name: "Wprowadzasz nową zasade",
        image: "/static/shop/rule.webp"
    },
    {
        name: "king_title",
        cost: 2000,
        require_target: false,
        view_name: "Każdy musi się do Ciebie zwracać wybranym przez Ciebie tytułem (np. Królu), albo pije ⭐",
        image: "/static/shop/king.png"
    }
];

function getCurrentPlayer() {
    return players.find(p => p.id === clientId);
}

function renderShop() {
    const container = document.getElementById("shop-items");
    container.innerHTML = "";

    const currentPlayer = getCurrentPlayer();
    if (!currentPlayer) return;

    shopItems.forEach(item => {
        const canAfford = currentPlayer.money >= item.cost;

        const div = document.createElement("div");
        div.className = "shop-item";

        let dropdownHTML = "";

        if (item.require_target) {
            dropdownHTML = `
                <select class="target-select">
                    <option value="">-- wybierz gracza --</option>
                    ${players
                        .filter(p => p.id !== clientId)
                        .map(p => `<option value="${p.id}">${p.name}</option>`)
                        .join("")}
                </select>
            `;
        }

        div.innerHTML = `
            <img src="${item.image}" alt="${item.name}">
            <h3>${item.view_name}</h3>
            <p>Koszt: ${item.cost}</p>
            ${dropdownHTML}
            <button data-cost="${item.cost}" ${!canAfford ? "disabled" : ""}>
                Kup
            </button>
        `;

        const button = div.querySelector("button");
        const select = div.querySelector(".target-select");

        button.addEventListener("click", () => {
            if (!canAfford) return;

            let targetId = null;

            if (item.require_target) {
                targetId = select.value;

                if (!targetId) {
                    alert("Wybierz gracza!");
                    return;
                }
            }

            buyItem(item.name, targetId);
        });

        container.appendChild(div);
    });
}

function buyItem(itemName, targetId = null) {
    fetch("/buy", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_id: clientId,
            item: itemName,
            target_id: targetId
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Kupiono:", data);

        // opcjonalnie odśwież dane graczy
        // np. fetchPlayers();
    })
    .catch(err => console.error(err));
}

function shopRefresh() {
    const currentPlayer = getCurrentPlayer();
    if (!currentPlayer) return;

    const buttons = document.querySelectorAll("#shop-items button");

    buttons.forEach(button => {
        const cost = parseInt(button.dataset.cost);

        if (currentPlayer.money >= cost) {
            button.disabled = false;
        } else {
            button.disabled = true;
        }
    });
}

function drawBuyHistory(buyHistory) {
    console.log(buyHistory);
    const container = document.getElementById("buy-history-list");
    container.innerHTML = "";

    // pomocnicza mapa itemów (name -> view_name)
    const itemMap = {};
    shopItems.forEach(item => {
        itemMap[item.name] = item.view_name;
    });

    // odwracamy żeby najnowsze były na górze
    [...buyHistory].reverse().forEach(entry => {
        const player = players.find(p => p.id === entry.buyer);
        if (!player) return;

        const viewName = itemMap[entry.item] || entry.item;

        const div = document.createElement("div");
        div.className = "buy-entry";

        div.innerHTML = `
            <img src="static/avatars/${player.avatar}" alt="${player.name}">
            <div class="text">
                <span class="player">${player.name}</span><br>
                kupił <span class="item">${viewName}</span>
            </div>
        `;

        container.appendChild(div);
    });
}

async function loadPlayers() {
    const res = await fetch(`/get_status?client_id=${clientId}`);

    const status = await res.json();

    if (lastStatus &&
        JSON.stringify(lastStatus) === JSON.stringify(status)) {
        return; // nic się nie zmieniło → nie renderujemy
    }

    lastStatus = status;

    if (status.lvl !== window.location.pathname) {
        window.location.href = status.lvl
        return
    }

    const new_players = status.players;
    if(new_players === players) return;
    players = new_players;
    if (!shopRendered) {
        shopRendered = true;
        renderShop()
    }
    renderPlayers();
    shopRefresh();

    let buyHistory = status.buy_history;
    drawBuyHistory(buyHistory);
}

setInterval(loadPlayers, 2000);
loadPlayers();


// inicjalizacja
