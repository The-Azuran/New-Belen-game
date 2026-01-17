// ============================================================================
// PREACHING THE TRUTH - Web Version
// By Rowan Valis & Claude
// ============================================================================

// --- CONFIGURATION ---
const CONFIG = {
    CONVERSION_THRESHOLD: 50,
    REJECTION_THRESHOLD: -30,
    MAX_CONVERSATION_TURNS: 5,
    BASE_HUNGER_PER_CONVERSATION: 10,
    GAME_LENGTH_DAYS: 7,
    DONATION_CHANCE: 0.3,
    DONATION_MIN: 5,
    DONATION_MAX: 20
};

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
const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

const FIRST_NAMES = ["Michael", "Jennifer", "Carlos", "Maria", "Billy", "Tammy", "Jose", "Rosa", "David", "Ashley", "Juan", "Elena", "Travis", "Crystal", "Miguel", "Sofia"];
const LAST_NAMES = ["Smith", "Johnson", "Garcia", "Rodriguez", "Williams", "Brown", "Martinez", "Davis", "Torres", "Gonzalez", "Wilson", "Anderson"];
const STREET_NAMES = ["Main", "Oak", "Maple", "Cedar", "Pine", "Church", "Park", "Washington", "Lincoln", "Magnolia", "First", "Second"];
const STREET_SUFFIXES = ["Street", "Avenue", "Road", "Drive", "Lane", "Boulevard"];

// --- DIALOGUE DATA ---
const OPENERS = [
    {
        id: "friendly",
        text: "Hello! Do you have a moment to talk about faith?",
        tags: ["friendly", "gentle"],
        baseInterest: 5,
        effectiveWith: ["neutral", "seeker", "lonely", "curious"],
        ineffectiveWith: ["hostile"]
    },
    {
        id: "direct",
        text: "I'm here to share the good news with you today.",
        tags: ["direct"],
        baseInterest: 0,
        effectiveWith: ["neutral", "intellectual"],
        ineffectiveWith: ["cynic", "hostile"]
    },
    {
        id: "question",
        text: "Have you ever wondered about the meaning of life?",
        tags: ["philosophical", "thoughtful"],
        baseInterest: 8,
        effectiveWith: ["seeker", "intellectual", "lonely", "curious"],
        ineffectiveWith: ["hostile", "grumpy"]
    },
    {
        id: "testimony",
        text: "Can I share something that changed my life?",
        tags: ["personal", "testimony"],
        baseInterest: 6,
        effectiveWith: ["seeker", "lonely", "curious", "receptive"],
        ineffectiveWith: ["skeptic", "intellectual"]
    },
    {
        id: "hellfire",
        text: "Are you prepared for judgment day?",
        tags: ["hellfire", "pushy"],
        baseInterest: -5,
        effectiveWith: ["seeker"],
        ineffectiveWith: ["skeptic", "intellectual", "cynic", "hostile", "neutral"]
    }
];

const OBJECTIONS = {
    busy: {
        id: "busy",
        text: "I'm really busy right now...",
        weights: { neutral: 2, distracted: 3 },
        counterWith: ["empathetic", "brief"]
    },
    not_interested: {
        id: "not_interested",
        text: "I'm not really interested in religion.",
        weights: { skeptic: 2, cynic: 2, neutral: 1 },
        counterWith: ["empathetic", "community", "question"]
    },
    already_religious: {
        id: "already_religious",
        text: "I already have my own beliefs.",
        weights: { neutral: 2 },
        counterWith: ["respectful", "common_ground"]
    },
    prove_it: {
        id: "prove_it",
        text: "How can you prove any of this is real?",
        weights: { skeptic: 3, intellectual: 3 },
        counterWith: ["logical", "testimony", "question"]
    },
    bad_experience: {
        id: "bad_experience",
        text: "I've had bad experiences with religious people.",
        weights: { cynic: 3, hostile: 2 },
        counterWith: ["empathetic", "apologetic", "different"]
    },
    curious: {
        id: "curious",
        text: "Tell me more about what you believe...",
        weights: { seeker: 3, lonely: 2, curious: 3 },
        counterWith: ["testimony", "community", "invitation"]
    },
    hurting: {
        id: "hurting",
        text: "I'm going through a really hard time right now.",
        weights: { lonely: 3, seeker: 2 },
        counterWith: ["empathetic", "community", "comfort"]
    },
    intellectual: {
        id: "intellectual",
        text: "I prefer to rely on science and reason.",
        weights: { intellectual: 3, skeptic: 2 },
        counterWith: ["logical", "respectful", "question"]
    }
};

const RESPONSES = {
    empathetic: {
        id: "empathetic",
        text: "I understand. Many people feel that way.",
        tags: ["friendly", "empathetic"],
        interestChange: 5,
        followUp: "Would you like to share what's on your mind?"
    },
    testimony: {
        id: "testimony",
        text: "Let me share my personal experience with you.",
        tags: ["personal"],
        interestChange: 8,
        effectiveWith: ["seeker", "lonely", "curious"],
        ineffectiveWith: ["skeptic", "intellectual"]
    },
    logical: {
        id: "logical",
        text: "Consider the evidence and historical records.",
        tags: ["logical", "intellectual"],
        interestChange: 4,
        effectiveWith: ["intellectual", "skeptic"],
        ineffectiveWith: ["hostile", "grumpy"]
    },
    community: {
        id: "community",
        text: "It's really about finding a community that cares.",
        tags: ["community", "friendly"],
        interestChange: 6,
        effectiveWith: ["lonely", "seeker"],
        ineffectiveWith: ["cynic"]
    },
    question: {
        id: "question",
        text: "What is it that you're looking for in life?",
        tags: ["thoughtful", "engaging"],
        interestChange: 4,
        effectiveWith: ["seeker", "lonely", "intellectual"],
        ineffectiveWith: ["hostile", "grumpy"]
    },
    comfort: {
        id: "comfort",
        text: "I'm sorry to hear that. Would you like someone to talk to?",
        tags: ["empathetic", "caring"],
        interestChange: 7,
        effectiveWith: ["lonely", "seeker"],
        ineffectiveWith: ["hostile", "skeptic"]
    },
    apologetic: {
        id: "apologetic",
        text: "I'm sorry you had that experience. Not everyone represents the faith well.",
        tags: ["empathetic", "humble"],
        interestChange: 6,
        effectiveWith: ["cynic", "hostile"],
        ineffectiveWith: []
    },
    invitation: {
        id: "invitation",
        text: "Would you like to visit our community sometime? No pressure.",
        tags: ["friendly", "inviting"],
        interestChange: 5,
        effectiveWith: ["seeker", "lonely", "curious"],
        ineffectiveWith: ["hostile", "skeptic"]
    },
    brief: {
        id: "brief",
        text: "I'll be quick - just one thought to consider.",
        tags: ["respectful", "brief"],
        interestChange: 3,
        effectiveWith: ["neutral", "distracted"],
        ineffectiveWith: []
    },
    pushy: {
        id: "pushy",
        text: "You really need to hear this - your soul depends on it!",
        tags: ["pushy", "hellfire"],
        interestChange: -8,
        effectiveWith: [],
        ineffectiveWith: ["skeptic", "cynic", "intellectual", "hostile", "neutral"]
    },
    leave: {
        id: "leave",
        text: "I'll leave you to think about it. Have a blessed day.",
        tags: ["polite_exit"],
        interestChange: 0,
        isExit: true
    }
};

// --- UTILITY FUNCTIONS ---
const randomChoice = (arr) => arr[Math.floor(Math.random() * arr.length)];
const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const generateName = () => `${randomChoice(FIRST_NAMES)} ${randomChoice(LAST_NAMES)}`;
const generateStreetName = () => `${randomChoice(STREET_NAMES)} ${randomChoice(STREET_SUFFIXES)}`;

// --- CONVERSATION ENGINE ---
class ConversationEngine {
    constructor(npc, preacher) {
        this.npc = npc;
        this.preacher = preacher;
        this.turn = 0;
        this.interest = this.calculateStartingInterest();
        this.lastObjection = null;
        this.usedResponses = new Set();
    }

    calculateStartingInterest() {
        let interest = 0;

        // Mood modifiers
        const moodModifiers = {
            receptive: 10,
            grumpy: -10,
            curious: 5,
            distracted: -5,
            neutral: 0
        };
        interest += moodModifiers[this.npc.mood] || 0;

        // Preacher personality bonus
        const bonus = this.preacher.personalityBonus[this.npc.personality];
        if (bonus) {
            interest += Math.floor(bonus * 50);
        }

        // Resistant penalty
        if (this.npc.resistant) {
            interest -= 25;
        }

        return interest;
    }

    getRelevantOpeners() {
        // Filter openers based on NPC personality and mood
        return OPENERS.filter(opener => {
            // Always include at least friendly and direct
            if (opener.id === "friendly" || opener.id === "direct") return true;

            // Check if effective with this personality/mood
            const isEffective = opener.effectiveWith?.includes(this.npc.personality) ||
                               opener.effectiveWith?.includes(this.npc.mood);
            const isIneffective = opener.ineffectiveWith?.includes(this.npc.personality) ||
                                 opener.ineffectiveWith?.includes(this.npc.mood);

            // Show if effective or not explicitly ineffective
            return isEffective || !isIneffective;
        }).slice(0, 4); // Limit to 4 openers
    }

    selectObjection() {
        // Weighted selection based on NPC personality and mood
        const weights = {};
        let totalWeight = 0;

        for (const [key, objection] of Object.entries(OBJECTIONS)) {
            let weight = objection.weights[this.npc.personality] || 1;
            weight += objection.weights[this.npc.mood] || 0;

            // Reduce weight for curious objection if interest is low
            if (key === "curious" && this.interest < 10) {
                weight *= 0.3;
            }

            // Increase weight for curious objection if interest is high
            if (key === "curious" && this.interest >= 20) {
                weight *= 2;
            }

            weights[key] = weight;
            totalWeight += weight;
        }

        // Weighted random selection
        let roll = Math.random() * totalWeight;
        for (const [key, weight] of Object.entries(weights)) {
            roll -= weight;
            if (roll <= 0) {
                this.lastObjection = OBJECTIONS[key];
                return OBJECTIONS[key];
            }
        }

        this.lastObjection = OBJECTIONS.not_interested;
        return OBJECTIONS.not_interested;
    }

    getRelevantResponses() {
        const responses = [];

        // If we have a last objection, prioritize counter-responses
        if (this.lastObjection?.counterWith) {
            for (const counterId of this.lastObjection.counterWith) {
                if (RESPONSES[counterId] && !this.usedResponses.has(counterId)) {
                    responses.push(RESPONSES[counterId]);
                }
            }
        }

        // Add other contextually appropriate responses
        for (const [key, response] of Object.entries(RESPONSES)) {
            if (responses.includes(response)) continue;
            if (this.usedResponses.has(key)) continue;
            if (response.isExit) continue;

            const isEffective = response.effectiveWith?.includes(this.npc.personality);
            const isIneffective = response.ineffectiveWith?.includes(this.npc.personality);

            if (isEffective) {
                responses.push(response);
            } else if (!isIneffective && responses.length < 4) {
                responses.push(response);
            }
        }

        // Always include leave option
        responses.push(RESPONSES.leave);

        // Limit to 4 options max (plus leave)
        return responses.slice(0, 5);
    }

    applyOpener(opener) {
        this.turn++;
        let change = opener.baseInterest;

        // Bonus/penalty based on effectiveness
        if (opener.effectiveWith?.includes(this.npc.personality)) {
            change += 3;
        }
        if (opener.ineffectiveWith?.includes(this.npc.personality)) {
            change -= 3;
        }

        this.interest += change;
        return change;
    }

    applyResponse(response) {
        this.turn++;
        this.usedResponses.add(response.id);

        let change = response.interestChange;

        // Effectiveness modifiers
        if (response.effectiveWith?.includes(this.npc.personality)) {
            change += 3;
        }
        if (response.ineffectiveWith?.includes(this.npc.personality)) {
            change -= 3;
        }

        // Preacher conversion bonus
        change += Math.floor(change * this.preacher.conversionBonus);

        this.interest += change;
        return change;
    }

    isConverted() {
        return this.interest >= CONFIG.CONVERSION_THRESHOLD;
    }

    isRejected() {
        return this.interest <= CONFIG.REJECTION_THRESHOLD;
    }

    isMaxTurns() {
        return this.turn >= CONFIG.MAX_CONVERSATION_TURNS;
    }

    getInterestDescription() {
        if (this.interest >= 40) return "They're very interested!";
        if (this.interest >= 20) return "They seem open to listening.";
        if (this.interest >= 0) return "They're listening politely.";
        if (this.interest >= -15) return "They seem uncertain.";
        return "They look like they want to leave.";
    }
}

// --- WORLD GENERATOR ---
class WorldGenerator {
    static generateNPC() {
        return {
            name: generateName(),
            personality: randomChoice(PERSONALITIES),
            mood: randomChoice(MOODS),
            converted: false,
            resistant: Math.random() < randomInt(20, 40) / 100 // 20-40% chance
        };
    }

    static generateLocation(type) {
        const npcs = [];
        let npcCount;
        if (type === "house") {
            npcCount = randomInt(1, 5);
        } else if (type === "store") {
            npcCount = randomInt(1, 3);
        } else {
            npcCount = randomInt(1, 4); // church
        }

        for (let i = 0; i < npcCount; i++) {
            npcs.push(this.generateNPC());
        }

        let name;
        if (type === "house") {
            name = `${randomInt(100, 9999)} ${generateStreetName()}`;
        } else if (type === "store") {
            name = randomChoice(["Quick Stop", "Corner Mart", "Save-A-Lot", "Mini Mart", "7-Eleven", "Dollar General", "Bodega", "Gas Station"]);
        } else if (type === "church") {
            name = `${randomChoice(["First", "New", "Grace", "Faith", "Mount", "Holy", "Saint"])} ${randomChoice(["Baptist", "Methodist", "Community", "Pentecostal", "Catholic", "Lutheran"])} Church`;
        }

        return { type, name, npcs };
    }

    static generateStreet() {
        const locations = [];
        const count = randomInt(2, 6);
        for (let i = 0; i < count; i++) {
            const roll = Math.random();
            let type = "house";
            if (roll > 0.92) type = "church";
            else if (roll > 0.82) type = "store";
            locations.push(this.generateLocation(type));
        }
        return { name: generateStreetName(), locations };
    }

    static generateNeighborhood() {
        const streets = [];
        const count = randomInt(2, 5);
        for (let i = 0; i < count; i++) {
            streets.push(this.generateStreet());
        }
        const suffixes = ["Heights", "Park", "Gardens", "District", "Village", "Estates", "Commons", "Grove"];
        return { name: `${randomChoice(STREET_NAMES)} ${randomChoice(suffixes)}`, streets };
    }

    static generateTown() {
        const neighborhoods = [];
        const count = randomInt(2, 4);
        for (let i = 0; i < count; i++) {
            neighborhoods.push(this.generateNeighborhood());
        }
        const suffixes = ["ville", "town", "burg", "field", "springs", "dale", "wood", "port"];
        return { name: `${randomChoice(STREET_NAMES)}${randomChoice(suffixes)}`, neighborhoods };
    }

    static generateCounty() {
        const towns = [];
        const count = randomInt(2, 5);
        for (let i = 0; i < count; i++) {
            towns.push(this.generateTown());
        }
        return { name: `${randomChoice(LAST_NAMES)} County`, towns };
    }
}

// --- UI CLASS ---
class UI {
    constructor() {
        this.output = document.getElementById("output");
        this.choices = document.getElementById("choices");
    }

    clear() {
        this.output.innerHTML = "";
        this.choices.innerHTML = "";
    }

    clearChoices() {
        this.choices.innerHTML = "";
    }

    print(text, className = "narrator") {
        const p = document.createElement("p");
        p.className = className;
        p.innerHTML = text;
        this.output.appendChild(p);
        this.output.scrollTop = this.output.scrollHeight;
    }

    heading(text) { this.print(text, "heading"); }
    speech(text) { this.print(`"${text}"`, "npc-speech"); }
    success(text) { this.print(text, "success"); }
    failure(text) { this.print(text, "failure"); }
    thought(text) { this.print(`* ${text} *`, "thought"); }

    addChoice(text, callback, className = "choice-btn") {
        const btn = document.createElement("button");
        btn.className = className;
        btn.textContent = text;
        btn.onclick = callback;
        this.choices.appendChild(btn);
    }

    addBackChoice(text, callback) {
        this.addChoice(text, callback, "choice-btn back-btn");
    }

    showInterestBar(interest) {
        const pct = Math.max(0, Math.min(100, interest + 50));
        const filled = Math.floor(pct / 5);
        this.print(`Interest: [${"=".repeat(filled)}${"-".repeat(20 - filled)}]`);
    }

    updateStatus(state) {
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
}

// --- GAME CLASS ---
class Game {
    constructor() {
        this.ui = new UI();
        this.state = this.createInitialState();
        this.conversation = null;
    }

    createInitialState() {
        return {
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
            currentNPC: null
        };
    }

    start() {
        this.ui.updateStatus(this.state);
        this.showWelcome();
    }

    showWelcome() {
        this.ui.clear();
        this.state.phase = "welcome";

        this.ui.heading("PREACHING THE TRUTH");
        this.ui.print("<i>Dedicated to Monica Huertas</i>");
        this.ui.print("");
        this.ui.print("In this game, you play as a preacher for a chosen religion.");
        this.ui.print("Your goal is to win as many souls as you can by going door-to-door and preaching your faith.");
        this.ui.print("");
        this.ui.print("Each day you will encounter various personalities. Some are seekers open to the truth. Others are skeptics who need logical arguments. Still others are lonely souls who need community.");
        this.ui.print("");
        this.ui.print("<b>The key to success:</b> Read each person and choose your approach wisely. Not every approach works with every personality.");
        this.ui.print("");

        this.ui.addChoice("Begin Game", () => this.showPreacherSelect());
    }

    showPreacherSelect() {
        this.ui.clear();
        this.state.phase = "preacher_select";

        this.ui.heading("Choose Your Preacher");
        this.ui.print("Each preacher has unique strengths and weaknesses.");
        this.ui.print("");

        PREACHERS.forEach((p) => {
            this.ui.print(`<b>${p.name}</b> - ${p.description}`);
            this.ui.print(`<i>Special: ${p.special}</i>`);
            this.ui.print("");
        });

        PREACHERS.forEach((p) => {
            this.ui.addChoice(p.name, () => this.selectPreacher(p));
        });

        this.ui.addChoice("Custom Character", () => {
            const name = prompt("Enter your preacher's name:");
            if (name) {
                this.selectPreacher({
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

    selectPreacher(preacher) {
        this.state.preacher = preacher;
        this.state.money = 20 + preacher.moneyBonus;
        this.ui.updateStatus(this.state);
        this.showReligionSelect();
    }

    showReligionSelect() {
        this.ui.clear();
        this.state.phase = "religion_select";

        this.ui.heading("Choose Your Religion");
        this.ui.print(`You are ${this.state.preacher.name}.`);
        this.ui.print(this.state.preacher.special);
        this.ui.print("");

        RELIGIONS.forEach((r) => {
            this.ui.addChoice(r, () => this.selectReligion(r));
        });
    }

    selectReligion(religion) {
        this.state.religion = religion;
        this.state.county = WorldGenerator.generateCounty();
        this.ui.updateStatus(this.state);
        this.startDay();
    }

    startDay() {
        this.state.hunger = 0;
        this.state.dailyScore = 0;
        this.state.currentTown = null;
        this.state.currentNeighborhood = null;
        this.state.currentStreet = null;
        this.state.currentLocation = null;

        this.ui.clear();

        this.ui.heading(`Day ${this.state.day + 1} - ${DAYS[this.state.day % 7]}`);
        this.ui.print("You wake up ready to spread the word.");

        if (this.state.day % 7 === 0) {
            const offering = randomInt(5, 15);
            this.state.money += offering;
            this.ui.success(`It's Sunday! You receive $${offering} from the offering.`);
        }

        this.ui.print("");
        this.ui.updateStatus(this.state);

        this.ui.addChoice("Head out to preach", () => this.showTownSelect());
    }

    showTownSelect() {
        this.ui.clear();

        this.ui.heading(this.state.county.name);
        this.ui.print("Choose a town to visit:");
        this.ui.print("");

        this.state.county.towns.forEach((town) => {
            this.ui.addChoice(`${town.name} (${town.neighborhoods.length} neighborhoods)`, () => {
                this.state.currentTown = town;
                this.ui.updateStatus(this.state);
                this.showNeighborhoodSelect();
            });
        });
    }

    showNeighborhoodSelect() {
        this.ui.clear();

        this.ui.heading(this.state.currentTown.name);
        this.ui.print("Choose a neighborhood:");
        this.ui.print("");

        this.state.currentTown.neighborhoods.forEach((n) => {
            this.ui.addChoice(`${n.name} (${n.streets.length} streets)`, () => {
                this.state.currentNeighborhood = n;
                this.ui.updateStatus(this.state);
                this.showStreetSelect();
            });
        });

        this.ui.addBackChoice("0. Back to town selection", () => {
            this.state.currentTown = null;
            this.ui.updateStatus(this.state);
            this.showTownSelect();
        });
    }

    showStreetSelect() {
        this.ui.clear();

        this.ui.heading(this.state.currentNeighborhood.name);
        this.ui.print("Choose a street:");
        this.ui.print("");

        this.state.currentNeighborhood.streets.forEach((s) => {
            this.ui.addChoice(`${s.name} (${s.locations.length} locations)`, () => {
                this.state.currentStreet = s;
                this.ui.updateStatus(this.state);
                this.showLocationSelect();
            });
        });

        this.ui.addBackChoice("0. Back to neighborhood selection", () => {
            this.state.currentNeighborhood = null;
            this.ui.updateStatus(this.state);
            this.showNeighborhoodSelect();
        });
    }

    showLocationSelect() {
        this.ui.clear();

        this.ui.heading(this.state.currentStreet.name);
        this.ui.print("Choose a location:");
        this.ui.print("");

        this.state.currentStreet.locations.forEach((loc) => {
            const icon = loc.type === "house" ? "House" : loc.type === "store" ? "Store" : "Church";
            const status = loc.npcs.every(n => n.converted) ? " (all converted)" : "";
            this.ui.addChoice(`[${icon}] ${loc.name}${status}`, () => {
                this.state.currentLocation = loc;
                this.handleLocation();
            });
        });

        this.ui.addBackChoice("0. Back to street selection", () => {
            this.state.currentStreet = null;
            this.ui.updateStatus(this.state);
            this.showStreetSelect();
        });
    }

    handleLocation() {
        this.ui.clear();
        const loc = this.state.currentLocation;
        this.ui.heading(loc.name);

        if (loc.type === "store") {
            this.handleStore();
        } else if (loc.type === "church") {
            this.handleChurch();
        } else {
            this.handleHouse();
        }
    }

    handleStore() {
        this.ui.print("You enter the store.");
        this.ui.print("");

        const items = [
            { name: "Candy Bar", price: 2, hunger: -10 },
            { name: "Sandwich", price: 5, hunger: -20 },
            { name: "Hot Meal", price: 8, hunger: -35 }
        ];

        items.forEach((item) => {
            const affordable = this.state.money >= item.price ? "" : " (can't afford)";
            this.ui.addChoice(`${item.name} - $${item.price} (${item.hunger} hunger)${affordable}`, () => {
                if (this.state.money >= item.price) {
                    this.state.money -= item.price;
                    this.state.hunger = Math.max(0, this.state.hunger + item.hunger);
                    this.ui.success(`You bought ${item.name} and ate it.`);
                    this.ui.updateStatus(this.state);
                } else {
                    this.ui.failure("You can't afford that.");
                }
            });
        });

        this.ui.addBackChoice("0. Leave store", () => this.showNextAction());
    }

    handleChurch() {
        const friendly = Math.random() > 0.3;

        if (friendly) {
            this.ui.success("The congregation welcomes you warmly!");
            this.ui.print("Your spirits are lifted.");
        } else {
            this.ui.failure("This church doesn't appreciate your denomination.");
            this.ui.print("You're asked to leave.");
            this.state.hunger = Math.min(100, this.state.hunger + 10);
            this.ui.updateStatus(this.state);
        }

        this.ui.addChoice("Continue", () => this.showNextAction());
    }

    handleHouse() {
        const unconverted = this.state.currentLocation.npcs.filter(n => !n.converted);

        if (unconverted.length === 0) {
            this.ui.print("Everyone here has already been converted.");
            this.ui.addChoice("Continue", () => this.showNextAction());
            return;
        }

        this.ui.print(`You see ${unconverted.length} person${unconverted.length > 1 ? 's' : ''} here.`);
        this.ui.print("");

        unconverted.forEach((npc) => {
            const hint = npc.resistant ? " [Resistant]" : "";
            this.ui.addChoice(`Talk to ${npc.name}${hint}`, () => this.startConversation(npc));
        });

        this.ui.addBackChoice("0. Move on", () => this.showNextAction());
    }

    startConversation(npc) {
        this.state.currentNPC = npc;
        this.conversation = new ConversationEngine(npc, this.state.preacher);

        this.ui.clear();
        this.ui.heading(`Talking with ${npc.name}`);
        this.ui.showInterestBar(this.conversation.interest);
        this.ui.print("");

        // Show personality hint
        const moodHints = {
            neutral: "They regard you calmly.",
            receptive: "They seem open to talking.",
            grumpy: "They look annoyed.",
            distracted: "They seem distracted.",
            curious: "They look curious."
        };

        const personalityHints = {
            skeptic: "They have a questioning look in their eyes.",
            seeker: "Something in their expression suggests they're searching for something.",
            lonely: "They seem like they could use someone to talk to.",
            intellectual: "They carry themselves with an academic air.",
            cynic: "Their expression is guarded and distrustful.",
            hostile: "They don't seem pleased to see you."
        };

        this.ui.print(moodHints[npc.mood] || "They wait for you to speak.");
        if (npc.personality !== "neutral") {
            this.ui.thought(personalityHints[npc.personality] || "");
        }
        this.ui.print("");

        this.showOpenerChoices();
    }

    showOpenerChoices() {
        this.ui.print("How do you want to start?");
        this.ui.print("");

        const openers = this.conversation.getRelevantOpeners();
        openers.forEach((opener) => {
            this.ui.addChoice(`"${opener.text}"`, () => this.useOpener(opener));
        });
    }

    useOpener(opener) {
        const change = this.conversation.applyOpener(opener);

        this.ui.clear();
        this.ui.heading(`Talking with ${this.state.currentNPC.name}`);
        this.ui.showInterestBar(this.conversation.interest);
        this.ui.print("");
        this.ui.speech(opener.text);
        this.ui.print("");

        // Show reaction
        if (change > 5) {
            this.ui.print("They seem interested in what you have to say.");
        } else if (change > 0) {
            this.ui.print("They're listening.");
        } else if (change < -3) {
            this.ui.print("That approach didn't land well.");
        }

        if (this.conversation.isConverted()) {
            this.endConversation(true);
        } else if (this.conversation.isRejected()) {
            this.endConversation(false);
        } else {
            this.showObjection();
        }
    }

    showObjection() {
        const objection = this.conversation.selectObjection();

        this.ui.print("");
        this.ui.speech(objection.text);
        this.ui.print("");

        this.showResponseChoices();
    }

    showResponseChoices() {
        this.ui.print("How do you respond?");
        this.ui.print("");

        const responses = this.conversation.getRelevantResponses();
        responses.forEach((resp) => {
            this.ui.addChoice(`"${resp.text}"`, () => this.useResponse(resp));
        });
    }

    useResponse(response) {
        const change = this.conversation.applyResponse(response);

        this.ui.clear();
        this.ui.heading(`Talking with ${this.state.currentNPC.name}`);
        this.ui.showInterestBar(this.conversation.interest);
        this.ui.print("");
        this.ui.speech(response.text);
        this.ui.print("");

        if (response.isExit) {
            this.ui.print("You part ways politely.");
            this.applyHunger();
            this.ui.addChoice("Continue", () => this.showNextAction());
            return;
        }

        // Show reaction based on effectiveness
        if (change > 5) {
            this.ui.print("That really resonated with them.");
        } else if (change > 0) {
            this.ui.print("They seem more receptive.");
        } else if (change < -3) {
            this.ui.print("They look uncomfortable with that approach.");
        } else {
            this.ui.print(this.conversation.getInterestDescription());
        }

        if (this.conversation.isConverted()) {
            this.endConversation(true);
        } else if (this.conversation.isRejected() || this.conversation.isMaxTurns()) {
            this.endConversation(false);
        } else {
            this.showObjection();
        }
    }

    endConversation(success) {
        this.applyHunger();
        this.ui.print("");

        if (success) {
            this.state.currentNPC.converted = true;
            this.state.score++;
            this.state.dailyScore++;

            this.ui.success("SUCCESS! They want to learn more about your faith!");

            if (Math.random() < CONFIG.DONATION_CHANCE) {
                const donation = randomInt(CONFIG.DONATION_MIN, CONFIG.DONATION_MAX);
                this.state.money += donation;
                this.ui.print(`They donate $${donation} to your ministry!`);
            }
        } else {
            if (this.conversation.isRejected()) {
                this.ui.failure("They've had enough and close the door.");
            } else {
                this.ui.print("They politely end the conversation. Maybe another time.");
            }
        }

        this.ui.updateStatus(this.state);

        if (this.state.hunger >= 100) {
            this.ui.addChoice("End Day", () => this.endDay());
        } else {
            this.ui.addChoice("Continue", () => this.handleLocation());
        }
    }

    applyHunger() {
        const amount = Math.floor(CONFIG.BASE_HUNGER_PER_CONVERSATION * this.state.preacher.hungerRate);
        this.state.hunger = Math.min(100, this.state.hunger + amount);
        this.ui.updateStatus(this.state);
    }

    showNextAction() {
        if (this.state.hunger >= 100) {
            this.endDay();
            return;
        }

        this.ui.clear();
        this.ui.print("What would you like to do?");
        this.ui.print("");

        this.ui.addChoice("Choose another location on this street", () => this.showLocationSelect());
        this.ui.addChoice("Go to a different street", () => {
            this.state.currentStreet = null;
            this.showStreetSelect();
        });
        this.ui.addChoice("Go to a different neighborhood", () => {
            this.state.currentStreet = null;
            this.state.currentNeighborhood = null;
            this.showNeighborhoodSelect();
        });
        this.ui.addChoice("Go to a different town", () => {
            this.state.currentStreet = null;
            this.state.currentNeighborhood = null;
            this.state.currentTown = null;
            this.showTownSelect();
        });
    }

    endDay() {
        this.ui.clear();

        this.ui.heading("Day's End");
        this.ui.print("You're too tired and hungry to continue.");
        this.ui.print("");
        this.ui.print(`Souls won today: ${this.state.dailyScore}`);
        this.ui.print(`Total souls: ${this.state.score}`);
        this.ui.print(`Money: $${this.state.money}`);
        this.ui.print("");

        this.state.day++;

        if (this.state.day >= CONFIG.GAME_LENGTH_DAYS) {
            this.endGame();
        } else {
            this.ui.addChoice("Start Next Day", () => this.startDay());
        }
    }

    endGame() {
        this.ui.heading("Your Ministry Has Ended");
        this.ui.print("");
        this.ui.print(`In ${CONFIG.GAME_LENGTH_DAYS} days, you won ${this.state.score} souls to the faith!`);
        this.ui.print("");

        if (this.state.score >= 20) {
            this.ui.success("Amazing! You are a true messenger of the faith!");
        } else if (this.state.score >= 10) {
            this.ui.print("A respectable ministry. The faithful are grateful.");
        } else if (this.state.score >= 5) {
            this.ui.print("A humble effort. Every soul counts.");
        } else {
            this.ui.print("The path of faith is not easy. Keep trying.");
        }

        this.ui.print("");
        this.ui.addChoice("Play Again", () => {
            this.state = this.createInitialState();
            this.ui.updateStatus(this.state);
            this.showWelcome();
        });
    }
}

// --- START GAME ---
const game = new Game();
game.start();
