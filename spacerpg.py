from random import randint  # Imports randint for random number generation.
import copy  # Imports copy, that lets me copy objects, Idk I saw it on stackoverflow and it does what I need.
starNames = ("acamar", "achird", "aldebaran", "meridiana", "arcturus", "antares", "borealis", "asterope", "kaitos", "castor", "celaeno", "pollux", "rastaban", "denebola", "ubuntu", "fomalhaut", "gorgonea", "hydrus", "muscida", "polaris", "kentaurus")
areas = []

class Color:
    R = '\033[31m'
    B = '\033[36m'
    Y = '\033[32m'
    E = '\033[0m'


class Player:
    def __init__(self, name, hp, st, ag):
        self.name = name
        self.mhp = hp  # max hp
        self.hp = hp  # health
        self.st = st  # strength
        self.ag = ag  # agility
        self.lvl = 1  # level
        self.xp = 0  # experience points
        self.stXP = 0  # strength experience
        self.agXP = 0  # agility experience
        self.skillPoints = 0  # skill points after leveling up
        self.cr = 1000  # credits
        for i in range(0, len(starNames) - 1):
            areas.append(Area((starNames[i].replace('\n', '')).capitalize() + " System", i, self, items))
        self.area = areas[0]  # area located
        self.inv = [Item("Map", 0), Equip("Sword", 10, 2, 0), Equip("Shirt", 0, 1, 2)]  # inventory
        self.weapon = Equip("Pistol", 0, 2, 1)
        self.armor = Equip("Uniform", 0, 1, 2)
        self.skills = []  # skills
        self.beastiary = [Enemy("Space Pirate", 20, 10, 10, 0, Item("Map", 0), 10, 10, 100)] #  list of enemies fought
        self.contracts = [copy.copy(self.area.contract)]  # contracts
        self.commands = [Command("Return"), Command("Stats"), Command("Distribute Stats")]  # list of commands


    def update(self):
        while True:
            self.commands.clear()
            self.commands = [Command("Return"), Command("Stats"), Command("Warp"), Command("Beastiary")]
            if self.area.explored < 100:
                self.commands.append(Command("Explore"))
            elif self.area.explored >= 100:
                for i in range(len(self.commands)):
                    if self.commands[i].name == "Explore":
                        del self.commands[i]
                self.commands.append(Command("Enter Planet"))
                self.commands.append(Command("Fight SP"))
            if len(self.contracts) > 0:
                self.commands.append(Command("Contracts"))
            elif len(self.contracts) == 0:
                for i in range(len(self.commands)):
                    if self.commands[i].name == "Contracts":
                        del self.commands[i]
            if self.skillPoints > 0:
                self.commands.append(Command("Distribute Stats"))
            elif self.skillPoints == 0:
                for i in range(len(self.commands)):
                    if self.commands[i].name == "Distribute Stats":
                        del self.commands[i]
            areaNum = 0
            for i in range(len(areas)):
                if areas[i].explored == 100:
                    areaNum += 1
                if (i == len(areas) - 1) and (areaNum == len(areas)):
                    self.commands.append(Command("Win"))
            self.command()

    def damage(self, target):
        if self.weapon.scaling == 0:
            target.hp -= int((self.weapon.mod * 1.5 * self.st) / target.ag)
            self.stXP += 1
            print(Color.Y + self.name + Color.E + " dealt " + Color.Y + str(int((self.weapon.mod * 1.5 * self.st) / target.ag)) + Color.E + " melee damage!")
        elif self.weapon.scaling == 1:
            target.hp -= int((self.weapon.mod * 1.5 * self.ag) / target.st)
            self.agXP += 1
            print(Color.Y + self.name + Color.E + " dealt " + Color.Y + str(int((self.weapon.mod * 1.5 * self.ag) / target.st)) + Color.E + " ranged damage!")

    def command(self):
        commandList = ""
        for i in range(len(self.commands)):
            commandList += "[" + str(i) + "]" + Color.B + self.commands[i].name + Color.E
            if i != (len(self.commands) - 1):
                commandList += "\n"
        print(commandList)
        inp = input("Select command")
        try:
            self.commands[int(inp)].use()
        except (IndexError, ValueError):
            return

    def stats(self, battle):
        print(
            " Name: " + Color.Y + self.name + Color.E + " LVL: " + Color.Y + str(self.lvl) + Color.E + " [" + str(self.xp) + "/100XP] \n " +
            "Credits: " + Color.Y + str(self.cr) + Color.E + " Stat Points: " + Color.Y + str(self.skillPoints) + Color.E + " \n " +
            "HP: " + Color.Y + str(self.hp) + Color.E + "/" + Color.Y + str(self.mhp) + Color.E + " \n ST: " + Color.Y + str(self.st) + Color.E + " [" + str(self.stXP) + "/100XP] \n AG: " + Color.Y + str(self.ag) + Color.E + " [" + str(self.agXP) + "/100XP] \n " +
            "Location: " + Color.Y + self.area.name + Color.E + " [" + str(self.area.explored) + "%] \n " +
            "Weapon: " + Color.Y + self.weapon.name + Color.E + " \n Armor: " + Color.Y + self.armor.name + Color.E
        )
        if len(self.inv) > 0:
            invList, spacing = "", 0  # Prints the players inventory. This is just formatting the string to look readable to humans.
            for i in range(len(self.inv)):
                spacing = 16 - len(self.inv[i].name)  # I assume no item will be longer than 16 characters, so each item is spaced 16 chars apart, with their length factored in.
                invList += "[" + str(i + 1) + "]" + Color.B + self.inv[i].name + Color.E + (" " * spacing)  # Shows the number of the item, it's name, and adds spaces to make each entry 16 characters apart.
                if (i + 1) % 2 == 0:  # Adds a line break every 4 entries.
                    invList += "\n"
            print(invList)
            invInput = input('Type the item number to use it.')
            try:
                if int(invInput) > 0:
                    if self.inv[int(invInput) - 1].use():
                        del self.inv[int(invInput) - 1]
                        if battle:
                            return
                        else:
                            self.stats(battle)
                else:
                    return
            except (IndexError, ValueError):  # Handles entries that aren't numbers in the inv's range.
                return

    def skill(self,
              target):  # Function to use skill in a fight. All skill objects have a use function, which checks their name against an if chain of skill effects. Want better way but can't think of one
        printSkill, spacing = "", 0
        for i in range(len(self.skills)):  # Prints skill list. Same as item list. Just list and string stuff
            spacing = 20 - len(self.skills[i].name)
            printSkill += "[" + str(i + 1) + "]" + Color.B + self.skills[i].name + Color.E + (" " * spacing)
            if (i + 1) % 2 == 0:
                printSkill += "\n"
        print(printSkill)
        skillInput = input('Type the skill number to use it.')
        try:
            if int(skillInput) > 0:
                self.skills[int(skillInput) - 1].use(self, target)  # Asks to use the selected skill.
            elif int(skillInput) == 0:
                return False
        except (IndexError, ValueError):  # Handles entries that aren't numbers in the skills's range.
            self.skill(target)

    def expGain(self, amt):  # Gives XP to player. Made into function so to include the level up check every time the player's XP increases.
        self.xp += amt
        if self.stXP >= 100:
            self.stXP -= 100
            self.st += 1
            print("Strength increased!")
        if self.agXP >= 100:
            self.agXP -= 100
            self.ag += 1
            print("Agility increased!")
        if self.xp >= 100:
            self.xp -= 100
            self.lvl += 1
            self.skillPoints += 0
            self.mhp += 5
            self.hp = self.mhp
            print("Leveled up! Level now " + Color.Y + str(self.lvl) + Color.E + "!")

    def statLevel(self):  # Let's player distribute stat points from leveling up. Want to use this system for skills too, and maybe perks, and talents, and other RPG things.
        while self.skillPoints > 0:
            statInput = input("You have " + str(self.skillPoints) + " stat points. Enter 1 for HP, 2 for ST, 3 for AG")
            amtInput = input("Enter how many points you would like to put into this stat")
            try:  # Don't put in incorrect information or you will have a bad time.
                if int(amtInput) <= self.skillPoints:
                    if statInput == "1":
                        self.mhp += int(amtInput)
                        self.hp += int(amtInput)
                        self.skillPoints -= int(amtInput)
                    elif statInput == "2":
                        self.st += int(amtInput)
                        self.skillPoints -= int(amtInput)
                    elif statInput == "3":
                        self.ag += int(amtInput)
                        self.skillPoints -= int(amtInput)
                else:
                    print("Not enough stat points")
            except (IndexError, ValueError):  # Handles entries that aren't numbers in the inv's range.
                return


class Enemy():  # Enemy. Drops item with a certain dropChance, and always gives an amount of XP and credits. Also inherits everything from Character
    def __init__(self, name, hp, st, ag, scaling, drop, xp, cr, dropChance):
        self.name = name
        self.hp = hp
        self.mhp = hp
        self.st = st
        self.ag = ag
        self.scaling = scaling
        self.drop = drop
        self.xp = xp
        self.cr = cr
        self.dropChance = dropChance

    def damage(self, target):
        if self.scaling == 0 and int((self.st) - (target.ag * .7 * target.armor.mod)) > 0:
            target.hp -= int((self.st) - (target.ag * .7 * target.armor.mod))
            print(Color.R + self.name + Color.E + " dealt " + Color.R + str(int((self.st) - (target.ag * .7 * target.armor.mod))) + Color.E + " melee damage!")
        elif self.scaling == 1 and int((self.ag) - (target.st * .7 * target.armor.mod)) > 0:
            target.hp -= int((self.ag) - (target.st * .7 * target.armor.mod))
            print(Color.R + self.name + Color.E + " dealt " + Color.R + str(int((self.ag) - (target.st * .7 * target.armor.mod))) + Color.E + " ranged damage!")
        else:
            print(Color.R + self.name + Color.E + " dealt no damage!")


class Item:  # Item class. Items and skills are essentially implemented the same way
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def use(self):  # Use function runs items name through if chain, don't know other way.
        if self.name == "Potion":  # Heals if player hp < max hp
            if player.hp < player.mhp:
                player.hp += 10
                return True
        elif self.name == "Magic Dust":  # Gives player XP
            player.expGain(20)
            return True
        elif self.name == "Antidote":  # Cures status effects, if I had any
            print("Don't you open up that window")
            return True
        elif self.name == "Map":
            player.area.explored = 100
            return True

    def buy(self):  # Buy function. Check if player has at least the cost of the item in credits, if they do, decreases that amount from the players wallet, and appends the item to the inventory.
        if player.cr >= self.cost:
            player.cr -= self.cost
            for i in range(len(player.contracts)):
                if player.contracts[i].object == self.name and player.contracts[i].amount != player.contracts[i].required:
                    player.contracts[i].amount += 1
                    print("Item used towards contract " + Color.Y + player.contracts[i].name + Color.E)
                    return
            player.inv.append(copy.copy(self))
            print("Purchased " + Color.Y + self.name + Color.E + "!")
        else:  # Poor, sad!
            print("Not enough credits! Need " + Color.Y + str(self.cost - player.cr) + Color.E + " credits.")
            return False


class Equip(Item):
    def __init__(self, name, cost, mod, scaling):
        super().__init__(name, cost)
        self.mod = mod  # amount to modify damage
        self.scaling = scaling  # melee or ranged, 0 or 1, 2 for armor

    def use(self):
        if self.scaling == 2:
            player.inv.append(copy.copy(player.armor))
            player.armor = copy.copy(self)
        else:
            player.inv.append(copy.copy(player.weapon))
            player.weapon = copy.copy(self)
        print("Equipped " + Color.Y + self.name + Color.E + "!")
        return True


items = [  # List of items.
    Item("Potion", 20),
    Item("Magic Dust", 30),
    Item("Antidote", 50)
]
itemsSet1 = [
    Item("Potion", 20),
    Item("Magic Dust", 30),
    Equip("Sword", 10, 1, 0)
]
enemies = []  # Item drop, XP drop, CR drop, item drop chance, name, HP, AD, AP, AR, MR, LK
for i in range(0, 1000):
    enemies.append(
        Enemy("#" + str(i), randint(10, 30), randint(7, 12), randint(7, 12), randint(0,1), copy.copy(items[0]), 10, 10, 20))


class Skill:  # Skill class.
    def __init__(self, name, cost):  # Has name and cost (mana? idk). Cost isn't implemented yet.
        self.name = name
        self.cost = cost

    def use(self, user, target):  # Use function runs skills name through if chain, don't know other way.
        if self.name == "Fire":  # Fire. Does AP damage, so calculates based on user's ap and targets mr.
            user.damage(target, 1)
            return True
        elif self.name == "Heal":  # Heals user. Could probably make it usable on people other than user, but there's no need at the moment.
            user.hp += 10
            print("Healed 10 HP!")
            if user.hp > user.mhp:  # Could put the check at the top to prevent people wasting a turn on healing when they're full hp, or I could do it this way.
                user.hp = user.mhp
            return True
        elif self.name == "Kill":  # Just kills the enemy. Debug mostly.
            target.hp = 0
            print("Enemy killed!")
            return True
        elif self.name == "Scan":
            print("Scanned " + target.name + "! \n HP: " + Color. R + str(target.hp) + Color.E + "/" + Color.R + str(target.mhp) + Color.E + " \n ST: " + Color.R + str(target.st) + Color.E + " \n AG: " + Color.R + str(target.ag) + Color.E)
        else:
            return False


skillList = [  # List of skills. For now the player can use all skills, but learning skills planned
    Skill("Kill", 20),
    Skill("Heal", 20),
    Skill("Scan", 20)
]


class Contract:  # Contract class. Haven't done anything yet.
    def __init__(self, task, object, required, cr, xp):
        self.task = task  # kill, collect
        self.object = object  # object or enemy required
        self.required = required  # amount required
        self.name = task.capitalize() + " " + str(required) + " " + object
        self.amount = 0  # amount total
        self.cr = cr  # cr given for completion
        self.xp = xp  # xp given for completion

    def check(self):
        if self.amount >= self.required:
            print('Completed the contract ' + Color.Y + self.name + Color.E + '!')
            player.cr += self.cr
            player.expGain(self.xp)
            return True


contracts = [
    Contract("kill", "Space Pirate", 3, 25, 25),
    Contract("collect", "Potion", 5, 25, 25)
]


class Area:  # Area class. Haven't done anything yet.
    def __init__(self, name, number, player, items):  # Name, and events is how many events will occur, and eventCount is how many have occurred. Will change probably.
        self.name = name
        self.number = number
        self.player = player
        self.enemies = [Enemy(self.name + " Scout", int(player.hp*.7), int(player.st*.8), int(player.ag*.8), 1, Item("Potion",20), 10, 10, 20),
                        Enemy(self.name + " Guard", int(player.hp*.8), int(player.st*.9), int(player.ag*.9), 0, Item("Potion",20), 20, 20, 20),
                        Enemy(self.name + " Defender", int(player.hp*1.1), int(player.st*1), int(player.ag*1), 0, Item("Potion",20), 30, 30, 20),
                        Enemy(self.name + " Soldier", int(player.hp*1.2), int(player.st*1.2), int(player.ag*1.2), 1, Item("Potion",20), 40, 40, 30),
                        Enemy(self.name + " Trooper", int(player.hp*1.3), int(player.st*1.3), int(player.ag*1.3), 1, Item("Potion",20), 30, 30, 20)]
        self.items = items
        self.explored = 0
        self.contract = Contract("kill", self.name + " Leader", 1, 100, 100)
        self.boss = Enemy(self.name + " Leader", int(player.hp*2),int(player.st*1.7),int(player.ag*1.7),0,Equip("Laser Pistol",50,2,1),100,100,100)

    def explore(self):
        if randint(0, 10) == 4:
            self.explored += 10
            print("Discovered more about the system")
        else:
            for i in player.contracts:
                if i.name == self.contract.name:
                    if game.chance(10):
                        game.fight(player, self.boss, False)
                        self.explored = 100
                        return
            game.fight(player, copy.copy(self.enemies[randint(0, len(self.enemies) - 1)]), True)
            self.explored += 5

    def planet(self):
        player.commands.clear()
        player.commands = [Command("Return"), Command("Shop"), Command("Pub"), Command("Warp")]
        player.command()


class Command:
    def __init__(self, name):
        self.name = name

    def use(self):
        if self.name == "Return":
            return
        elif self.name == "Win":
            exit()
        elif self.name == "Explore":
            player.area.explore()
        elif self.name == "Beastiary":
            print("List of enemies: ")
            for i in range(len(player.beastiary)):
                print(Color.R + player.beastiary[i].name + Color.E + " \n HP: " + str(player.beastiary[i].mhp) + " \n ST: " + str(player.beastiary[i].st) + " \n AG: " + str(player.beastiary[i].ag))
        elif self.name == "Fight SP":
            game.fight(player, Enemy("Space Pirate", 20, 10, 10, 0, Item("Map", 0), 10, 10, 100), True)
        elif self.name == "Stats":
            player.stats(False)
        elif self.name == "Distribute Stats":
            player.statLevel()
        elif self.name == "Enter Planet":
            player.area.planet()
        elif self.name == "Shop":
            game.shop(player, player.area.items)
        elif self.name == "Pub":
            print("Received contracts.")
            player.contracts.append(contracts[0])
            player.contracts.append(contracts[1])
        elif self.name == "Warp":
            spacing, areasList, color = 0, "", Color.B
            for i in range(len(areas)):
                spacing = 16 - len(areas[i].name)
                if areas[i].explored == 0:
                    color = Color.R
                elif areas[i].explored >= 100:
                    color = Color.B
                else:
                    color = Color.Y
                areasList += "[" + str(i + 1) + "]" + color + areas[i].name + Color.E + (" " * spacing)
                if (i + 1) % 2 == 0:
                    areasList += "\n"
            print(areasList)
            areaInput = input('Type the area number to warp to it.')
            try:
                if int(areaInput) > 0:  # and input('Warp to ' + Color.Y + areas[int(areaInput) - 1].name + Color.E + '? 1 for yes.') == "1":
                    if areas[int(areaInput) - 1].explored == 0:
                        player.contracts.append(copy.copy(areas[int(areaInput) - 1].contract))
                        areas[int(areaInput) - 1] = Area(areas[int(areaInput) - 1].name, areas[int(areaInput) - 1].number, areas[int(areaInput) - 1].player, areas[int(areaInput) - 1].items)
                    player.area = areas[int(areaInput) - 1]
            except (IndexError, ValueError):  # Handles entries that aren't numbers in the inv's range.
                return
        elif self.name == "Contracts":
            spacing, contractList = 0, ""
            for i in range(len(player.contracts)):
                spacing = 24 - len(player.contracts[i].name)
                contractList += "[" + str(i + 1) + "]" + Color.B + player.contracts[i].name + Color.E + (" " * spacing)
                if i != (len(player.contracts)-1):
                    contractList += "\n"
            print(contractList)
            contractInput = input("Select contract")
            try:
                if player.contracts[int(contractInput) - 1].check() == True:
                    del player.contracts[int(contractInput) - 1]
                else:
                    print(str(player.contracts[int(contractInput) - 1].amount) + "/" + str(player.contracts[int(contractInput) - 1].required) + " " + player.contracts[int(contractInput) - 1].object)
            except (IndexError, ValueError):
                return


class Game:  # Game class. Where all the game stuff happens.
    def __init__(self):
        print("Welcome to the game. 1 is yes, 0 is no or return. Use the enter key. Enjoy.")

    def shop(self, player, items):  # Shop function. Allows certain shops to only sell certain items, but they need to be in a continuous block, at the moment. Could just make separate item lists for each area's shop, but that's redundant.
        itemsList, spacing = "", 0
        for i in range(len(items)):  # Lists items in item list within the given range. This just prints the items that the user can buy.
            spacing = 20 - len(items[i].name) - len(str(items[i].cost))  # Even spacing between items in the print.
            itemsList += "[" + str(i + 1) + "]" + Color.B + items[i].name + Color.E + " (" + str(items[i].cost) + ")" + (
                " " * spacing)  # Making the string look pretty
            if (i + 1) % 2 == 0:  # Every 4 items, line break
                itemsList += "\n"
        print(itemsList)
        storeInput = input("You have " + Color.Y + str(player.cr) + Color.E + " Credits.\n Type the number of the item you wish to buy")
        try:
            if storeInput != "0" and items[int(storeInput) - 1]:  # Yay generalized item purchasing instead of a stupidly long elif chain!
                amtInput = input("Enter amount to buy")
                for i in range(int(amtInput)):
                    if items[int(storeInput) - 1].buy() == False:
                        break
                game.shop(player, items)
            else:
                return
        except (IndexError, ValueError):  # Error handling. Type a number in the range and there won't be any issues.
            return

    def fight(self, player, en, am):  # Fight function. Could theoretically have non-players fight each other using this function, just need an AI for both sides in that usecase.
        enemy, turnCount = en, 1  # Copies enemy object from enemy list. Object is deleted when enemy hp > 0. TurnCount, number of turns, UI purposes.
        print("Enemy " + Color.R + enemy.name + Color.E + " appears!")
        if am == True and game.chance(10) == True:  # Enemy ambush, gets to move first. Set whatever probability you want, or whatever, I don't care. Maybe you always get ambushed in some areas. Pretty good.
            turn = 0  # Turn 0 is enemy turn
            print(" Ambushed!")
        else:
            turn = 1  # Turn 1 is player turn
        while True:  # While loop if enemy is alive.
            if turn == 1:
                print("Turn " + str(turnCount) + " | " + Color.Y + player.name + Color.E + ": " + str(player.hp) + " HP | " + Color.R + enemy.name + Color.E + ": " + str(enemy.hp) + " HP")  # UI
                fightInput = input("1 to attack, 2 for items, 3 for skills, 4 to escape")  # Options for player. 1 is plain physical attack, 2 is use an item, 3 is use a skill, 4 tries to escape.
                if fightInput == "1":
                    player.damage(enemy)  # Attack enemy
                elif fightInput == "2" and len(player.inv) > 0:
                    player.stats(True)  # Check player stats/use item
                elif fightInput == "3":
                    if player.skill(enemy) == False:  # Check skills
                        continue
                elif fightInput == "4":
                    if game.chance(33):  # Maybe I have garbage collection issues I'm not aware of with all this function switching.
                        print("Escaped!")
                        return
                    else:
                        print("Failed to escape!")
                else:
                    continue
                turnCount += 1
                turn = 0
            else:
                enemy.damage(player)  # enemy attacks. No AI yet, just randomly attacks with physical or ability damage.
                turn = 1
            if player.hp <= 0:  # If you die, you lose. GG
                print("You died!")
                quit()
            elif enemy.hp <= 0:  # If the enemy dies, you win. Return ends function right? I don't want a bunch of dead fight functions left running bc I'm bad at python.
                print("Won!")
                player.cr += enemy.cr
                player.expGain(enemy.xp)
                for num, i in enumerate(player.beastiary):
                    if i.name == enemy.name:
                        break
                    elif num == len(player.beastiary) - 1:
                        player.beastiary.append(copy.copy(enemy))
                if game.chance(enemy.dropChance) == True:
                    player.inv.append(enemy.drop)
                    print("Received " + Color.Y + enemy.drop.name + Color.E + "!")
                for i in range(len(player.contracts)):
                    if player.contracts[i].object == enemy.name:
                        player.contracts[i].amount += 1
                        break
                del enemy
                return

    def chance(self, percent):
        if randint(0, 100) < percent:
            return True


game = Game()  # Initializes game object. Stuff
player = Player(input("Name . . . ").capitalize(), 25, 10, 10)# Creates player. Could have character creator at start, or could just give the player statpoints and let them figure it out.
player.skills = skillList  # Just gives player all skills. Debugging
player.update()  # Starts update function in player object, which is essentially the whole game
