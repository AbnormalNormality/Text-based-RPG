import random
from colorama import Fore
import os
import time
devm = False
skills = []
def readFile(file,x):
    try:
        with open(file, "r") as file:
            for _ in range(x + 1):
                x_line = file.readline()
        return x_line.strip()
    except:
        pass
#Start
save = 1
while True:
    choice = input("Do you have a savefile? (y/n)\n")
    if choice.lower() == "y" or choice.lower() == "n":
        if choice == "y":
            choice = input("Where is the file located? (Default is savefile.txt)\n").rstrip("\"").lstrip("\"")
            choice = (r"C:\Users\dandr\PycharmProjects\Python Projects\Text-based RPG\savefile.txt").rstrip("\"").lstrip("\"")
            if not os.path.isfile(choice):
                print("Could not find any file at the specified path")
                continue
            else:
                if sum(1 for _ in open(choice)) > 1:
                    while True:
                        save = input("Multiple savefiles detected, which one do you want to use? (" + str(sum(1 for _ in open(choice))) + (")\n"))
                        try:
                            save = int(save)
                            if save >= 1 and save <= sum(1 for _ in open(choice)):
                                break
                        except:
                            print("\033[F\033[K", end="")
                            print("\033[F\033[K", end="")
                user,xp,xpRoof,levelCurve,level,HPValue,defense,eHPValue,eDefense,attack,magic,MPValue,eAttack,eStrongAttack,attackChance,strongAttackChance,specialChance,waitChance = readFile(choice, save - 1).split(",")
                xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attack, magic, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance = [float(var) for var in (xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attack, magic, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance)]
        if choice == "n":
            save = -1
            user = input("What name do you want for the savefile?\n")
            xp = 0
            xpRoof = 100
            levelCurve = 2.05
            level = 0
            HPValue = 20
            defense = 0
            eHPValue = 14
            eDefense = 0
            attack = 5
            magic = 3
            MPValue = 15
            eAttack = 3.5
            eStrongAttack = 5.5
            attackChance = 25
            strongAttackChance = 50
            specialChance = 75
            waitChance = 100
        break
    else:
        print("\033[F\033[K", end="")
        print("\033[F\033[K", end="")
while True:
    choice = input("Do you want to play combat mode or story mode?\n")
    if choice.lower() == "combat" or choice.lower() == "story":
        break
    else:
        print("\033[F\033[K", end="")
        print("\033[F\033[K", end="")
os.system('cls||clear')
def levelUp():
    global HPValue,attack,magic,defense,MPValue
    if level == 1:
        print("New skill, heal")
        skills.append("heal")
    if level == 3:
        print("New skill,")
        skills.append("")
    if level == 6:
        print("New skill,")
        skills.append("")
    if level == 10:
        print("New skill,")
        skills.append("")
    while True:
        choice = input("What stat do you want to raise? (HP, attack, magic, defense)\n")
        if choice.lower() == "hp" or choice.lower() == "attack" or choice.lower() == "magic" or choice.lower() == "defense":
            break
        else:
            print("\033[F\033[K", end="")
            print("\033[F\033[K", end="")
    if choice.lower() == "hp":
        HPValue *= 1.05
        print(HPValue)
    if choice.lower() == "attack":
        attack *= 1.05
        print(attack)
    if choice.lower() == "magic":
        magic *= 1.05
        MPValue *= 1.02
        print(magic,MPValue)
    if choice.lower() == "defense":
        if defense == 0:
            defense = 1
        else:
            defense *= 1.05
        print(defense)
    print("Your",choice,"has been increased by 5%")
def combat(HPValue,defense,eHPValue,eDefense,attack,magic,MPValue,eAttack,eStrongAttack,attackChance,strongAttackChance,specialChance,waitChance):
    global xp,xpRoof,level,levelCurve,turn
    level = int(level)
    turn = 0
    HP = HPValue
    MP = MPValue
    eHP = eHPValue
    while HP >= 1 and eHP >= 1:
        #Player Turn
        choice = ""
        if not choice.lower() == "player" and not choice.lower() == "enemy":
            print(Fore.GREEN + str(round(HP)) + Fore.RESET,"/",Fore.RED + str(round(eHP)) + Fore.RESET)
        while True:
            choice = input("What do you want to do? (attack, special, or scout)\n")
            if choice.lower() == "attack" or choice.lower() == "special" or choice.lower() == "scout":
                print("\033[F\033[K", end="")
                print("\033[F\033[K", end="")
                if not choice.lower() == "scout":
                    print("\033[F\033[K", end="")
                break
            else:
                print("\033[F\033[K", end="")
                print("\033[F\033[K", end="")
        if choice.lower() == "attack":
            damage = random.randint(round(attack - attack * 0.3), round(attack + attack * 0.3)) - round(eDefense / 2)
            eHP -= damage
            print("You attack",name)
            print(Fore.YELLOW + name,"loses",damage,"health" + Fore.RESET)
        if choice.lower() == "special":
            while True:
                choice = input("What ability do you want to use? " + str(skills).replace("\'","") + "\n")
                if choice.lower() in skills:
                    print("\033[F\033[K", end="")
                    print("\033[F\033[K", end="")
                    print("\033[F\033[K", end="")
                    break
                else:
                    print("\033[F\033[K", end="")
                    print("\033[F\033[K", end="")
            try:
                if choice == skills[0]:
                    if MP >= 8:
                        MP -= 8
                        healing_amount = round(HP * 0.3)
                        excess = (HP + healing_amount) % HPValue
                        HP += healing_amount - excess
                        print("You cast heal,", healing_amount - excess)
                    else:
                        print("You don't have enough MP (8), you have",MP)
                if choice == skills[1]:
                    print("Second skill")
                if choice == skills[2]:
                    print("Third skill")
            except:
                pass
        if choice.lower() == "scout":
            while True:
                choice = input("Who do you want to scout? (player, enemy)\n")
                if choice.lower() == "player" or choice.lower() == "enemy":
                    print("\033[F\033[K", end="")
                    print("\033[F\033[K", end="")
                    print("\033[F\033[K", end="")
                    break
                else:
                    print("\033[F\033[K", end="")
                    print("\033[F\033[K", end="")
            if choice.lower() == "player":
                print(user,round(HP),round(defense),round(attack),round(magic),round(MP))
            if choice.lower() == "enemy":
                print(name,"the",type,round(eHP),round(eAttack),round(eStrongAttack))
            continue
        print("")
        if eHP >= 1:
            time.sleep(1)
            turn += 1
            #Enemy Turn
            choice = random.randint(1,100)
            if choice <= attackChance:
                #Weak attack
                damage = random.randint(round(eAttack - eAttack * 0.3), round(eAttack + eAttack * 0.3)) - round(defense / 2)
                HP -= damage
                print(name,"attacks you")
                print(Fore.RED + "You lose",damage,"health" + Fore.RESET)
            if choice > attackChance and choice <= strongAttackChance:
                #Strong attack
                damage = random.randint(round(eStrongAttack - eStrongAttack * 0.3), round(eStrongAttack + eStrongAttack * 0.3)) - round(defense / 2)
                HP -= damage
                print(name,"does a strong attack")
                print(Fore.RED + "You lose",damage,"health" + Fore.RESET)
            if choice > strongAttackChance and choice <= specialChance:
                #Special
                print(name,"does... Something?")
            if choice > specialChance:
                # Wait
                print(name,"does nothing")
            print("")
            time.sleep(1)
            turn += 1
    if eHP <= 1:
        print("You win")
        xp = xp + round(eHPValue + (eAttack + eStrongAttack) * 2)
        print("You gained", round(eHPValue + (eAttack + eStrongAttack) * 2), "xp (" + str(xp) + ")")
        if xp >= xpRoof:
            storage = 0
            while xp >= xpRoof:
                level += 1
                xp -= xpRoof
                xpRoof = round(xpRoof * levelCurve)
                print("Level up! (" + str(level) + ")")
                storage += 1
            while storage > 0:
                storage -= 1
                levelUp()
    if HP <= 1:
        print("You lose")
        input("Press ENTER to exit")
        exit()
    input("Press ENTER to continue")
    os.system('cls||clear')
def getName(*number):
    if not number == "":
        enemyName = random.randint(0,9)
    else:
        enemyName = number
    if enemyName == 0:
        return("Clyde")
    if enemyName == 1:
        return("Jeremy")
    if enemyName == 2:
        return("Bob")
    if enemyName == 3:
        return("Robbert")
    if enemyName == 4:
        return(Fore.RED + "Placeholder" + Fore.RESET)
    if enemyName == 5:
        return(Fore.RED + "Placeholder" + Fore.RESET)
    if enemyName == 6:
        return(Fore.RED + "Placeholder" + Fore.RESET)
    if enemyName == 7:
        return(Fore.RED + "Placeholder" + Fore.RESET)
    if enemyName == 8:
        return(Fore.RED + "Placeholder" + Fore.RESET)
    if enemyName == 9:
        return(Fore.RED + "Placeholder" + Fore.RESET)
def getType(*number):
    #Make a chance value the same as the next to disable it
    #Except for the waitChance, to disable waiting, set it to 100
    global attackChance,strongAttackChance,specialChance,waitChance
    if not number == "":
        enemyType = random.randint(0, 9)
    else:
        enemyType = number
    if enemyType == 0:
        return("Dragon")
        attackChance = 0
        strongAttackChance = 0
        specialChance = 0
        waitChance = 0
    if enemyType == 1:
        return("Goblin")
        attackChance = 50
        strongAttackChance = 62.5
        specialChance = 75
        waitChance = 75
    if enemyType == 2:
        return("Mage")
        attackChance = 0
        strongAttackChance = 0
        specialChance = 0
        waitChance = 0
    if enemyType == 3:
        return("Troll")
        attackChance = 0
        strongAttackChance = 0
        specialChance = 0
        waitChance = 0
    if enemyType == 4:
        return("Warrior")
        attackChance = 0
        strongAttackChance = 0
        specialChance = 0
        waitChance = 0
    if enemyType == 5:
        return("Golem")
        attackChance = 0
        strongAttackChance = 0
        specialChance = 0
        waitChance = 0
    if enemyType == 6:
        return("Peasant")
        attackChance = 0
        strongAttackChance = 0
        specialChance = 0
        waitChance = 0
    if enemyType == 7:
        return(Fore.RED + "Placeholder" + Fore.RESET)
        attackChance = 0
        strongAttackChance = 0
        specialChance = 0
        waitChance = 0
    if enemyType == 8:
        return(Fore.RED + "Placeholder" + Fore.RESET)
        attackChance = 0
        strongAttackChance = 0
        specialChance = 0
        waitChance = 0
    if enemyType == 9:
        return(Fore.RED + "Placeholder" + Fore.RESET)
        attackChance = 0
        strongAttackChance = 0
        specialChance = 0
        waitChance = 0
if choice == "combat":
    while True:
        global name,type
        name = getName()
        type = getType()
        print("You are attacked by",name,"the",type)
        combat(HPValue, defense, eHPValue, eDefense, attack, magic, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance)
        eHPValue = round(eHPValue * 1.05,1)
        if eDefense == 0:
            eDefense = 1
        else:
            eDefense = round(eDefense * 1.05,1)
        eAttack = round(eAttack * 1.05,1)
        eStrongAttack = round(eStrongAttack * 1.05,1)
        if not "file" in locals():
            file = "savefile.txt"
        variables = [user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attack, magic,
                     MPValue,
                     eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance]
        if save == -1:
            save = sum(1 for _ in open(file)) + 1
            with open(file, 'a') as f:
                f.writelines("\n")
            print("Balls")
        with open(file, 'r') as f:
            lines = f.readlines()
        if 1 <= save <= len(lines):
            lines[save - 1] = ','.join(map(str, variables)) + '\n'
        with open(file, 'w') as f:
            f.writelines(lines)
if choice == "story":
    input("Dead end, turn back ")