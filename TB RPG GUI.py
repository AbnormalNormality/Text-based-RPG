from tkinter import Tk, Label, Button
from tkinter.ttk import *
import random
import ctypes
import os
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)  # 6 corresponds to SW_MINIMIZE

def readFile(file,x):
    try:
        with open(file, "r") as file:
            for _ in range(x + 1):
                x_line = file.readline()
        return x_line.strip()
    except:
        pass

def saveGameFile(fileLocation):
    if not os.path.isfile(fileLocation):
        with open(fileLocation, 'w') as f:
            f.write("")
    save = sum(1 for _ in open(fileLocation)) + 1
    with open(fileLocation, 'a') as f:
        f.writelines("\n")
        print("Balls")
    with open(fileLocation, 'r') as f:
        lines = f.readlines()
    if 1 <= save <= len(lines):
        lines[save - 1] = ','.join(map(str, variables)) + '\n'
    with open(fileLocation, 'w') as f:
        f.writelines(lines)

def tkprint(window, yourText, side):
    label = Label(window, text=yourText)
    label.pack(side=side)
    return label

def tkbutton(window, text, command, side, **kwargs):
    button = Button(window, text=text, command=command, **kwargs)
    button.pack(side=side)
    return button

def getName():
    global name
    names = ["Bob","Jim Scarey","Apples","Corban","Oscar","Charlie","Alia","Spencer","Avery","Sophie","Chris Snack"]
    name = random.choice(names)
    return name

def getRace():
    global race
    races = ["Goblin", "Dragon", "Troll", "Mage", "Warrior", "Rogue", "Golem", "Peasant","Fangirl"]
    race = random.choice(races)
    return race

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
    print(f"Button clicked: {item}")
    secondPhase()

def scout(target):
    global user,HP,attackValue,magicValue,MPValue,defense,name,eHP,eAttack,eStrongAttack,eDefense
    if target == "player":
        Label(log,text="{}: {}, {}, {}, {}, {}".format(user,HP,attackValue,magicValue,MPValue,defense)).pack(side="top")
    if target == "enemy":
        Label(log,text="{}: {}, {}, {}, {}".format(name,eHP,eAttack,eStrongAttack,eDefense)).pack(side="top")
    mainPhase()

def perform_action(action):
    global text,canAction
    if canAction == True:
        text.destroy()
        deleteButtons(frame_bottom)
        Button(frame_bottom, text="Back", command=lambda: mainPhase()).pack(side="left")
        if action == "Magic":
            text = Label(main, text="What ability do you want to use?")
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
    global text, level, values, eHP, xp, xpRoof, canAction, HPValue, eHPValue, HP, loop, winCheck
    if not "loop" in globals() or loop == False:
        HP = HPValue
        eHP = eHPValue
        loop = True
        winCheck = False
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
                if level >= 2:
                    skills.append("Heal")
                if level >= 5:
                    skills.append("Fireball")
                if level >= 8:
                    skills.append("Lightning")
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

def secondPhase():
    global enemyChoice,HP,eAttack,eStrongAttack,attackChance,strongAttackChance,specialChance,waitChance
    enemyChoice = random.randint(1, 100)
    if enemyChoice <= attackChance:
        # Weak attack
        damage = random.randint(round(eAttack - eAttack * 0.3), round(eAttack + eAttack * 0.3)) - round(defense / 2)
        HP -= damage
        tkprint(log, "{} does an attack (-{})".format(name, damage), "top")
    if enemyChoice > attackChance and enemyChoice <= strongAttackChance:
        # Strong attack
        damage = random.randint(round(eStrongAttack - eStrongAttack * 0.3),round(eStrongAttack + eStrongAttack * 0.3)) - round(defense / 2)
        HP -= damage
        tkprint(log,"{} does a strong attack (-{})".format(name,damage),"top")
    if enemyChoice > strongAttackChance and enemyChoice <= specialChance:
        # Special
        tkprint(log, "{} does nothing".format(name), "top")
    if enemyChoice > specialChance:
        # Wait
        tkprint(log, "{} does nothing".format(name), "top")
    mainPhase()

def endCombat(result):
    global cont, canAction, xp, xpRoof, levelCurve, level, HPValue, defense, eHP, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance
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
        eStrongAttack = 5.5
        attackChance = 25
        strongAttackChance = 50
        specialChance = 75
        waitChance = 100
    canAction = False
    try:
        log_bottom.destroy()
    except:
        pass
    log_bottom = Frame(log)
    log_bottom.pack(side="top")
    cont = tkbutton(log_bottom, "Save", saveGameFile, "left")
    cont = tkbutton(log_bottom,"Continue",newCombat,"left")

gateVariable = False

user = ""
canDestroy = False

saveCheck = Tk()
saveCheck.title("Save Check")
saveCheck.minsize(150, 190)
saveCheck.geometry("150x190+50+50")

frame_bottom = Frame(saveCheck)
frame_bottom.pack(side="bottom")

frame_top = Frame(saveCheck)

def passCheck(*forcePass):
    global gateVariable, user, hasSavefile,canDestroy
    if forcePass:
        saveCheck.destroy()
    gateVariable = True
    if hasSavefile == "no":
        user = userInput.get()
        saveCheck.destroy()

def afterInput():
    global user
    if userInput.get() == "":
        saveLocation = "savefile.txt"
    else:
        saveLocation = userInput.get()

    def multisavefile(save):
        try:
            save = int(save)
            if 0 <= save <= sum(1 for _ in open(saveLocation)):
                saveSafe = True
                if save == 0:
                    save = int(readFile(r"extradata.txt", 0))
            else:
                saveSafe = False
        except:
            saveSafe = False
        if saveSafe == True:
            global user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance
            user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance = readFile(
                saveLocation, int(save) - 1).split(",")
            xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance = [
                float(var) for var in (
                xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack,
                eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance)]
            passCheck("pass")
    if sum(1 for _ in open(saveLocation)) > 1:
        global multisave
        if not "multisave" in globals():
            label1 = Label(text="Multiple savefiles detected, which one do you want to use? Use file 0 for the most recent save ({})".format(
                str(sum(1 for _ in open(saveLocation)))), wraplength=150)
            label1.pack(side="top")
            multiSave = Entry(saveCheck, width=15)
            multiSave.pack(side="top")
            finish.destroy()
            button1 = Button(saveCheck, text="Load savefile", command=lambda: print(multiSave.get()) or multisavefile(multiSave.get()))
            button1.pack(side="bottom")
    else:
        save = 1
        user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance = readFile(saveLocation, save - 1).split(",")
        xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance = [float(var) for var in (xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack,eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance)]
        passCheck("pass")

def savefile(choice):
    global userInput,hasSavefile
    deleteButtons(frame_top)
    textLabel.destroy()
    if choice == "yes":
        hasSavefile = "yes"
        frame_top.destroy()
        Label(saveCheck, text="Where is your savefile located?", wraplength=150).pack(side="top")
        userInput = Entry(saveCheck, width=20)
        userInput.pack(side="top")
        enterFile = Button(saveCheck, text="Continue", command=afterInput)
        enterFile.pack(side="top")
    if choice == "no":
        hasSavefile = "no"
        frame_top.destroy()
        Label(saveCheck,text="What name do you want for your savefile?",wraplength=150).pack(side="top")
        userInput = Entry(saveCheck,width=20)
        userInput.pack(side="top")

textLabel = Label(saveCheck, text="Do you have a savefile?")
textLabel.pack(side="top")
frame_top.pack(side="top")
Button(frame_top,text="Yes",command=lambda: savefile("yes")).pack(side="left")
Button(frame_top,text="No",command=lambda: savefile("no")).pack(side="left")
finish = Button(saveCheck,text="Finish",command=passCheck)
finish.pack(side="bottom")
saveCheck.mainloop()

while not gateVariable:
    pass

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
if hasSavefile == "no":
    xp = 0
    xpRoof = 90
    levelCurve = 1.25
    level = 0
    HPValue = 20
    HP = 20
    defense = 0
    eHPValue = 14
    eDefense = 0
    attackValue = 5
    magicValue = 3
    MPValue = 15
    eAttack = 3.5
    eStrongAttack = 5.5
    attackChance = 25
    strongAttackChance = 50
    specialChance = 75
    waitChance = 100
    file = "savefile.txt"
if hasSavefile == "yes":
    pass

variables = [user, xp, xpRoof, levelCurve, level, HPValue, defense, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance]
atkButton = tkbutton(frame_bottom, "Attack", lambda: attack(), "left")
magButton = tkbutton(frame_bottom, "Magic", lambda: perform_action("Magic"), "left")
sctButton = tkbutton(frame_bottom, "Scout", lambda: perform_action("Scout"), "left")
def newCombat():
    global eHP,loglabel,cont,loop,canContinue
    if canContinue == True:
        loop = False
        name = getName()
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
        loglabel = tkprint(main, "{} the {} attacks you!".format(getName(), getRace()), "top")
        tkprint(log, "{} the {} attacks you!".format(name, race), "top")
        mainPhase()

newCombat()

main.mainloop()