from tkinter import Tk, Label, Button
from tkinter.ttk import *
import random

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
    names = ["Bob"]
    name = random.choice(names)
    return name

def getRace():
    global race
    races = ["Goblin", "Dragon", "Troll", "Mage", "Warrior", "Rogue", "Golem", "Peasant"]
    race = random.choice(races)
    return race

def attack():
    global eHP, name, canAction
    if canAction == True:
        damage = random.randint(round(attackValue - attackValue * 0.3), round(attackValue + attackValue * 0.3)) - round(eDefense / 2)
        eHP -= damage
        tkprint(log, "You attack {} (-{})".format(name,damage), "top")
        secondPhase()
    else:
        pass

def perform_action(action):
    global text,canAction
    if canAction == True:
        text.destroy()
        if action == "Magic":
            text = Label(main, text="What ability do you want to use?")
            text.pack(side="bottom")
        elif action == "Scout":
            text = Label(main, text="Who do you want to scout")
            text.pack(side="bottom")
    else:
        pass
def mainPhase():
    global text, level, values, eHP, xp, xpRoof, canAction
    canAction = True
    level = int(level)
    turn = 0
    HP = HPValue
    MP = MPValue
    if HP < 0:
        HP = 0
    if eHP < 0:
        eHP = 0
    if eHP <= 1:
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
                #levelUp()
        endCombat("win")
    if HP <= 1:
        endCombat("lose")
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
    enemyChoice = random.randint(1, 100)
    mainPhase()

def endCombat(result):
    global cont, canAction, xp, xpRoof, levelCurve, level, HPValue, defense, eHP, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance
    if result == "win":
        tkprint(log,"You win!","top")
        eHPValue = round(eHPValue * 1.05,1)
        if eDefense == 0:
            eDefense = 1
        else:
            eDefense = round(eDefense * 1.05,1)
        eAttack = round(eAttack * 1.05,1)
        eStrongAttack = round(eStrongAttack * 1.05,1)
    if result == "lose":
        tkprint(log,"Lose!","top")
        xp = 0
        xpRoof = 100
        levelCurve = 2.05
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
    cont = tkbutton(log,"Continue?",newCombat,"top")
global user, xp, xpRoof, levelCurve, level, HPValue, defense, eHP, eHPValue, eDefense, attackValue, magicValue, MPValue, eAttack, eStrongAttack, attackChance, strongAttackChance, specialChance, waitChance
user = "Alia"
xp = 0
xpRoof = 100
levelCurve = 2.05
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
tkbutton(frame_bottom, "Attack", lambda: attack(), "left")
tkbutton(frame_bottom, "Magic", lambda: perform_action("Magic"), "left")
tkbutton(frame_bottom, "Scout", lambda: perform_action("Scout"), "left")
def newCombat():
    global eHP,loglabel,cont
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