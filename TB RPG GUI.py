from tkinter import Tk, Label, Button, Toplevel
from tkinter.ttk import *
import random
import ctypes
import os
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

def readFile(file,x):
    try:
        with open(file, "r") as file:
            for _ in range(x + 1):
                x_line = file.readline()
        return x_line.strip()
    except:
        pass

def tkprint(window, yourText, side):
    label = Label(window, text=yourText)
    label.pack(side=side)
    return label

def tkbutton(window, text, command, side, **kwargs):
    button = Button(window, text=text, command=command, **kwargs)
    button.pack(side=side)
    return button

def getName(*extra):
    names = ["Bob","Jim Scarey","Apples","Corban","Oscar","Charlie","Alia","Spencer","Avery","Sophie","Chris Snack","Mr. Peepee on your ear",""]
    return random.choice(names)

def getRace(*extra):
    races = ["Goblin", "Dragon", "Troll", "Mage", "Warrior", "Rogue", "Golem", "Peasant","Fangirl","Tree","Loser","Viking","God","Fruit snacks","Child","Opponent"]
    adjectives = ["Viscious", "Playful", "Angry","Energetic","Empty","Smart","Depressed","Afraid"]
    if extra:
        return random.choice(races)
    else:
        return random.choice(adjectives)+" "+random.choice(races)

def resetMain():
    main.title("New! Text-based RPG")
    main.minsize(200, 100)
    main.geometry("300x100+50+50")
    deleteButtons(frame_bottom)
    atkButton = tkbutton(frame_bottom, "Attack", lambda: attack(), "left")
    magButton = tkbutton(frame_bottom, "Magic", lambda: perform_action("Magic"), "left")
    sctButton = tkbutton(frame_bottom, "Scout", lambda: perform_action("Scout"), "left")

def deleteButtons(root):
    for widget in root.winfo_children():
        if isinstance(widget, Button):
            widget.destroy()

def deleteAll(root):
    for widget in root.winfo_children():
        widget.destroy()

def deleteLabels(root):
    for widget in root.winfo_children():
        if isinstance(widget, Label):
            widget.destroy()

def resetLog():
    log.title("Log")
    log.minsize(175, 300)
    log.geometry("175x300+375+50")

def attack():
    global eHP, name, canAction
    if canAction == True:
        damage = random.randint(round(attackValue - attackValue * 0.3), round(attackValue + attackValue * 0.3)) - round(eDefense / 2)
        eHP -= damage
        tkprint(log, "You attack {} (-{})".format(name,damage), "top")
        secondPhase()
    else:
        pass

def item_click(item):
    global MP
    print(f"Button clicked: {item}")
    Label(log,text="You cast {}!".format(item)).pack(side="top")
    if item == "Heal" and MP >= 6:
        MP -= 8
        healing_amount = round(HP * 0.3)
        excess = (HP + healing_amount) % HPValue
        HP += healing_amount - excess
        tkprint(log,"You heal {}".format(healing_amount - excess),"top")
    if item == "Fireball" and MP >= 0:
        #effect
        tkprint(log,"text","top")
    secondPhase()

def scout(target):
    global user,HP,attackValue,magicValue,MPValue,defense,name,eHP,eAttack,eStrongAttack,eDefense
    if target == "player":
        Label(log,text="{}: {}, {}, {}, {}, {}".format(user,HP,attackValue,magicValue,MPValue,defense)).pack(side="top")
    if target == "enemy":
        Label(log,text="{}: {}, {}, {}, {}".format(name,eHP,eAttack,eStrongAttack,eDefense)).pack(side="top")
    mainPhase()

def perform_action(action):
    global text,canAction,MP
    if canAction == True:
        text.destroy()
        deleteButtons(frame_bottom)
        Button(frame_bottom, text="Back", command=lambda: mainPhase()).pack(side="left")
        if action == "Magic":
            text = Label(main, text="What ability do you want to use? ({})".format(MP))
            text.pack(side="bottom")
            [Button(frame_bottom, text=item, command=lambda i=item: item_click(i)).pack(side="left") for item in skills]
        elif action == "Scout":
            text = Label(main, text="Who do you want to scout")
            text.pack(side="bottom")
            Button(frame_bottom,text="You",command=lambda: scout("player")).pack(side="left")
            Button(frame_bottom, text=name, command=lambda: scout("enemy")).pack(side="left")
    else:
        pass

def levelUp():
    global atkButton,magButton,sctButton,canContinue,level
    level += 1
    if level >= 2:
        skills.append("Heal")
    if level >= 5:
        skills.append("Fireball")
    if level >= 8:
        skills.append("Lightning")
    canContinue = False
    deleteButtons(frame_bottom)
    choice = None
    def raiseStat(stat):
        global HPValue,defense,attackValue,magicValue,MPValue,canContinue
        HPButton.destroy()
        defenseButton.destroy()
        attackButton.destroy()
        magicButton.destroy()
        if stat == "HP":
            chosenStat = "HP"
            HPValue *= 1.05
        if stat == "defense":
            chosenStat = "defense"
            defense *= 1.05
        if stat == "attack":
            chosenStat = "attack"
            attackValue *= 1.05
        if stat == "magic":
            chosenStat = "magic"
            magicValue *= 1.05
            MPValue *= 1.05
        canContinue = True
        Label(log,text="{} has been increased by 5%".format(chosenStat),wraplength=175).pack(side="top")
        resetMain()
    HPButton = tkbutton(frame_bottom,"HP",lambda:raiseStat("HP"),"left")
    attackButton = tkbutton(frame_bottom,"Attack",lambda:raiseStat("attack"),"left")
    magicButton = tkbutton(frame_bottom,"Magic",lambda:raiseStat("magic"),"left")
    defenseButton = tkbutton(frame_bottom,"Defense",lambda:raiseStat("defense"),"left")

def mainPhase():
    global text, level, values, eHP, xp, xpRoof, canAction, HPValue, eHPValue, HP, loop, winCheck, MPValue, MP, turn
    if not "loop" in globals() or loop == False:
        turn = 0
        HP = HPValue
        eHP = eHPValue
        MP = MPValue
        loop = True
        winCheck = False
    else:
        turn += 1
    canAction = True
    resetMain()
    level = int(level)
    turn = 0
    if HP < 0:
        HP = 0
    if eHP < 0:
        eHP = 0
    if eHP < 1:
        winCheck = True
        xp = xp + round(eHPValue + (eAttack + eStrongAttack) * 2)
        tkprint(log,"You gained {} xp, ({})".format(round(eHPValue + (eAttack + eStrongAttack) * 2),xp),"top")
        if xp >= xpRoof:
            storage = 0
            while xp >= xpRoof:
                level += 1
                xp -= xpRoof
                xpRoof = round(xpRoof * levelCurve)
                tkprint(log,"Level up! (" + str(level) + ")","top")
                storage += 1
            while storage > 0:
                storage -= 1
                levelUp()
        endCombat("win")
    if HP < 1:
        try:
            if winCheck == False:
                endCombat("lose")
        except:
            pass
    try:
        text.destroy()
    except:
        pass
    try:
        values.destroy()
    except:
        pass
    values = Label(main, text="{}/{}".format(round(HP), round(eHP)))
    values.pack(side="top")
    text = Label(main, text="What do you do?")
    text.pack(side="bottom")

def addChance(list,item,chance):
    x = chance
    while x > 0:
        list.append(item)
        x -= 1

enemyActions = []
addChance(enemyActions,"weakAttack",50)
addChance(enemyActions,"strongAttack",25)
addChance(enemyActions,"special",0)
addChance(enemyActions,"wait",25)

def secondPhase():
    global enemyChoice,HP,eAttack,eStrongAttack,turn,enemyActions
    turn += 1
    enemyChoice = random.choice(enemyActions)
    if enemyChoice == "weakAttack":
        damage = random.randint(round(eAttack - eAttack * 0.3), round(eAttack + eAttack * 0.3)) - round(defense / 2)
        HP -= damage
        tkprint(log, "{} does an attack (-{})".format(name, damage), "top")
    if enemyChoice == "strongAttack":
        damage = random.randint(round(eStrongAttack - eStrongAttack * 0.3),round(eStrongAttack + eStrongAttack * 0.3)) - round(defense / 2)
        HP -= damage
        tkprint(log,"{} does a strong attack (-{})".format(name,damage),"top")
    if enemyChoice == "special":
        tkprint(log, "{} does nothing".format(name), "top")
    if enemyChoice == "wait":
        pass
        tkprint(log, "{} does nothing".format(name), "top")
    mainPhase()
def saveGameFile(fileLocation):
    global save, user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack
    variables = [user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack]
    if not os.path.isfile(fileLocation):
        tkprint(log,"Savefile not found","top")
        tkprint(log,"Creating new savefile","top")
        with open(fileLocation, 'x') as f:
            f.write("")
    if save == -1:
        if not os.path.isfile(fileLocation):
            with open(fileLocation, 'x') as f:
                f.write("")
        save = sum(1 for _ in open(fileLocation)) + 1
        with open(fileLocation, 'a') as f:
            f.writelines("\n")
        save = sum(1 for _ in open(fileLocation))
    with open(fileLocation, 'r') as f:
        lines = f.readlines()
    if 1 <= save <= len(lines):
        lines[save - 1] = ','.join(map(str, variables)) + '\n'
    with open(fileLocation, 'w') as f:
        f.writelines(lines)
    if "savebutton" in globals():
        savebutton.destroy()

def endCombat(result):
    global log_bottom, savebutton, save, file, cont, canAction, xp, xpRoof, levelCurve, level, HPValue, defense, eHP, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, fileLocation
    if result == "win":
        tkprint(log,"You win!","top")
        eHPValue = round(eHPValue * 1.01,1)
        if eDefense == 0:
            eDefense = 1
        else:
            eDefense = round(eDefense * 1.01,1)
        eAttack = round(eAttack * 1.01,1)
        eStrongAttack = round(eStrongAttack * 1.01,1)
    if result == "lose":
        tkprint(log,"You lose!","top")
        tkprint(log, "Stats reset", "top")
        xp = 0
        xpRoof = 90
        levelCurve = 1.25
        level = 0
        HPValue = 20
        defense = 0
        eHPValue = 14
        eDefense = 0
        attackValue = 5
        magicValue = 3
        MPValue = 15
        eAttack = 3.5
    canAction = False
    try:
        log_bottom.destroy()
    except:
        pass
    log_bottom = Frame(log)
    log_bottom.pack(side="top")
    savebutton = tkbutton(log_bottom, "Save", lambda:saveGameFile(file), "left")
    cont = tkbutton(log_bottom,"Continue",newCombat,"left")

saveCheck = Tk()
saveCheck.title("Save Check")
saveCheck.minsize(150, 190)
saveCheck.geometry("150x190+50+50")

def hasSavefile(result):
    global file
    frame_top.destroy()
    label.destroy()
    if result == True:
        def finish():
            global file
            if not entry.get() == "":
                file = entry.get()
            else:
                file = "savefile.txt"
            deleteAll(saveCheck)
            save = 1
            if not sum(1 for _ in open(file)) > 1:
                user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attack, magic, MPValue, eAttack, eStrongAttack = readFile(file, save - 1).split(",")
                xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attack, magic, MPValue, eAttack, eStrongAttack = [float(var) for var in (xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attack, magic, MPValue,eAttack, eStrongAttack)]
                saveCheck.destroy()
            else:
                def savefile(number):
                    global file, save, user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack
                    save = int(number.split(" ")[0])
                    saveCheck.destroy()
                    user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack = readFile(file, save - 1).split(",")
                    xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack = [float(var) for var in (xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attack, magic, MPValue, eAttack, eStrongAttack)]
                Label(saveCheck,text="Multiple savefiles detected, which one do you want to use? Most recent: {}".format(readFile("extradata.txt",0)),wraplength=150).pack(side="top")
                saves = []
                x = 0
                while len(saves) < sum(1 for _ in open(file)):
                    saves.append("{} - {}".format((x + 1),readFile(file,x).split(",")[0]))
                    x += 1
                [Button(saveCheck, text=item, command=lambda i=item: savefile(i)).pack(side="top") for item in saves]
        Label(saveCheck, text="Where is your savefile located? Leave blank for default", wraplength=150).pack(side="top")
        entry = Entry(width=15)
        entry.pack(side="top")
        Button(saveCheck, text="Continue", command=finish).pack(side="top")
    else:
        if result == False:
            def finish():
                global save, file, user,xp,xpRoof,levelCurve,level,HPValue,defense,eHPValue,eDefense,attackValue,magicValue,MPValue,eAttack,eStrongAttack
                file = "savefile.txt"
                save = -1
                if not entry.get() == "":
                    user = entry.get().replace(" ","_")
                else:
                    user = "Unnamed"
                xp = 0
                xpRoof = 90
                levelCurve = 1.25
                level = 0
                HPValue = 20
                defense = 0
                eHPValue = 14
                eDefense = 0
                attackValue = 5
                magicValue = 3
                MPValue = 15
                eAttack = 3.5
                eStrongAttack = 5.5
                file = "savefile.txt"
                saveGameFile(file)
                saveCheck.destroy()
            Label(saveCheck, text="What name do you want for your savefile?", wraplength=150).pack(side="top")
            entry = Entry(saveCheck, width=15)
            entry.pack(side="top")
            Button(saveCheck, text="Finish", command=finish).pack(side="top")

label = Label(saveCheck, text="Do you have a savefile")
label.pack(side="top")
frame_top = Frame(saveCheck)
frame_top.pack(side="top")
Button(frame_top,text="Yes",command=lambda:hasSavefile(True)).pack(side="left")
Button(frame_top,text="No",command=lambda:hasSavefile(False)).pack(side="left")
saveCheck.mainloop()

main = Tk()
main.title("New! Text-based RPG")
main.minsize(200, 100)
main.geometry("300x100+50+50")

log = Tk()
log.title("Log")
log.minsize(175, 300)
log.geometry("175x300+375+50")

frame_bottom = Frame(main)
frame_bottom.pack(side="bottom")

canContinue = True
winCheck = False
skills = []
variables = [user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack]
atkButton = tkbutton(frame_bottom, "Attack", lambda: attack(), "left")
magButton = tkbutton(frame_bottom, "Magic", lambda: perform_action("Magic"), "left")
sctButton = tkbutton(frame_bottom, "Scout", lambda: perform_action("Scout"), "left")
def newCombat():
    global eHP,loglabel,cont,loop,canContinue,name,race
    if canContinue == True:
        loop = False
        name = getName()
        race = getRace(1)
        eHP = eHPValue
        try:
            loglabel.destroy()
            for widget in log.winfo_children():
                widget.destroy()
        except:
            pass
        try:
            cont.destroy()
        except:
            pass
        loglabel = tkprint(main, "{} the {} attacks you!".format(name, race), "top")
        tkprint(log, "{} the {} attacks you!".format(name, race), "top")
        mainPhase()

newCombat()
main.mainloop()
