"""Procedural location descriptions for 1990s suburban America.

Authored by Rowan Valle; Executed by Claude Code.

Descriptions are generated at world creation using seeded RNG,
so they persist throughout the playthrough. Each description is
composed from combinable elements (exterior + detail + atmosphere).
"""
from __future__ import annotations

import random

# =============================================================================
# HOUSE DESCRIPTIONS
# =============================================================================

HOUSE_EXTERIORS = [
    "A modest ranch-style home with aluminum siding.",
    "A two-story colonial with peeling white paint.",
    "A small bungalow behind a chain-link fence.",
    "A brick split-level with a two-car garage.",
    "A Cape Cod with green shutters and a screen door.",
    "A faded yellow duplex with mismatched curtains.",
    "A tidy little house with flower boxes in the windows.",
    "A run-down Victorian divided into apartments.",
    "A trailer home with a wooden porch addition.",
    "A beige ranch with a basketball hoop over the garage.",
    "A narrow shotgun house with a sagging roof.",
    "A white clapboard house with a wraparound porch.",
    "A stucco house with terracotta trim and a dead lawn.",
    "A prefab home with vinyl siding and new gutters.",
    "A weathered farmhouse at the end of a long driveway.",
    "A squat concrete-block house painted pastel pink.",
    "A raised ranch with wood paneling visible through the windows.",
    "A saltbox-style home with a crooked mailbox.",
    "A large house with too many additions bolted on over the years.",
    "A modest A-frame with a patchy gravel yard.",
]

HOUSE_DETAILS = [
    "A faded American flag hangs from the porch.",
    "Christmas lights are still up from last year.",
    "A Big Wheel sits overturned in the driveway.",
    "The mailbox is stuffed with catalogs.",
    "A 'Beware of Dog' sign is zip-tied to the fence.",
    "A garden gnome stands guard by the front steps.",
    "Someone left a sprinkler running on the brown lawn.",
    "A rusted pickup truck sits on blocks in the yard.",
    "Wind chimes tinkle from the porch eaves.",
    "A 'Bush/Quayle '92' bumper sticker peels on the car out front.",
    "Kids' bikes are piled against the garage door.",
    "A satellite dish the size of a hot tub dominates the yard.",
    "The house number is hand-painted on the curb.",
    "A welcome mat reads 'Go Away' in cheerful letters.",
    "Plastic flamingos stand in formation on the lawn.",
    "A tire swing hangs from the oak tree.",
    "The driveway is cracked and dandelions push through.",
    "A 'Protected by Smith & Wesson' sticker on the door.",
    "An old couch sits on the porch, sun-bleached and sagging.",
    "A ceramic Virgin Mary stands in a half-buried bathtub shrine.",
    "The screen door is patched with duct tape.",
    "A Dodge Caravan with a 'Baby on Board' sign in the driveway.",
    "A cat watches you from the windowsill.",
    "The lawn is immaculate. Someone here takes pride.",
    "A child's drawing is taped to the storm door.",
]

HOUSE_ATMOSPHERES = [
    "The curtains twitch as you approach.",
    "A dog barks somewhere inside.",
    "The TV flickers blue through the front window.",
    "The smell of something cooking drifts out.",
    "A radio plays country music from the backyard.",
    "The house is quiet. Almost too quiet.",
    "You hear kids arguing through the screen door.",
    "Someone peeks through the blinds, then lets them fall.",
    "The porch light is on, even in daylight.",
    "A ceiling fan spins lazily on the porch.",
    "You can hear a soap opera through the open window.",
    "The doorbell is broken. You'll have to knock.",
    "Cigarette smoke curls from a cracked window.",
    "A lawn mower idles in the back. Someone's home.",
    "The house smells like fresh laundry and Pine-Sol.",
    "A baby cries somewhere deep in the house.",
    "The screen door creaks in the breeze.",
    "You hear a vacuum cleaner running inside.",
    "The house is dark. Shades drawn against the heat.",
    "A wind-up music box plays faintly from an upstairs window.",
]

# =============================================================================
# STORE DESCRIPTIONS
# =============================================================================

STORE_EXTERIORS = [
    "Fluorescent lights buzz behind smudged glass doors.",
    "A hand-painted OPEN sign hangs crooked in the window.",
    "A cramped storefront wedged between a laundromat and a barber.",
    "A concrete-block building with a gravel parking lot.",
    "An old gas station converted into a convenience store.",
    "A strip mall unit with sun-faded awnings.",
    "A family-run shop with hand-lettered hours on the door.",
    "A corner store with bars on the windows and a neon beer sign.",
    "A tidy little market with a bell above the door.",
    "A prefab building with a massive ice machine out front.",
]

STORE_DETAILS = [
    "Cigarette ads plaster the windows.",
    "A bulletin board by the entrance is covered in lost-pet flyers.",
    "A payphone by the entrance, receiver dangling.",
    "Stacks of firewood wrapped in plastic sit by the door.",
    "A handwritten sign: 'WE RESERVE THE RIGHT TO REFUSE SERVICE.'",
    "Lottery ticket displays fill the counter.",
    "A rotating hot dog machine turns in the window.",
    "Newspapers in a wire rack by the door. Today's headline is grim.",
    "A gumball machine with a broken crank guards the entrance.",
    "Shopping carts with wobbly wheels line the sidewalk.",
    "A 'Help Wanted' sign has been in the window so long it's yellowed.",
    "An ATM with a $2.50 fee blinks by the entrance.",
]

STORE_ATMOSPHERES = [
    "The AC hits you as you step inside.",
    "Country music plays from a tinny radio behind the counter.",
    "The cashier eyes you from behind a plexiglass partition.",
    "The floor is sticky near the soda fountain.",
    "It smells like beef jerky and floor cleaner.",
    "A ceiling fan wobbles dangerously overhead.",
    "The fluorescent lights give everything a greenish cast.",
    "Two old men argue about baseball near the coffee pot.",
    "A teenager flips through a magazine, ignoring everything.",
    "The store is empty. Just you and the hum of the coolers.",
]

# =============================================================================
# CHURCH DESCRIPTIONS
# =============================================================================

CHURCH_EXTERIORS = [
    "A white clapboard church with a modest wooden steeple.",
    "A large brick building with tall stained glass windows.",
    "A converted storefront with a hand-lettered sign above the door.",
    "A stone chapel with ivy creeping up the walls.",
    "A modern building with a glass atrium and a parking lot for 200.",
    "A small wooden church with a tin roof and a gravel lot.",
    "A grand old building with columns and a bell tower.",
    "A prefab metal building with a cross bolted to the front.",
    "An old schoolhouse repurposed as a church. The bell still rings.",
    "A sprawling campus with multiple buildings and a lighted sign.",
    "A tiny chapel barely bigger than a house, paint peeling.",
    "A limestone church with gargoyles and a rose window.",
]

CHURCH_DETAILS = [
    "The marquee reads: 'FREE COFFEE, EXPENSIVE SALVATION.'",
    "A statue of Mary stands in a small garden out front.",
    "The parking lot is freshly paved. Prosperity.",
    "A marquee: 'SUNDAY SERMON: ARE YOU READY?'",
    "A chain-link fence surrounds a modest playground.",
    "The doors are propped open. All are welcome, apparently.",
    "A donation box sits by the entrance, padlocked.",
    "Someone left flowers at the base of the cross.",
    "A bumper sticker on the marquee: 'Honk if you love Jesus.'",
    "A cemetery stretches behind the building, ancient stones leaning.",
    "A bus with the church name painted on the side sits in the lot.",
    "The stained glass depicts the Last Supper in vivid color.",
    "A nativity scene sits out front, year-round.",
    "A sign: 'WEDNESDAY NIGHT BINGO - ALL WELCOME.'",
]

CHURCH_ATMOSPHERES = [
    "Hymns drift through the open doors.",
    "The building is silent. A crow sits on the cross.",
    "The organ is playing. Someone is practicing.",
    "You smell incense from the doorway.",
    "An old woman sweeps the front steps, humming.",
    "The bells chime the hour as you approach.",
    "Children's laughter comes from a Sunday school room.",
    "The air inside is cool and smells like polished wood.",
    "A pastor's voice echoes faintly from within.",
    "The church feels empty. The parking lot is deserted.",
    "A choir rehearsal spills beautiful noise into the street.",
    "Candles flicker through the windows in the dim interior.",
]

# =============================================================================
# LIBRARY DESCRIPTIONS
# =============================================================================

LIBRARY_EXTERIORS = [
    "A squat brick building with 'PUBLIC LIBRARY' carved above the door.",
    "A converted Victorian house with creaky wooden floors.",
    "A modern glass-and-steel building that looks out of place here.",
    "A Carnegie-era stone building with columns and wide steps.",
    "A single-story building with a flat roof and a book drop slot.",
    "A branch library in a strip mall, next to a dry cleaner.",
    "An old stone building with 'FREE TO ALL' engraved above the lintel.",
    "A cozy cottage-style building with window planters full of herbs.",
]

LIBRARY_DETAILS = [
    "A book drop slot is jammed open with returns.",
    "Children's drawings are taped to the windows.",
    "A poster advertises the summer reading program.",
    "A cart of FREE books sits outside, picked over.",
    "A 'Silence Please' sign hangs above the entrance.",
    "Flyers for a literacy program cover the bulletin board.",
    "A bronze plaque honors a local benefactor. The name is worn smooth.",
    "Someone chained their bike to the handicap ramp railing.",
    "A 'Friends of the Library' bake sale table sits empty by the door.",
    "A sign: 'INTERNET ACCESS - 30 MIN LIMIT.'",
]

LIBRARY_ATMOSPHERES = [
    "The smell of old paper hits you at the threshold.",
    "Someone left a coffee cup on the return cart.",
    "A librarian stamps books with metronomic precision.",
    "Two teenagers whisper urgently over a shared textbook.",
    "The air conditioning hums. It's ten degrees colder in here.",
    "An elderly man sleeps in a chair by the periodicals.",
    "A child sits cross-legged on the floor, lost in a picture book.",
    "The microfiche machine whirs in the reference section.",
    "It's quiet in a way that feels almost sacred.",
    "The water fountain makes a loud CLUNK every time someone uses it.",
]


# =============================================================================
# PARK DESCRIPTIONS
# =============================================================================

PARK_EXTERIORS = [
    "A grassy square with a few scattered picnic tables and a rusted grill.",
    "A small park with a wooden playground and a gravel jogging path.",
    "An open field with a gazebo and a war memorial at the center.",
    "A tree-lined park with benches along a cracked asphalt path.",
    "A dusty ball field with bleachers and a concession stand boarded shut.",
    "A well-kept park with a fountain that hasn't worked in years.",
    "A strip of green between two roads, barely big enough for a swing set.",
    "A wooded park with a creek running through it and a footbridge.",
    "A flat, shadeless park with a basketball court and a porta-john.",
    "A community garden borders one edge. Someone is growing tomatoes.",
]

PARK_DETAILS = [
    "A man feeds pigeons from a bench.",
    "Teenagers loiter near the basketball court.",
    "An old woman walks a tiny dog on a rhinestone leash.",
    "A father pushes his daughter on the swings.",
    "Someone left a Bible on a bench. It's waterlogged.",
    "A homeless man sleeps under a newspaper on a bench.",
    "Kids chase each other around the playground, screaming.",
    "A jogger circles the path, headphones in, ignoring everything.",
    "A sign reads: 'NO LOITERING.' Nobody reads it.",
    "A couple shares a sandwich on a blanket.",
    "Someone is practicing tai chi near the fountain.",
    "A handmade sign is stapled to a tree: 'MISSING DOG - REWARD.'",
]

PARK_ATMOSPHERES = [
    "The sun is warm. People are relaxed here.",
    "Sprinklers hiss across the grass, catching the light.",
    "The park smells like cut grass and charcoal.",
    "It's peaceful. A good place to talk to people.",
    "A breeze rustles the leaves. This feels like neutral ground.",
    "The ice cream truck's jingle echoes from a block away.",
    "Birds argue in the trees. Otherwise, it's calm.",
    "Ants have claimed the picnic table. You'll have to stand.",
    "The shade under the oaks is the only relief from the heat.",
    "A radio plays oldies from someone's boombox.",
]

# =============================================================================
# DINER DESCRIPTIONS
# =============================================================================

DINER_EXTERIORS = [
    "A chrome-sided diner with red vinyl booths visible through the windows.",
    "A squat brick building with a neon 'EAT' sign buzzing in the window.",
    "A converted railroad car with a hand-painted menu board outside.",
    "A roadside diner with a gravel lot full of pickup trucks.",
    "A family restaurant with gingham curtains and a pie case by the register.",
    "A greasy spoon with fogged windows and a bell above the door.",
    "A breakfast joint with a line out the door on weekends.",
    "A dingy little cafe with a counter and six stools.",
    "A pancake house with a cartoon chef on the sign.",
    "A truck stop diner with a rotating dessert case and free refills.",
]

DINER_DETAILS = [
    "The specials board reads: 'MEATLOAF $3.99. LIKE MAMA USED TO MAKE.'",
    "A tip jar by the register says 'COLLEGE FUND' in marker.",
    "Truckers' caps hang on pegs by the door.",
    "A jukebox in the corner plays Patsy Cline.",
    "The counter is worn smooth from a thousand elbows.",
    "Ketchup bottles sit on every table, pre-crusted.",
    "A wall of Polaroids shows regulars spanning decades.",
    "The daily paper is spread across the counter, sports section up.",
    "A sign behind the register: 'IN GOD WE TRUST. ALL OTHERS PAY CASH.'",
    "A coffee pot sits on the burner, thick and dark. It's been there since dawn.",
    "Kids' drawings are pinned to a corkboard by the bathrooms.",
    "A bell rings every time the kitchen window opens.",
]

DINER_ATMOSPHERES = [
    "The smell of bacon grease and fresh coffee fills the air.",
    "A waitress refills cups without asking. She knows everyone here.",
    "Two men in work boots argue about the Cowboys at the counter.",
    "The AC is broken. Ceiling fans spin at full speed.",
    "A group of teenagers shares a plate of fries and too much laughter.",
    "It's the kind of place where everyone knows your business.",
    "The cook yells 'ORDER UP!' and a plate slides across the window.",
    "An old man sits alone, reading the obituaries. He comes every day.",
    "The radio is tuned to a talk show. Someone is yelling about politics.",
    "Conversation lulls as you walk in. You're not a regular.",
]

# =============================================================================
# LAUNDROMAT DESCRIPTIONS
# =============================================================================

LAUNDROMAT_EXTERIORS = [
    "A long, narrow room with two rows of machines and a folding table.",
    "A bright laundromat with a row of plastic chairs bolted to the floor.",
    "A dingy wash-and-fold with flickering fluorescent lights.",
    "A clean, modern laundromat with a TV mounted in the corner.",
    "A basement-level laundromat you have to walk down steps to enter.",
    "A combined laundromat and dry cleaner with plastic-wrapped suits on a rack.",
    "A cramped space between a nail salon and a check-cashing place.",
    "A surprisingly cheerful laundromat with yellow walls and potted plants.",
]

LAUNDROMAT_DETAILS = [
    "A vending machine sells single-load detergent packets for 75 cents.",
    "A sign: 'NOT RESPONSIBLE FOR LOST ITEMS.' Someone lost a sock anyway.",
    "Magazines from 1993 sit in a wire rack. The covers are curled.",
    "A quarter-operated arcade game blinks in the corner. Ms. Pac-Man.",
    "Someone left a basket of clothes in machine #7. Again.",
    "A handwritten sign: 'PLEASE REMOVE CLOTHES PROMPTLY.'",
    "A lost-and-found box overflows with single socks and a child's shoe.",
    "The change machine is out of order. A handwritten note says 'SORRY.'",
    "Someone taped a 'FOR SALE' flyer for a used minivan to the wall.",
    "The dryers cost 25 cents for 8 minutes. Highway robbery.",
]

LAUNDROMAT_ATMOSPHERES = [
    "Machines tumble and hum. The heat is tropical.",
    "A woman reads a romance novel, waiting for the spin cycle.",
    "The smell of fabric softener is almost overwhelming.",
    "A young mother folds onesies while her toddler naps in a car seat.",
    "An old man watches his clothes spin like it's television.",
    "People are stuck here. They've got nowhere to be for the next hour.",
    "The rhythmic thump of unbalanced loads fills the room.",
    "Someone is on the payphone outside, voice rising.",
    "It's warm and damp. Condensation fogs the front window.",
    "A soap opera plays on the mounted TV. Nobody's watching.",
]

# =============================================================================
# COMMUNITY CENTER DESCRIPTIONS
# =============================================================================

COMMUNITY_CENTER_EXTERIORS = [
    "A flat-roofed cinderblock building with a basketball court out back.",
    "A converted school gymnasium with a hand-painted mural on the side.",
    "A prefab building with a bulletin board crammed with event flyers.",
    "A brick building with a flagpole and a marquee announcing events.",
    "An old VFW hall repurposed as a community space.",
    "A modern building with large windows and a wheelchair ramp.",
    "A church annex that doubles as the neighborhood meeting hall.",
    "A weathered wooden building with 'COMMUNITY CENTER' stenciled on the door.",
]

COMMUNITY_CENTER_DETAILS = [
    "A flyer announces: 'AA MEETING - TUESDAYS 7PM.'",
    "Folding chairs are stacked against the wall from last night's event.",
    "A trophy case displays Little League championships from the '80s.",
    "A sign-up sheet for a potluck dinner hangs on the door.",
    "Kids' artwork is displayed in the hallway. The theme was 'My Family.'",
    "A bake sale table is being set up near the entrance.",
    "The parking lot has a 'NO SKATEBOARDING' sign. Skid marks everywhere.",
    "A banner reads: 'NEIGHBORHOOD WATCH - KEEPING OUR STREETS SAFE.'",
    "Someone is setting up a table for voter registration.",
    "A bulletin board lists: tutoring, ESL classes, senior bingo, and yoga.",
]

COMMUNITY_CENTER_ATMOSPHERES = [
    "The building smells like floor wax and instant coffee.",
    "A group of seniors plays dominoes at a folding table.",
    "Kids run through the hall. Someone yells 'NO RUNNING!' from an office.",
    "A woman arranges donated canned goods into boxes.",
    "The echo of a basketball bouncing comes from the gym.",
    "It's the kind of place that runs on volunteers and stubbornness.",
    "A man in a polo shirt with a clipboard eyes you. He's in charge here.",
    "The fluorescent lights buzz. One flickers near the bathroom.",
    "Someone is photocopying flyers. The machine jams. They curse softly.",
    "Two women set up coffee and donuts for an evening meeting.",
]


def generate_park_description() -> str:
    """Generate a random park description."""
    exterior = random.choice(PARK_EXTERIORS)
    detail = random.choice(PARK_DETAILS)
    atmosphere = random.choice(PARK_ATMOSPHERES)
    return f"{exterior} {detail} {atmosphere}"


def generate_diner_description() -> str:
    """Generate a random diner description."""
    exterior = random.choice(DINER_EXTERIORS)
    detail = random.choice(DINER_DETAILS)
    atmosphere = random.choice(DINER_ATMOSPHERES)
    return f"{exterior} {detail} {atmosphere}"


def generate_laundromat_description() -> str:
    """Generate a random laundromat description."""
    exterior = random.choice(LAUNDROMAT_EXTERIORS)
    detail = random.choice(LAUNDROMAT_DETAILS)
    atmosphere = random.choice(LAUNDROMAT_ATMOSPHERES)
    return f"{exterior} {detail} {atmosphere}"


def generate_community_center_description() -> str:
    """Generate a random community center description."""
    exterior = random.choice(COMMUNITY_CENTER_EXTERIORS)
    detail = random.choice(COMMUNITY_CENTER_DETAILS)
    atmosphere = random.choice(COMMUNITY_CENTER_ATMOSPHERES)
    return f"{exterior} {detail} {atmosphere}"


def generate_house_description() -> str:
    """Generate a random house description from composable elements."""
    exterior = random.choice(HOUSE_EXTERIORS)
    detail = random.choice(HOUSE_DETAILS)
    atmosphere = random.choice(HOUSE_ATMOSPHERES)
    return f"{exterior} {detail} {atmosphere}"


def generate_store_description() -> str:
    """Generate a random store description."""
    exterior = random.choice(STORE_EXTERIORS)
    detail = random.choice(STORE_DETAILS)
    atmosphere = random.choice(STORE_ATMOSPHERES)
    return f"{exterior} {detail} {atmosphere}"


def generate_church_description() -> str:
    """Generate a random church description."""
    exterior = random.choice(CHURCH_EXTERIORS)
    detail = random.choice(CHURCH_DETAILS)
    atmosphere = random.choice(CHURCH_ATMOSPHERES)
    return f"{exterior} {detail} {atmosphere}"


def generate_library_description() -> str:
    """Generate a random library description."""
    exterior = random.choice(LIBRARY_EXTERIORS)
    detail = random.choice(LIBRARY_DETAILS)
    atmosphere = random.choice(LIBRARY_ATMOSPHERES)
    return f"{exterior} {detail} {atmosphere}"
