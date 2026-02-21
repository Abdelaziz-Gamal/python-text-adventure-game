import json
import time
import random

enemy = random.choice([
    "a mysterious hooded figure",
    "a tall pale man with glowing eyes",
    "a silent man holding a lantern",
    "a masked stranger covered in dust"])

cave_monster = random.choice([
    "a giant red-eyed monster",
    "a shadow creature with long claws",
    "a massive cave troll",
    "a distorted humanoid beast"])

forest_whisper = random.choice([
    "Suddenly, a soft voice whispers your name.",
    "Suddenly, you hear faint laughter between the trees.",
    "Suddenly, something moves quickly behind you.",
    "Suddenly, a cold breath touches your neck."])

monster_sound = random.choice([
    "You hear heavy breathing very close.",
    "Claws scrape against the rocks.",
    "The monster sniffs the air.",
    "Something growls right above you."])

camp_detail = random.choice([
    "You notice strange symbols carved on a tree.",
    "You see footprints that are not human.",
    "The wind carries a distant scream.",
    "You feel like someone was here moments ago."])

locations = [
    {"name": "a dark forest",
    "cave_desc": "To your left, vines cover the entrance of a shadowy cave.",
    "house_desc": "To your right, a wooden abandoned house stands silently."},

    {"name": "a foggy hill",
    "cave_desc": "To your left, a cave is carved into the rocky hillside.",
    "house_desc": "To your right, a small stone house overlooks the valley."},

    {"name": "a mysterious valley",
    "cave_desc": "To your left, a deep cave breathes cold air.",
    "house_desc": "To your right, an old broken house leans dangerously."}
]

def print_pause(text, sec):  # it makes a delay after every line
    print(text)
    time.sleep(sec)
    print("")

def load_account():
    try:
        with open("accounts.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_account(accounts):
    with open("accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)

def sign_in():
    accounts = load_account()
    print("=== Sign In ===")
    user = input("Username: ").lower()
    if user not in accounts:
        print("Username not found!\n")
        return None

    email = input("Email: ").lower()
    password = input("Password: ")
    if email == accounts[user]["email"] and password == accounts[user]["password"]:
        return user
    else:
        print("Wrong credentials!\n")
        return None

def sign_up():
    accounts = load_account()
    print("=== Sign Up ===")
    user = input("Choose username: ").lower()
    if user in accounts:
        print("Username already exists!\n")
        return None

    email = input("Email: ").lower()
    while True:
        password = input("Password: ")
        password_confirm = input("Confirm Password: ")
        if password == password_confirm:
            break
        print("Passwords do not match. Try again.\n")

    accounts[user] = {
        "email": email,
        "password": password,
        "highscore": 0}

    save_account(accounts)
    print_pause(f"Account created successfully! Welcome {user}!",1)

    return user

def delete_account(username):
    accounts = load_account()
    if username in accounts:
        while True:
            confirm = input(f"Are you sure you want to delete the account '{username}'? (yes/no): ")
            if confirm.lower() == "yes":
                del accounts[username]
                save_account(accounts)
                print(f"Account '{username}' deleted successfully!")
                return True

            elif confirm.lower() == "no":
                print("Account deletion canceled.")
                return False

            else:
                print("Wrong input. Please type 'yes' or 'no'")
    else:
        print("Username not found!")

    return False

def edit_account(username):
    accounts = load_account()
    if username not in accounts:
        print("Username not found!")
        return

    print("=== Edit Account ===")
    print("1) Change Email")
    print("2) Change Password")
    choice = input("Choose option (1 or 2): ")

    if choice == "1":
        new_email = input("Enter new email: ").lower()
        accounts[username]["email"] = new_email
        save_account(accounts)
        print("Email updated successfully!")

    elif choice == "2":
        while True:
            new_password = input("Enter new password: ")
            confirm_password = input("Confirm new password: ")

            if new_password == confirm_password:
                accounts[username]["password"] = new_password
                save_account(accounts)
                print("Password updated successfully!")
                break

            print("Passwords do not match. Try again.")
    else:
        print("Invalid choice!")

def player_choice():  # ask the player about the choice which he wants to make
    choice = input("Please enter your choice (1 or 2): ")
    while choice not in ["1", "2"]:
        print("invalid input!")
        choice = input("Please enter your choice (1 or 2): ")
    return choice

def win_or_lose(score):
    if score >= 21:
        return "Congratulations! You win!🏆🎉"
    else:
        return "GAME OVER! You lose!"
    
def end_game(score):
    print("Current score:", score)
    print(win_or_lose(score))
    print("")

def intro():
    accounts = load_account()
    while True:
        print("1) Sign In")
        print("2) Sign Up")
        choice = input("Choose (1 or 2): ")
        if choice == "1":
            username = sign_in()
            if username:
                while True:
                    print("What do you want to do?")
                    print("1) Start Game")
                    print("2) Edit Account")
                    print("3) Delete Account")
                    next_choice = input("Choose (1, 2 or 3): ")

                    if next_choice == "1":
                        print_pause(f"Welcome {username}!",1)
                        print_pause("I am really happy that you decided to try my game again", 2)

                        if accounts[username]["highscore"]< 50:
                            print_pause("Hope you get better score this time😂", 2)
                        print("Your Highest Score was:", accounts[username]["highscore"])
                        print("")
                        print_pause("The highest score you can get is 50", 2)
                        print_pause("As you know if you got less than 21 points you will lose", 2)
                        print_pause("your current score is 0 points", 2)
                        print_pause("hope you enjoy our game and come back again and again...Lets start!", 2)

                        return username  # proceed to main_game

                    elif next_choice == "2":
                        edit_account(username)

                    elif next_choice == "3":
                        delete_account(username)
                        username = None  # account deleted
                        break

                    else:
                        print("Invalid choice!\n")

                if username:  # account still exists
                    break

        elif choice == "2":
            username = sign_up()
            if username:
                print_pause("I am really happy that you decided to try my game", 2)
                print_pause("before we start..if you got less than 21 points you will lose", 2)
                print_pause("The highest score you can get is 50", 2)
                print_pause("You start with 0 points", 2)
                print_pause("hope you enjoy our game...Lets start!", 2)
                break
        else:
            print("Invalid choice!\n")
    return username

def start_game():
    place = random.choice(locations)
    print_pause(f"You find yourself standing in {place['name']}.", 2)
    print_pause(place["cave_desc"], 2)
    print_pause(place["house_desc"], 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to knock on the door of the house.", 2)
    print_pause("Enter 2 to enter the cave.", 1)

def knock_on_door():
    print_pause("You knock on the door of the house.", 2)
    print_pause(f"A {enemy} opens the door and invites you inside.", 3)
    print_pause("What would you like to do next?", 2)
    print_pause("Enter 1 to accept the invitation.", 2)
    print_pause("Enter 2 to decline and continue exploring outside.", 1)

def accept_invitation():
    print_pause("You accept the invitation and step inside the house.", 2)
    print_pause(f"The {enemy} leads you to a grand hall.", 3)
    print_pause("What would you like to do next?", 2)
    print_pause("Enter 1 to explore the hall.", 2)
    print_pause("Enter 2 to follow the figure to another room.", 1)

def hall_decision():
    print_pause("You walk deeper into the grand hall.", 2)
    print_pause("Dust covers the floor and strange symbols cover the walls.", 3)
    print_pause("In the center, you find an old chest and a huge ancient book.", 3)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to open the mysterious chest.", 2)
    print_pause("Enter 2 to read the ancient book.", 1)

def open_chest_decision():
    print_pause("You slowly open the ancient chest.", 2)
    print_pause("A strange golden light shines from inside.", 3)
    print_pause("Inside, you find a glowing crystal and a rusty key.", 2)
    print_pause("You feel powerful but also scared.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to take the crystal.", 2)
    print_pause("Enter 2 to take the key and leave quietly.", 1)

def take_crystal_ending():
    print_pause("You grab the glowing crystal.", 2)
    print_pause("Power flows through your body.", 2)
    print_pause("The house starts shaking violently.", 2)
    print_pause("A portal opens in front of you.", 2)
    print_pause("You jump inside and escape safely.", 2)
    print_pause("You discovered a secret power and survived.", 2)

def take_key_ending():
    print_pause("You take the rusty key and turn back.", 2)
    print_pause("Suddenly, the chest explodes.", 2)
    print_pause("Dark smoke fills the room.", 2)
    print_pause("You cannot breathe.", 2)
    print_pause("Everything goes black.", 2)
    print_pause("You were trapped by a curse.", 2)

def read_book_decision():
    print_pause("You open the ancient book carefully.", 2)
    print_pause("The pages start moving by themselves.", 3)
    print_pause("Strange words enter your mind.", 2)
    print_pause("You feel dizzy but wiser.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to continue reading.", 2)
    print_pause("Enter 2 to close the book immediately.", 1)

def continue_reading_ending():
    print_pause("You keep reading the strange words.", 2)
    print_pause("Your mind becomes clearer.", 2)
    print_pause("You understand the secrets of the house.", 2)
    print_pause("A hidden door opens.", 2)
    print_pause("You walk out safely with knowledge.", 2)
    print_pause("Wisdom saved you.", 2)

def close_book_ending():
    print_pause("You close the book quickly.", 2)
    print_pause("The room becomes silent.", 2)
    print_pause("Suddenly, shadows surround you.", 2)
    print_pause("They pull you into darkness.", 2)
    print_pause("You should NOT have interrupted the magic.", 2)

def follow_decision():
    print_pause(f"You follow the {enemy} quietly.", 2)
    print_pause("He enters a dark corridor and starts whispering strange words.", 3)
    print_pause("You feel something is not right.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to trust him and continue following.", 2)
    print_pause("Enter 2 to spy on him secretly.", 1)

def trust_him_decision():
    print_pause("You decide to trust the mysterious man.", 2)
    print_pause("He leads you to a hidden underground room.", 3)
    print_pause("You see strange machines working.", 2)
    print_pause("He tells you: 'This is our secret.'", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to help him.", 2)
    print_pause("Enter 2 to escape quietly.", 1)

def help_him_ending():
    print_pause("You pick up the tools and work with him.", 2)
    print_pause("The machine begins to hum and glow.", 2)
    print_pause("Suddenly, the room is filled with warm, golden light.", 2)
    print_pause("He looks at you and nods with kindness.", 2)
    print_pause("A secret door opens. You can see your home.", 2)
    print_pause("You are not a stranger anymore. You are a friend.", 2)

def escape_quietly_ending():
    print_pause("You walk on your toes. You are almost at the door.", 2)
    print_pause("CRACK! The old floor screams under your foot.", 2)
    print_pause("Everything stops. The man slowly turns his head.", 2)
    print_pause("His eyes are full of fire and hate.", 2)
    print_pause("You run for the door, but he is too fast.", 2)
    print_pause("He captures you. The world goes black.", 2)
    print_pause("Silence was your only hope, and you BROKE it.", 2)

def spy_him_decision():
    print_pause("You hide behind the walls and spy on him.", 2)
    print_pause("You hear him talking to dark shadows.", 3)
    print_pause("He seems dangerous.", 2)
    print_pause("You feel your heart beating fast.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to confront him.", 2)
    print_pause("Enter 2 to run away.", 1)

def confront_him_ending():
    print_pause("You walk up to him and shout.", 2)
    print_pause("He does not look afraid. He just smiles.", 2)
    print_pause("He snaps his fingers.", 2)
    print_pause("The walls begin to move. There is no way out.", 2)
    print_pause("Shadows grab your arms and pull you down.", 2)
    print_pause("His laugh is the last thing you ever hear.", 2)
    print_pause("You walked right into his spider web.", 2)

def run_away_ending():
    print_pause("You run as fast as you can.", 2)
    print_pause("All doors and windows are closed.", 2)
    print_pause("He finds you.", 2)
    print_pause("He locks you in a room for days.", 2)
    print_pause("You DIED from hunger.", 2)

def decline_the_invitation():
    print_pause("You decline the invitation and decide to explore outside.", 2)
    print_pause("As you walk further, you stumble upon a hidden path.", 2)
    print_pause("What would you like to do next?", 2)
    print_pause("Enter 1 to follow the hidden path.", 2)
    print_pause("Enter 2 to continue exploring the surrounding area.", 1)

def hidden_path_decision():
    print_pause("You walk through the hidden path carefully.", 2)
    print_pause("Soon, you reach a broken bridge over a deep valley.", 3)
    print_pause("Next to it, there are dangerous rocky cliffs.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to cross the old bridge.", 2)
    print_pause("Enter 2 to climb the rocky cliffs.", 1)

def cross_bridge_decision():
    print_pause("You step carefully onto the old bridge.", 2)
    print_pause("It shakes with every step.", 3)
    print_pause("Below you is a deep dark valley.", 2)
    print_pause("The wind becomes stronger.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to run fast.", 2)
    print_pause("Enter 2 to move slowly.", 1)

def run_fast_bridge_ending():
    print_pause("You start running fast.", 2)
    print_pause("The bridge shakes violently.", 2)
    print_pause("It breaks under your feet.", 2)
    print_pause("You fall into the valley.", 2)

def move_slowly_bridge_ending():
    print_pause("You take one small step at a time.", 2)
    print_pause("The bridge shakes. Your legs are shaking too.", 2)
    print_pause("You reach the other side. You are safe!", 2)
    print_pause("But your heart is too tired to beat.", 2)
    print_pause("The world turns grey. You fall into the ground.", 2)
    print_pause("You survived the bridge but not the journey.", 2)

def climb_rocks_decision():
    print_pause("You start climbing the dangerous rocks.", 2)
    print_pause("Sharp stones hurt your hands.", 3)
    print_pause("You almost slip several times.", 2)
    print_pause("But you see a path above.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to keep climbing.", 2)
    print_pause("Enter 2 to go back down.", 1)

def keep_climbing_ending():
    print_pause("You keep climbing despite the pain.", 2)
    print_pause("Your hands bleed.", 2)
    print_pause("Suddenly, a rock breaks.", 2)
    print_pause("You fall down.", 2)
    print_pause("One mistake was enough.", 2)

def go_back_down_ending():
    print_pause("You decide to go back down.", 2)
    print_pause("The ground is slippery.", 2)
    print_pause("You lose control.", 2)
    print_pause("You hit the rocks.", 2)
    print_pause("Retreat came too late.", 2)

def forest_decision():
    print_pause("You enter a dark and silent forest.", 2)
    print_pause("Strange glowing lights appear between the trees.", 3)
    print_pause("At the same time, you find a small place to build shelter.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to follow the glowing lights.", 2)
    print_pause("Enter 2 to build a shelter and rest.", 1)

def follow_lights_decision():
    print_pause("You follow the glowing beautiful lights.", 2)
    print_pause("They move deeper into the forest.", 3)
    print_pause("You feel like they are watching you.", 2)
    print_pause(forest_whisper, 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to follow faster.", 2)
    print_pause("Enter 2 to hide.", 1)

def follow_faster_ending():
    print_pause("The lights are so beautiful. You start to run.", 2)
    print_pause("They dance in the air, leading you deeper into the fog.", 2)
    print_pause("You reach out to touch one...", 2)
    print_pause("Suddenly, the ground vanishes under your feet.", 2)
    print_pause("You are falling into the cold, dark empty air.", 2)
    print_pause("The lights stop and watch you fall. They were laughing.", 2)
    print_pause("Beauty can be a deadly trap.", 2)

def hide_lights_ending():
    print_pause("You hide behind the trees.", 2)
    print_pause("But, the whispers get stronger.", 2)
    print_pause("You feel dizzy and strange powers inside you.", 2)
    print_pause("you collapse and no one is near to save you.", 2)

def build_shelter_decision():
    print_pause("You build a small shelter from branches.", 2)
    print_pause("A cold wind starts blowing.", 3)
    print_pause("You feel safer but very tired.", 2)
    print_pause("You hear footsteps nearby.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to investigate.", 2)
    print_pause("Enter 2 to stay hidden.", 1)

def investigate_shelter_ending():
    print_pause("You walk slowly toward the strange sound.", 2)
    print_pause("The light fades. It is very dark here.", 2)
    print_pause("Suddenly, many yellow eyes open in the shadows.", 2)
    print_pause("The creatures do not bark or growl. They just watch.", 2)
    print_pause("You try to run, but the exit is blocked.", 2)
    print_pause("They move toward you all at once.", 2)
    print_pause("💀 Some secrets are not meant to be found.", 2)

def stay_hidden_ending():
    print_pause("You hold your breath and stay very still.", 2)
    print_pause("The footsteps get closer... then they pass.", 2)
    print_pause("The dark forest becomes quiet again.", 2)
    print_pause("Slowly, the black sky turns to gold.", 2)
    print_pause("The sun is up. The danger is gone.", 2)
    print_pause("You walk out into the light, safe and free.", 2)

def going_to_cave():
    print_pause("You peer into the dark cave.", 2)
    print_pause("You hear weird noises coming from inside.", 3)
    print_pause("What would you like to do next?", 2)
    print_pause("Enter 1 to enter the cave.", 2)
    print_pause("Enter 2 to turn back and explore another area.", 1)

def enter_cave():
    print_pause("You gather your courage and step into the cave.", 2)
    print_pause("The darkness envelops you as you venture deeper.", 3)
    print_pause("What would you like to do next?", 2)
    print_pause("Enter 1 to continue exploring the cave.", 2)
    print_pause("Enter 2 to search for a way out.", 1)

def lake_decision():
    print_pause("You arrive at a huge underground lake.", 2)
    print_pause("The water is cold and you cannot see the bottom.", 3)
    print_pause("Nearby, there is a small broken wooden boat.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to swim across the lake.", 2)
    print_pause("Enter 2 to use the boat.", 1)

def swim_lake_decision():
    print_pause("You jump into the freezing water.", 2)
    print_pause("Your body starts shaking.", 3)
    print_pause("Something moves under you.", 2)
    print_pause("You PANIC.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to swim faster.", 2)
    print_pause("Enter 2 to go back.", 1)

def swim_faster_ending():
    print_pause("You start swimming faster.", 2)
    print_pause("Your muscles burn painfully.", 2)
    print_pause("Something grabs your leg.", 2)
    print_pause("You are pulled underwater.", 2)
    print_pause("You try to resist but you ended up DROWNING.", 2)

def go_back_lake_ending():
    print_pause("You decide to go back slowly.", 2)
    print_pause("The thing under the water gets closer and closer....", 2)
    print_pause("Suddenly it attacks you.", 2)
    print_pause("You try to fight to stay alive.", 2)
    print_pause("But you ended up being KILLED.", 2)

def use_boat_decision():
    print_pause("You enter the old wooden boat.", 2)
    print_pause("It slowly moves on the lake.", 3)
    print_pause("Water starts leaking inside.", 2)
    print_pause("The boat is unstable.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to row faster.", 2)
    print_pause("Enter 2 to fix the hole.", 1)

def row_faster_ending():
    print_pause("You row as fast as you can.", 2)
    print_pause("Water keeps leaking inside.", 2)
    print_pause("The boat becomes heavy.", 2)
    print_pause("It sinks.", 2)
    print_pause("Speed couldn't save you.", 2)

def fix_hole_ending():
    print_pause("You try to fix the hole carefully.", 2)
    print_pause("You use nearby wood pieces.", 2)
    print_pause("The leak slows down.", 2)
    print_pause("You reach the other side.", 2)
    print_pause("Intelligence saved you.", 2)

def monster_decision():
    print_pause("While searching for a way out of the cave", 3)
    print_pause("You enter an area filled with bones and broken weapons.", 2)
    print_pause(f"Suddenly, {cave_monster} appears in front of you!", 3)
    print_pause("Its eyes glow red and it starts approaching.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to fight the monster.", 2)
    print_pause("Enter 2 to hide and wait.", 1)

def fight_monster_decision():
    print_pause("You prepare yourself for battle.", 2)
    print_pause("The monster roars loudly.", 3)
    print_pause("It attacks with huge claws.", 2)
    print_pause("You feel fear but also courage.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to attack first.", 2)
    print_pause("Enter 2 to defend.", 1)

def attack_first_ending():
    print_pause("You run at the monster and swing your weapon!", 2)
    print_pause("The monster does not even move.", 2)
    print_pause("It looks down at you and smiles.", 2)
    print_pause("With one giant hand, it swats you away like a fly.", 2)
    print_pause("You hit the ground hard. You cannot get up.", 2)
    print_pause("You were brave, but it was too big to fight.", 2)

def defend_ending():
    print_pause("You focus on defending yourself.", 2)
    print_pause("You wait for the right moment.", 2)
    print_pause("The monster starts to lose interest.", 2)
    print_pause("You escape quietly.", 2)
    print_pause("Patience saved you.", 2)

def hide_monster_decision():
    print_pause("You hide behind large rocks.", 2)
    print_pause("The monster searches for you.", 3)
    print_pause("It gets closer.", 2)
    print_pause("You hold your breath.", 2)
    print_pause(monster_sound, 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to escape quietly.", 2)
    print_pause("Enter 2 to surprise attack.", 1)

def escape_quietly_cave_ending():
    print_pause("You move slowly and quietly.", 2)
    print_pause("The monster doesn't notice you.", 2)
    print_pause("You find a secret tunnel.", 2)
    print_pause("You escape safely.", 2)
    print_pause("Stealth saved you.", 2)

def surprise_attack_ending():
    print_pause("You jump suddenly at the monster.", 2)
    print_pause("It reacts instantly.", 2)
    print_pause("It crushes you.", 2)
    print_pause("You fall unconscious.", 2)
    print_pause("Surprise FAILED.", 2)

def exploring_another_area():
    print_pause("You decide not to enter the cave and turn back.", 2)
    print_pause("While exploring another area, you glance at a shiny room in the distance.", 3)
    print_pause("BUT....You feel a strange energy coming from it.", 2)
    print_pause("What would you like to do next?", 2)
    print_pause("Enter 1 to go to the room.", 2)
    print_pause("Enter 2 to ignore it and continue exploring.", 1)

def treasure_decision():
    print_pause("You go there and discover the secret room is filled with gold.", 2)
    print_pause("In the middle, there is a glowing treasure box.", 3)
    print_pause("You feel the strange energy getting stronger.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to open the treasure.", 2)
    print_pause("Enter 2 to ignore it and walk away.", 1)

def open_treasure_decision():
    print_pause("You open the glowing treasure slowly.", 2)
    print_pause("Dark smoke fills the room.", 3)
    print_pause("You start coughing badly.", 2)
    print_pause("A strange voice speaks.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to listen.", 2)
    print_pause("Enter 2 to escape.", 1)

def listen_voice_ending():
    print_pause("You listen to the strange voice.", 2)
    print_pause("It enters your mind.", 2)
    print_pause("You lose control of yourself.", 2)
    print_pause("You become trapped forever.", 2)
    print_pause("The voice consumed you.", 2)

def escape_smoke_ending():
    print_pause("You run away from the smoke.", 2)
    print_pause("You cover your face.", 2)
    print_pause("You run for miles, barely able to breathe.", 2)
    print_pause("Finally you are out of the smoke, but you are in the middle of nowhere.", 3)
    print_pause("Now you are lost forever.", 2)

def ignore_treasure_decision():
    print_pause("You ignore the treasure and walk away.", 2)
    print_pause("The ground starts shaking.", 3)
    print_pause("The room begins collapsing.", 2)
    print_pause("You must act fast.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to run.", 2)
    print_pause("Enter 2 to hide.", 1)

def run_collapse_ending():
    print_pause("You start running fast.", 2)
    print_pause("The ground cracks.", 2)
    print_pause("Rocks fall everywhere.", 2)
    print_pause("You are CRUSHED.", 2)

def hide_collapse_ending():
    print_pause("You hide under a strong rock.", 2)
    print_pause("Debris falls around you.", 2)
    print_pause("You survive barely.", 2)
    print_pause("But most of your bones are BROKEN and you can NOT move.", 3)

def camp_decision():
    print_pause("You find an abandoned camp with old tents.", 2)
    print_pause("A dying fire is still burning slightly.", 3)
    print_pause(camp_detail, 2)
    print_pause("But, you feel very tired after your journey.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to rest near the fire.", 2)
    print_pause("Enter 2 to search the area.", 1)

def rest_camp_decision():
    print_pause("You sit near the warm fire.", 2)
    print_pause("Your eyes slowly close.", 3)
    print_pause("You dream of strange places.", 2)
    print_pause("Suddenly, you wake up.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to stay awake.", 2)
    print_pause("Enter 2 to sleep again.", 1)

def stay_awake_ending():
    print_pause("You stay awake and alert.", 2)
    print_pause("You notice shadows moving.", 2)
    print_pause("You escape before danger comes.", 2)
    print_pause("You reach safety.", 2)
    print_pause("Awareness saved you.", 2)

def sleep_again_ending():
    print_pause("You fall asleep again.", 2)
    print_pause("Strange sounds surround you.", 2)
    print_pause("You never wake up again.", 2)
    print_pause("Sleep became your enemy.", 2)

def search_camp_decision():
    print_pause("You search the camp carefully.", 2)
    print_pause("You find old maps and weapons.", 3)
    print_pause("They may be useful.", 2)
    print_pause("You hear noises nearby.", 2)
    print_pause("What would you like to do?", 2)
    print_pause("Enter 1 to take the weapons.", 2)
    print_pause("Enter 2 to hide.", 1)

def take_weapons_ending():
    print_pause("You grab the old sword.", 2)
    print_pause("At first, you feel strong.", 2)
    print_pause("Then, the sword starts to burn.", 2)
    print_pause("It sticks to your hand. You cannot let go!", 2)
    print_pause("The weapon is drinking your life.", 2)
    print_pause("You are not the master. You are the PREY.", 2)

def hide_camp_ending():
    print_pause("You slip silently into the shadows to hide.", 2)
    print_pause("The footsteps stop right in front of your hiding spot.", 2)
    print_pause("Total silence fills the air...", 3)
    print_pause("Suddenly, a cold voice whispers: 'Found you.'", 2)
    print_pause("You are surrounded before you can even scream.", 2)
    print_pause("You were never safe. You were being hunted.", 2)

def main_game():
    start_game()
    total_score = 0

    next_choice1 = player_choice()

    if next_choice1 == "1":
        knock_on_door()
        print("current score still: ", total_score)

        next_choice2 = player_choice()

        if next_choice2 == "1":
            accept_invitation()
            total_score += 10
            print("Good job! current score: ", total_score)

            next_choice3 = player_choice()

            if next_choice3 == "1":
                hall_decision()
                total_score += 10
                print("Good job! current score: ", total_score)

                next_choice9 = player_choice()

                if next_choice9 == "1":
                    open_chest_decision()
                    total_score += 10
                    print("Good job! current score: ", total_score)

                    next_choice17 = player_choice()

                    if next_choice17 == "1":
                        take_crystal_ending()
                        total_score += 10
                        end_game(total_score)

                    elif next_choice17 == "2":
                        take_key_ending()
                        total_score -= 10
                        end_game(total_score)

                elif next_choice9 == "2":
                    read_book_decision()
                    print("current score still: ", total_score)

                    next_choice18 = player_choice()

                    if next_choice18 == "1":
                        continue_reading_ending()
                        total_score += 10
                        end_game(total_score)

                    elif next_choice18 == "2":
                        close_book_ending()
                        total_score -= 10
                        end_game(total_score)

            elif next_choice3 == "2":
                follow_decision()
                total_score -= 10
                print("bad choice! current score: ", total_score)

                next_choice10 = player_choice()

                if next_choice10 == "1":
                    trust_him_decision()
                    total_score += 10
                    print("Good job! current score: ", total_score)

                    next_choice19 = player_choice()

                    if next_choice19 == "1":
                        help_him_ending()
                        total_score += 20
                        print("AMAZING job! current score: ", total_score)
                        game_status = win_or_lose(total_score)
                        print(game_status)

                    elif next_choice19 == "2":
                        escape_quietly_ending()
                        total_score -= 10
                        end_game(total_score)

                elif next_choice10 == "2":
                    spy_him_decision()
                    print("current score still: ", total_score)

                    next_choice20 = player_choice()

                    if next_choice20 == "1":
                        confront_him_ending()
                        end_game(total_score)

                    elif next_choice20 == "2":
                        run_away_ending()
                        total_score -= 10
                        end_game(total_score)

        elif next_choice2 == "2":
            decline_the_invitation()
            total_score -= 10
            print("bad choice! current score: ", total_score)

            next_choice4 = player_choice()

            if next_choice4 == "1":
                hidden_path_decision()
                total_score -= 10
                print("bad choice! current score: ", total_score)

                next_choice11 = player_choice()

                if next_choice11 == "1":
                    cross_bridge_decision()
                    total_score += 10
                    print("Good job! current score: ", total_score)

                    next_choice21 = player_choice()

                    if next_choice21 == "1":
                        run_fast_bridge_ending()
                        total_score -= 10
                        end_game(total_score)

                    elif next_choice21 == "2":
                        move_slowly_bridge_ending()
                        total_score += 10
                        end_game(total_score)

                elif next_choice11 == "2":
                    climb_rocks_decision()
                    total_score -= 10
                    print("bad choice! current score: ", total_score)

                    next_choice22 = player_choice()

                    if next_choice22 == "1":
                        keep_climbing_ending()
                        end_game(total_score)

                    elif next_choice22 == "2":
                        go_back_down_ending()
                        total_score -= 10
                        end_game(total_score)
                        print_pause("How can you be this bad...that is the lowest possible score",2)
                        print_pause("You literally chose every wrong choice!🫵😂", 2)

            elif next_choice4 == "2":
                forest_decision()
                total_score += 10
                print("Good job! current score: ", total_score)

                next_choice12 = player_choice()

                if next_choice12 == "1":
                    follow_lights_decision()
                    total_score -= 10
                    print("bad choice! current score: ", total_score)

                    next_choice23 = player_choice()

                    if next_choice23 == "1":
                        follow_faster_ending()
                        total_score -= 10
                        end_game(total_score)

                    elif next_choice23 == "2":
                        hide_lights_ending()
                        end_game(total_score)

                elif next_choice12 == "2":
                    build_shelter_decision()
                    total_score += 10
                    print("Good job! current score: ", total_score)

                    next_choice24 = player_choice()

                    if next_choice24 == "1":
                        investigate_shelter_ending()
                        total_score -= 10
                        end_game(total_score)

                    elif next_choice24 == "2":
                        stay_hidden_ending()
                        total_score += 20
                        print("AMAZING job! current score: ", total_score)
                        game_status = win_or_lose(total_score)
                        print(game_status)

    elif next_choice1 == "2":
        going_to_cave()
        total_score += 10
        print("Good job! current score: ", total_score)

        next_choice5 = player_choice()

        if next_choice5 == "1":
            enter_cave()
            total_score += 10
            print("Good job! current score: ", total_score)

            next_choice6 = player_choice()

            if next_choice6 == "1":
                lake_decision()
                total_score -= 10
                print("bad choice! current score: ", total_score)

                next_choice13 = player_choice()

                if next_choice13 == "1":
                    swim_lake_decision()
                    total_score -= 10
                    print("bad choice! current score: ", total_score)

                    next_choice25 = player_choice()

                    if next_choice25 == "1":
                        swim_faster_ending()
                        total_score -= 10
                        end_game(total_score)

                    elif next_choice25 == "2":
                        go_back_lake_ending()
                        total_score -= 10
                        end_game(total_score)

                elif next_choice13 == "2":
                    use_boat_decision()
                    total_score += 10
                    print("Good job! current score: ", total_score)

                    next_choice26 = player_choice()

                    if next_choice26 == "1":
                        row_faster_ending()
                        total_score -= 10
                        end_game(total_score)

                    elif next_choice26 == "2":
                        fix_hole_ending()
                        total_score += 10
                        end_game(total_score)

            elif next_choice6 == "2":
                monster_decision()
                total_score += 10
                print("Good job! current score: ", total_score)

                next_choice14 = player_choice()

                if next_choice14 == "1":
                    fight_monster_decision()
                    total_score += 10
                    print("Good job! current score: ", total_score)

                    next_choice27 = player_choice()

                    if next_choice27 == "1":
                        attack_first_ending()
                        total_score -= 20
                        print("The WORST choice! current score: ", total_score)
                        game_status = win_or_lose(total_score)
                        print(game_status)

                    elif next_choice27 == "2":
                        defend_ending()
                        total_score += 10
                        end_game(total_score)
                        print_pause("How can you be this good!...that is the highest possible score", 2)
                        print_pause("You literally chose every right choice! EXCELLENT🎉🔥🔥", 2)

                elif next_choice14 == "2":
                    hide_monster_decision()
                    total_score -= 10
                    print("bad choice! current score: ", total_score)

                    next_choice28 = player_choice()

                    if next_choice28 == "1":
                        escape_quietly_cave_ending()
                        total_score += 10
                        end_game(total_score)

                    elif next_choice28 == "2":
                        surprise_attack_ending()
                        total_score -= 10
                        end_game(total_score)

        elif next_choice5 == "2":
            exploring_another_area()
            total_score -= 10
            print("bad choice! current score: ", total_score)

            next_choice7 = player_choice()

            if next_choice7 == "1":
                treasure_decision()
                total_score -= 10
                print("bad choice! current score: ", total_score)

                next_choice15 = player_choice()

                if next_choice15 == "1":
                    open_treasure_decision()
                    total_score += 10
                    print("Good job! current score: ", total_score)

                    next_choice29 = player_choice()

                    if next_choice29 == "1":
                        listen_voice_ending()
                        total_score -= 10
                        end_game(total_score)

                    elif next_choice29 == "2":
                        escape_smoke_ending()
                        end_game(total_score)

                elif next_choice15 == "2":
                    ignore_treasure_decision()
                    total_score -= 10
                    print("bad choice! current score: ", total_score)

                    next_choice30 = player_choice()

                    if next_choice30 == "1":
                        run_collapse_ending()
                        total_score -= 10
                        end_game(total_score)

                    elif next_choice30 == "2":
                        hide_collapse_ending()
                        end_game(total_score)

            elif next_choice7 == "2":
                camp_decision()
                total_score += 10
                print("Good job! current score: ", total_score)

                next_choice16 = player_choice()

                if next_choice16 == "1":
                    rest_camp_decision()
                    total_score += 10
                    print("Good job! current score: ", total_score)

                    next_choice31 = player_choice()

                    if next_choice31 == "1":
                        stay_awake_ending()
                        total_score += 10
                        end_game(total_score)

                    elif next_choice31 == "2":
                        sleep_again_ending()
                        total_score -= 10
                        end_game(total_score)

                elif next_choice16 == "2":
                    search_camp_decision()
                    total_score -= 10
                    print("bad choice! current score: ", total_score)

                    next_choice32 = player_choice()

                    if next_choice32 == "1":
                        take_weapons_ending()
                        end_game(total_score)

                    elif next_choice32 == "2":
                        hide_camp_ending()
                        total_score -= 10
                        end_game(total_score)
    return total_score

current_user = intro()
if not current_user:
    print("No user found. Exiting game.")
    exit()
while True:
    account = load_account()
    the_score = main_game()
    if the_score > account[current_user]["highscore"]:
        account[current_user]["highscore"] = the_score
        save_account(account)
        print("🔥 NEW HIGH SCORE!")

    print("Your Highest Score:", account[current_user]["highscore"])
    print_pause("do you want to play again?", 1)
    print_pause("choose 1 if you want to play again", 1)
    print_pause("choose 2 if you do not want to play again", 1)
    next_choice8 = player_choice()
    if next_choice8 == "2":
        print("thank you for playing")
        break
