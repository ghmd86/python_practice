# This is a sample Python script.
import time
import pygetwindow as gw
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pyautogui
import pytesseract

puzzles_survival = gw.getWindowsWithTitle('Puzzles & Survival')[0]


def click_confirm(box):
    confirm = pyautogui.locateOnScreen('confirm.png', limit=box, confidence=0.7)
    print('confirm', confirm)
    pyautogui.click(confirm)


def click_train():
    train = pyautogui.locateOnWindow('train.png', title=puzzles_survival.title, confidence=0.7)
    print('Train button', train)
    if train:
        pyautogui.click(train)


def train_troops(times):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {times}')  # Press Ctrl+F8 to toggle the breakpoint.
    time.sleep(2)
    print(gw.getAllTitles())

    print(gw.getActiveWindow().title)
    # puzzlesSurvival.activate()
    print(gw.getActiveWindow())
    print(pyautogui.position())
    # pyautogui.moveTo(1434, 1272)
    for x in range(times):
        print(x)
        # # click train
        click_train()
        time.sleep(1)
        # # click resource auto use
        cancelconfirm = pyautogui.locateOnWindow('cancelconfirm.png', title=puzzles_survival.title, confidence=0.7)
        print('Confirm Dialog', cancelconfirm)
        if (cancelconfirm):
            click_confirm(cancelconfirm)
            click_train()
        time.sleep(1)
        # click train again
        # pyautogui.click(x=1434, y=1272, clicks=1, interval=1)
        time.sleep(1)
        # click on the speedup
        speedup = pyautogui.locateOnWindow('speedup.png', title=puzzles_survival.title, confidence=0.7)
        print('Speedup', speedup)
        if speedup:
            pyautogui.click(speedup)
        time.sleep(1)
        autospeedup = pyautogui.locateOnWindow('autospeedup.png', title=puzzles_survival.title, confidence=0.6)
        print('autospeedup', autospeedup)
        if autospeedup:
            pyautogui.click(autospeedup)
        time.sleep(1)
        confirmbox = pyautogui.locateOnWindow('confirmbox.png', title=puzzles_survival.title, confidence=0.7)
        print('Confirm Box', confirmbox)
        if confirmbox:
            checkbox = pyautogui.locateOnScreen('checkbox.png', limit=confirmbox, confidence=0.7)
            print('checkbox', checkbox)
            if checkbox:
                pyautogui.click(checkbox)
            time.sleep(1)
            confirm = pyautogui.locateOnScreen('confirm.png', limit=confirmbox, confidence=0.7)
            print('confirm', confirm)
            if confirm:
                pyautogui.click(confirm)
        time.sleep(1)
        fivemin = pyautogui.locateOnWindow('fivemin.png', title=puzzles_survival.title, confidence=0.6)
        print('five mins location', fivemin)
        if fivemin:
            use = pyautogui.locateOnWindow('use.png', limit=fivemin, title=puzzles_survival.title, confidence=0.6)
            print('use location', use)
            if use:
                pyautogui.click(use)
        time.sleep(1)
        # click on auto speedup
        # pyautogui.click(x=1411, y=1306, clicks=1, interval=1)
        # Click on 5 min auto speed
        # pyautogui.click(x=1506, y=375, clicks=1, interval=1)
        # time.sleep(1)


# train_troops(1)
def findOnScreen(image, confidence=1.0):
    """

    :rtype: object
    """
    puzzles_survival.activate()
    time.sleep(1)
    return pyautogui.locateOnWindow(image=image, title=puzzles_survival.title, confidence=confidence)


def complete_helps(times):
    # Click on help all
    time.sleep(2)
    print(pyautogui.position())
    # puzzles_survival.activate()

    help_full = findOnScreen('helpfull.png', 0.9)
    print(help_full, times)
    pyautogui.click(help_full, clicks=times, interval=1)

    # if help1:
    #     for t in range(times):
    #         print(t)
    #         time.sleep(1)
    #         pyautogui.click(help1)


complete_helps(3)


def heal_troops(times):
    time.sleep(2)
    print(pyautogui.position())
    for t in range(times):
        clear = pyautogui.locateOnScreen("Clear.png", grayscale=True, confidence=0.8)
        if clear:
            pyautogui.click(clear)
            print(clear)
        plus = pyautogui.locateOnScreen('plus.png', confidence=0.8)
        if plus:
            pyautogui.click(plus)
            print(plus)
        heal = pyautogui.locateOnScreen('heal.png', confidence=0.8)

        if heal:
            pyautogui.click(heal)
            print(heal)
        time.sleep(1)
        helps = pyautogui.locateOnScreen('help.png')

        print("Help", helps)

        if helps:
            pyautogui.click(helps)
            print(helps)
        else:
            pyautogui.click(1229, 1317)
        time.sleep(4)


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':


# heal_troops(1)


def gather_food():
    print(pyautogui.position())
    # find world map button on screen

    world = pyautogui.locateOnScreen("world.png", region=(950, 1250, 500, 500))
    print(world)
    # click on world


# click on magnifying glass
# click on food icon
# select level
# click search
# click on the food spot
# click on gather button
# click on click Quick Select
# click Dispatch


# gather_food()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def findLowLevel():
    print(puzzles_survival.title)

    low_level = pyautogui.locateOnWindow(image='lowlvl.png', title=puzzles_survival.title, confidence=0.4)

    print(low_level)
    if low_level:
        print(low_level)


# findLowLevel()

def readText():
    print(pytesseract.image_to_string('img.png'))

# print(findOnScreen('world.png'))
# world = findOnScreen('helpfull.png')
# print('world',world)
# pyautogui.click(world)

# readText()
