// ============================================================================
// PREACHING THE TRUTH - Web Version
// ============================================================================

// --- DATA ---

const PREACHERS = [
    {
        id: "belen",
        name: "Belen Torres",
        description: "An old Dominican woman, former witch turned evangelist with stories to tell",
        conversionBonus: 0.05,
        reputationBonus: -5,
        moneyBonus: 15,
        hungerRate: 1.1,
        personalityBonus: { lonely: 0.15, seeker: 0.20, skeptic: -0.10 },
        special: "Ex-witch who survived Haitian Vudu and demon encounters. Her testimony is wild."
    },
    {
        id: "scott",
        name: "Dr. Scott Johnson",
        description: "A scholarly theologian with logical arguments",
        conversionBonus: 0.0,
        reputationBonus: 5,
        moneyBonus: 20,
        hungerRate: 1.2,
        personalityBonus: { intellectual: 0.15, skeptic: 0.10 },
        special: "Persuasive with intellectuals and skeptics, but tires easily"
    },
    {
        id: "joyce",
        name: "Sister Joyce Meyer",
        description: "An energetic motivational preacher",
        conversionBonus: 0.0,
        reputationBonus: 0,
        moneyBonus: 10,
        hungerRate: 0.9,
        personalityBonus: { cynic: 0.15, hostile: 0.05 },
        special: "High energy and can break through to cynics"
    },
    {
        id: "billy",
        name: "Pastor Billy Graham Jr.",
        description: "A charismatic crusade-style preacher",
        conversionBonus: 0.10,
        reputationBonus: 10,
        moneyBonus: 0,
        hungerRate: 1.1,
        personalityBonus: { seeker: 0.15 },
        special: "Famous name opens doors, great with seekers"
    },
    {
        id: "joel",
        name: "Reverend Joel Prosperity",
        description: "A prosperity gospel preacher with a winning smile",
        conversionBonus: -0.05,
        reputationBonus: -5,
        moneyBonus: 50,
        hungerRate: 0.8,
        personalityBonus: { lonely: 0.10 },
        special: "Wealthy but people are wary of his motives"
    },
    {
        id: "marcus",
        name: "Brother Marcus",
        description: "A humble street preacher with fire in his heart",
        conversionBonus: 0.0,
        reputationBonus: -10,
        moneyBonus: -10,
        hungerRate: 0.85,
        personalityBonus: { hostile: 0.15, skeptic: -0.10 },
        special: "Fearless with hostile crowds but too intense for skeptics"
    },
    {
        id: "olga",
        name: "Titi Olga",
        description: "A wonderfully warm community mother with a heart full of love for everyone",
        conversionBonus: 0.08,
        reputationBonus: 5,
        moneyBonus: 30,
        hungerRate: 0.75,
        personalityBonus: { lonely: 0.20, cynic: 0.15, skeptic: 0.05 },
        special: "Such a blessing to everyone she meets. Truly. Everyone says so."
    }
];

const RELIGIONS = ["Evangelist", "Jehovah's Witness", "Mormon", "Custom"];

const PERSONALITIES = ["neutral", "skeptic", "seeker", "lonely", "intellectual", "cynic", "hostile"];
const MOODS = ["neutral", "receptive", "grumpy", "distracted", "curious"];

const FIRST_NAMES = ["Michael", "Jennifer", "Carlos", "Maria", "Billy", "Tammy", "Jose", "Rosa", "David", "Ashley", "Juan", "Elena", "Travis", "Crystal", "Miguel", "Sofia"];
const LAST_NAMES = ["Smith", "Johnson", "Garcia", "Rodriguez", "Williams", "Brown", "Martinez", "Davis", "Torres", "Gonzalez", "Wilson", "Anderson"];

const STREET_NAMES = ["Main", "Oak", "Maple", "Cedar", "Pine", "Church", "Park", "Washington", "Lincoln", "Magnolia", "First", "Second"];
const STREET_SUFFIXES = ["Street", "Avenue", "Road", "Drive", "Lane", "Boulevard"];

const OPENERS = [
    { id: "friendly", text: "Hello! Do you have a moment to talk about faith?", tags: ["friendly"], baseInterest: 5 },
    { id: "direct", text: "I'm here to share the good news with you today.", tags: ["direct"], baseInterest: 0 },
    { id: "question", text: "Have you ever wondered about the meaning of life?", tags: ["philosophical"], baseInterest: 8 },
    { id: "hellfire", text: "Are you prepared for judgment day?", tags: ["hellfire", "pushy"], baseInterest: -5 }
];

const OBJECTIONS = [
    { id: "busy", text: "I'm really busy right now...", personality_weight: { neutral: 2, distracted: 3 } },
    { id: "not_interested", text: "I'm not really interested in religion.", personality_weight: { skeptic: 2, cynic: 2 } },
    { id: "already_religious", text: "I already have my own beliefs.", personality_weight: { neutral: 1 } },
    { id: "prove_it", text: "How can you prove any of this is real?", personality_weight: { skeptic: 3, intellectual: 3 } },
    { id: "bad_experience", text: "I've had bad experiences with religious people.", personality_weight: { cynic: 3, hostile: 2 } },
    { id: "curious", text: "Tell me more about what you believe...", personality_weight: { seeker: 3, lonely: 2, curious: 2 } }
];

const RESPONSES = [
    { id: "empathetic", text: "I understand. Many people feel that way.", tags: ["friendly", "empathetic"], interestChange: 5 },
    { id: "testimony", text: "Let me share my personal experience with you.", tags: ["personal"], interestChange: 8 },
    { id: "logical", text: "Consider the evidence and historical records.", tags: ["logical"], interestChange: 3 },
    { id: "pushy", text: "You really need to hear this - your soul depends on it!", tags: ["pushy", "hellfire"], interestChange: -8 },
    { id: "community", text: "It's really about finding a community that cares.", tags: ["community", "friendly"], interestChange: 6 },
    { id: "leave", text: "I'll leave you to think about it. Have a blessed day.", tags: ["polite_exit"], interestChange: 0, isExit: true }
];

const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

// --- GAME STATE ---

let state = {
    phase: "welcome",
    preacher: null,
    religion: null,
    money: 20,
    hunger: 0,
    score: 0,
    dailyScore: 0,
    day: 0,

    // World
    county: null,
    currentTown: null,
    currentNeighborhood: null,
    currentStreet: null,
    currentLocation: null,

    // Conversation
    currentNPC: null,
    interest: 0,
    conversationTurn: 0,

    // Bonuses
    conversionBonus: 0,
    hungerRate: 1.0,
    personalityBonus: {}
};

// --- UTILITY FUNCTIONS ---

function randomChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateName() {
    return `${randomChoice(FIRST_NAMES)} ${randomChoice(LAST_NAMES)}`;
}

function generateStreetName() {
    return `${randomChoice(STREET_NAMES)} ${randomChoice(STREET_SUFFIXES)}`;
}

// --- WORLD GENERATION ---

function generateNPC() {
    return {
        name: generateName(),
        personality: randomChoice(PERSONALITIES),
        mood: randomChoice(MOODS),
        converted: false,
        resistant: Math.random() < 0.3
    };
}

function generateLocation(type) {
    const npcs = [];
    const npcCount = type === "house" ? randomInt(1, 4) : 1;
    for (let i = 0; i < npcCount; i++) {
        npcs.push(generateNPC());
    }

    let name;
    if (type === "house") {
        name = `${randomInt(100, 9999)} ${generateStreetName()}`;
    } else if (type === "store") {
        name = randomChoice(["Quick Stop", "Corner Mart", "Save-A-Lot", "Mini Mart", "7-Eleven"]);
    } else if (type === "church") {
        name = `${randomChoice(["First", "New", "Grace", "Faith"])} ${randomChoice(["Baptist", "Methodist", "Community"])} Church`;
    }

    return { type, name, npcs };
}

function generateStreet() {
    const locations = [];
    const count = randomInt(3, 5);
    for (let i = 0; i < count; i++) {
        const roll = Math.random();
        let type = "house";
        if (roll > 0.9) type = "church";
        else if (roll > 0.8) type = "store";
        locations.push(generateLocation(type));
    }
    return { name: generateStreetName(), locations };
}

function generateNeighborhood() {
    const streets = [];
    const count = randomInt(2, 5);
    for (let i = 0; i < count; i++) {
        streets.push(generateStreet());
    }
    const suffixes = ["Heights", "Park", "Gardens", "District", "Village"];
    return { name: `${randomChoice(STREET_NAMES)} ${randomChoice(suffixes)}`, streets };
}

function generateTown() {
    const neighborhoods = [];
    const count = randomInt(2, 3);
    for (let i = 0; i < count; i++) {
        neighborhoods.push(generateNeighborhood());
    }
    const suffixes = ["ville", "town", "burg", "field", "springs"];
    return { name: `${randomChoice(STREET_NAMES)}${randomChoice(suffixes)}`, neighborhoods };
}

function generateCounty() {
    const towns = [];
    for (let i = 0; i < 3; i++) {
        towns.push(generateTown());
    }
    return { name: `${randomChoice(LAST_NAMES)} County`, towns };
}

// --- UI FUNCTIONS ---

const output = document.getElementById("output");
const choices = document.getElementById("choices");

function clearOutput() {
    output.innerHTML = "";
}

function print(text, className = "narrator") {
    const p = document.createElement("p");
    p.className = className;
    p.innerHTML = text;
    output.appendChild(p);
    output.scrollTop = output.scrollHeight;
}

function printHeading(text) {
    print(text, "heading");
}

function printSpeech(text) {
    print(`"${text}"`, "npc-speech");
}

function printSuccess(text) {
    print(text, "success");
}

function printFailure(text) {
    print(text, "failure");
}

function printThought(text) {
    print(`* ${text} *`, "thought");
}

function clearChoices() {
    choices.innerHTML = "";
}

function addChoice(text, callback, className = "choice-btn") {
    const btn = document.createElement("button");
    btn.className = className;
    btn.textContent = text;
    btn.onclick = callback;
    choices.appendChild(btn);
}

function addBackChoice(text, callback) {
    addChoice(text, callback, "choice-btn back-btn");
}

function updateStatus() {
    document.getElementById("stat-preacher").textContent = `Preacher: ${state.preacher?.name || "-"}`;
    document.getElementById("stat-day").textContent = `Day: ${DAYS[state.day % 7]}`;
    document.getElementById("stat-hunger").textContent = `Hunger: ${state.hunger}/100`;
    document.getElementById("stat-money").textContent = `Money: $${state.money}`;
    document.getElementById("stat-souls").textContent = `Souls: ${state.score}`;

    let loc = "";
    if (state.currentTown) loc += state.currentTown.name;
    if (state.currentNeighborhood) loc += ` > ${state.currentNeighborhood.name}`;
    if (state.currentStreet) loc += ` > ${state.currentStreet.name}`;
    document.getElementById("current-location").textContent = loc || "Home";
}

// --- GAME PHASES ---

function showWelcome() {
    clearOutput();
    clearChoices();
    state.phase = "welcome";

    print("In this game, you play as a preacher for a chosen religion.");
    print("Your goal is to win as many souls as you can by going door-to-door and preaching your faith.");
    print("");
    print("Each day you will encounter various responses from people. Your hunger increases as you preach. When it reaches 100, the day ends.");
    print("");
    print("<b>Controls:</b> Click buttons to make choices. Press '0' options to go back.");
    print("");

    addChoice("Begin Game", showPreacherSelect);
}

function showPreacherSelect() {
    clearOutput();
    clearChoices();
    state.phase = "preacher_select";

    printHeading("Choose Your Preacher");

    PREACHERS.forEach((p, i) => {
        print(`<b>${p.name}</b> - ${p.description}`);
        print(`<i>Special: ${p.special}</i>`);
        print("");
    });

    PREACHERS.forEach((p) => {
        addChoice(p.name, () => selectPreacher(p));
    });

    addChoice("Custom Character", () => {
        const name = prompt("Enter your preacher's name:");
        if (name) {
            selectPreacher({
                id: "custom",
                name: name,
                description: "A dedicated servant of the faith",
                conversionBonus: 0,
                reputationBonus: 0,
                moneyBonus: 0,
                hungerRate: 1.0,
                personalityBonus: {},
                special: "A blank slate - no bonuses or penalties"
            });
        }
    }, "choice-btn special-btn");
}

function selectPreacher(preacher) {
    state.preacher = preacher;
    state.money = 20 + preacher.moneyBonus;
    state.conversionBonus = preacher.conversionBonus;
    state.hungerRate = preacher.hungerRate;
    state.personalityBonus = preacher.personalityBonus;

    updateStatus();
    showReligionSelect();
}

function showReligionSelect() {
    clearOutput();
    clearChoices();
    state.phase = "religion_select";

    printHeading("Choose Your Religion");
    print(`You are ${state.preacher.name}.`);
    print(state.preacher.special);
    print("");

    RELIGIONS.forEach((r) => {
        addChoice(r, () => selectReligion(r));
    });
}

function selectReligion(religion) {
    state.religion = religion;
    state.county = generateCounty();
    updateStatus();
    startDay();
}

function startDay() {
    state.hunger = 0;
    state.dailyScore = 0;
    state.currentTown = null;
    state.currentNeighborhood = null;
    state.currentStreet = null;
    state.currentLocation = null;

    clearOutput();
    clearChoices();

    printHeading(`Day ${state.day + 1} - ${DAYS[state.day % 7]}`);
    print(`You wake up ready to spread the word.`);

    if (state.day % 7 === 0) {
        const offering = randomInt(5, 15);
        state.money += offering;
        printSuccess(`It's Sunday! You receive $${offering} from the offering.`);
    }

    print("");
    updateStatus();

    addChoice("Head out to preach", showTownSelect);
}

function showTownSelect() {
    clearOutput();
    clearChoices();

    printHeading(state.county.name);
    print("Choose a town to visit:");
    print("");

    state.county.towns.forEach((town) => {
        addChoice(`${town.name} (${town.neighborhoods.length} neighborhoods)`, () => {
            state.currentTown = town;
            updateStatus();
            showNeighborhoodSelect();
        });
    });
}

function showNeighborhoodSelect() {
    clearOutput();
    clearChoices();

    printHeading(state.currentTown.name);
    print("Choose a neighborhood:");
    print("");

    state.currentTown.neighborhoods.forEach((n) => {
        addChoice(`${n.name} (${n.streets.length} streets)`, () => {
            state.currentNeighborhood = n;
            updateStatus();
            showStreetSelect();
        });
    });

    addBackChoice("0. Back to town selection", () => {
        state.currentTown = null;
        updateStatus();
        showTownSelect();
    });
}

function showStreetSelect() {
    clearOutput();
    clearChoices();

    printHeading(state.currentNeighborhood.name);
    print("Choose a street:");
    print("");

    state.currentNeighborhood.streets.forEach((s) => {
        addChoice(`${s.name} (${s.locations.length} locations)`, () => {
            state.currentStreet = s;
            updateStatus();
            showLocationSelect();
        });
    });

    addBackChoice("0. Back to neighborhood selection", () => {
        state.currentNeighborhood = null;
        updateStatus();
        showNeighborhoodSelect();
    });
}

function showLocationSelect() {
    clearOutput();
    clearChoices();

    printHeading(state.currentStreet.name);
    print("Choose a location:");
    print("");

    state.currentStreet.locations.forEach((loc) => {
        const icon = loc.type === "house" ? "🏠" : loc.type === "store" ? "🏪" : "⛪";
        const status = loc.npcs.every(n => n.converted) ? " (all converted)" : "";
        addChoice(`${icon} ${loc.name}${status}`, () => {
            state.currentLocation = loc;
            handleLocation();
        });
    });

    addBackChoice("0. Back to street selection", () => {
        state.currentStreet = null;
        updateStatus();
        showStreetSelect();
    });
}

function handleLocation() {
    clearOutput();
    clearChoices();

    const loc = state.currentLocation;
    printHeading(loc.name);

    if (loc.type === "store") {
        handleStore();
    } else if (loc.type === "church") {
        handleChurch();
    } else {
        handleHouse();
    }
}

function handleStore() {
    print("You enter the store.");
    print("");

    const items = [
        { name: "Candy Bar", price: 2, hunger: -10 },
        { name: "Sandwich", price: 5, hunger: -20 },
        { name: "Hot Meal", price: 8, hunger: -35 }
    ];

    items.forEach((item) => {
        const affordable = state.money >= item.price ? "" : " (can't afford)";
        addChoice(`${item.name} - $${item.price} (${item.hunger} hunger)${affordable}`, () => {
            if (state.money >= item.price) {
                state.money -= item.price;
                state.hunger = Math.max(0, state.hunger + item.hunger);
                printSuccess(`You bought ${item.name} and ate it.`);
                updateStatus();
            } else {
                printFailure("You can't afford that.");
            }
        });
    });

    addBackChoice("0. Leave store", showNextAction);
}

function handleChurch() {
    const friendly = Math.random() > 0.3;

    if (friendly) {
        printSuccess("The congregation welcomes you warmly!");
        print("Your spirits are lifted.");
    } else {
        printFailure("This church doesn't appreciate your denomination.");
        print("You're asked to leave.");
        state.hunger = Math.min(100, state.hunger + 10);
        updateStatus();
    }

    addChoice("Continue", showNextAction);
}

function handleHouse() {
    const unconverted = state.currentLocation.npcs.filter(n => !n.converted);

    if (unconverted.length === 0) {
        print("Everyone here has already been converted.");
        addChoice("Continue", showNextAction);
        return;
    }

    print(`You see ${unconverted.length} people here:`);
    print("");

    unconverted.forEach((npc) => {
        const hint = npc.resistant ? " [Resistant]" : "";
        addChoice(`${npc.name}${hint}`, () => startConversation(npc));
    });

    addBackChoice("0. Move on", showNextAction);
}

function startConversation(npc) {
    state.currentNPC = npc;
    state.conversationTurn = 0;

    // Calculate starting interest
    let interest = 0;
    if (npc.mood === "receptive") interest += 10;
    if (npc.mood === "grumpy") interest -= 10;
    if (npc.mood === "curious") interest += 5;

    // Apply preacher personality bonus
    if (state.personalityBonus[npc.personality]) {
        interest += Math.floor(state.personalityBonus[npc.personality] * 50);
    }

    if (npc.resistant) interest -= 25;

    state.interest = interest;

    clearOutput();
    clearChoices();

    printHeading(`Conversation with ${npc.name}`);
    showInterestBar();

    const moodText = {
        neutral: "They regard you calmly.",
        receptive: "They seem open to talking.",
        grumpy: "They look annoyed.",
        distracted: "They seem distracted.",
        curious: "They look curious."
    };
    print(moodText[npc.mood] || "They wait for you to speak.");
    print("");

    showOpenerChoices();
}

function showInterestBar() {
    const pct = Math.max(0, Math.min(100, (state.interest + 50)));
    print(`Interest: [${"=".repeat(Math.floor(pct / 5))}${"-".repeat(20 - Math.floor(pct / 5))}]`);
}

function showOpenerChoices() {
    print("How do you want to start?");
    print("");

    OPENERS.forEach((opener) => {
        addChoice(`"${opener.text}"`, () => useOpener(opener));
    });
}

function useOpener(opener) {
    state.interest += opener.baseInterest;
    state.conversationTurn++;

    clearOutput();
    printHeading(`Conversation with ${state.currentNPC.name}`);
    showInterestBar();
    print("");

    printSpeech(opener.text);

    if (state.interest >= 50) {
        endConversation(true);
    } else if (state.interest <= -30) {
        endConversation(false);
    } else {
        showObjection();
    }
}

function showObjection() {
    // Pick a weighted objection based on personality
    const npc = state.currentNPC;
    let objection = randomChoice(OBJECTIONS);

    print("");
    printSpeech(objection.text);
    print("");

    showResponseChoices();
}

function showResponseChoices() {
    print("How do you respond?");
    print("");

    RESPONSES.forEach((resp) => {
        addChoice(`"${resp.text}"`, () => useResponse(resp));
    });
}

function useResponse(response) {
    state.interest += response.interestChange;
    state.conversationTurn++;

    clearOutput();
    printHeading(`Conversation with ${state.currentNPC.name}`);
    showInterestBar();
    print("");

    printSpeech(response.text);
    print("");

    if (response.isExit) {
        print("You part ways politely.");
        applyHunger();
        addChoice("Continue", showNextAction);
        return;
    }

    // NPC reaction
    if (response.interestChange > 0) {
        print("They seem to warm up to you.");
    } else if (response.interestChange < 0) {
        print("They look uncomfortable.");
    }

    if (state.interest >= 50) {
        endConversation(true);
    } else if (state.interest <= -30 || state.conversationTurn >= 5) {
        endConversation(false);
    } else {
        showObjection();
    }
}

function endConversation(success) {
    applyHunger();

    print("");

    if (success) {
        state.currentNPC.converted = true;
        state.score++;
        state.dailyScore++;

        printSuccess("SUCCESS! They want to learn more about your faith!");

        // Chance for donation
        if (Math.random() < 0.3) {
            const donation = randomInt(5, 20);
            state.money += donation;
            print(`They donate $${donation} to your ministry!`);
        }
    } else {
        printFailure("They've had enough and close the door.");
    }

    updateStatus();

    if (state.hunger >= 100) {
        addChoice("End Day", endDay);
    } else {
        addChoice("Continue", showNextAction);
    }
}

function applyHunger() {
    const amount = Math.floor(10 * state.hungerRate);
    state.hunger = Math.min(100, state.hunger + amount);
    updateStatus();
}

function showNextAction() {
    if (state.hunger >= 100) {
        endDay();
        return;
    }

    clearOutput();
    clearChoices();

    print("What would you like to do?");
    print("");

    addChoice("1. Choose another location on this street", showLocationSelect);
    addChoice("2. Go to a different street", () => {
        state.currentStreet = null;
        showStreetSelect();
    });
    addChoice("3. Go to a different neighborhood", () => {
        state.currentStreet = null;
        state.currentNeighborhood = null;
        showNeighborhoodSelect();
    });
    addChoice("4. Go to a different town", () => {
        state.currentStreet = null;
        state.currentNeighborhood = null;
        state.currentTown = null;
        showTownSelect();
    });
}

function endDay() {
    clearOutput();
    clearChoices();

    printHeading("Day's End");
    print("You're too tired and hungry to continue.");
    print("");
    print(`Souls won today: ${state.dailyScore}`);
    print(`Total souls: ${state.score}`);
    print(`Money: $${state.money}`);
    print("");

    state.day++;

    if (state.day >= 7) {
        endGame();
    } else {
        addChoice("Start Next Day", startDay);
    }
}

function endGame() {
    printHeading("Your Ministry Has Ended");
    print("");
    print(`In 7 days, you won ${state.score} souls to the faith!`);
    print("");

    if (state.score >= 20) {
        printSuccess("Amazing! You are a true messenger of the faith!");
    } else if (state.score >= 10) {
        print("A respectable ministry. The faithful are grateful.");
    } else if (state.score >= 5) {
        print("A humble effort. Every soul counts.");
    } else {
        print("The path of faith is not easy. Keep trying.");
    }

    print("");
    addChoice("Play Again", () => {
        state = {
            phase: "welcome",
            preacher: null,
            religion: null,
            money: 20,
            hunger: 0,
            score: 0,
            dailyScore: 0,
            day: 0,
            county: null,
            currentTown: null,
            currentNeighborhood: null,
            currentStreet: null,
            currentLocation: null,
            currentNPC: null,
            interest: 0,
            conversationTurn: 0,
            conversionBonus: 0,
            hungerRate: 1.0,
            personalityBonus: {}
        };
        updateStatus();
        showWelcome();
    });
}

// --- START GAME ---
updateStatus();
showWelcome();
