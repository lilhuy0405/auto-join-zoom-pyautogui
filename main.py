import pyautogui
import os
import time
import sys
from tabulate import tabulate
from datetime import datetime
from data import classes

pyautogui.FAILSAFE = True
zoomPath = 'C:\\Users\\luuhu\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe'
joinBtnImagePath = 'images/join-btn.png'
idInputImagePath = 'images/id-input.png'
nameInputImagePath = 'images/name-input.png'
passwordInputImagePath = 'images/pwd-input.png'

zoomName = '08_19F7_Luwu DDuwsc Huy'


def openZoom(path):
    os.startfile(path)


def locateElement(imagePath):
    failCount = 0
    maxFailCount = 100
    while True:
        res = pyautogui.locateCenterOnScreen(imagePath, confidence=.5)
        if res is not None:
            print("finding element", imagePath)
            return res
        failCount = failCount + 1
        print("Failed to find", imagePath,  str(failCount),
              "times", "will try again after 1 second")
        time.sleep(1)
        if failCount == maxFailCount:
            return None


def clickOnAnElement(imagePath):
    res = locateElement(imagePath)
    if res is None:
        sys.exit("Can not found the element", imagePath)
    pyautogui.click(x=res.x, y=res.y)


def joinZoomMeeting(id, name, password):
    # open zoom and click join
    openZoom(zoomPath)
    clickOnAnElement(joinBtnImagePath)
    # enter meeting ID
    clickOnAnElement(idInputImagePath)
    pyautogui.typewrite(id, interval=.1)
    # enter meeting name
    clickOnAnElement(nameInputImagePath)
    pyautogui.press('backspace', presses=50)
    pyautogui.typewrite(name+'\n', interval=.1)

    # enter meeting password
    if len(password) > 0:
        clickOnAnElement(passwordInputImagePath)
        pyautogui.press('backspace', presses=50)
        pyautogui.typewrite(password+'\n', interval=.1)


def convertHourToMinute(h, m):
    return h * 60 + m


def getClassHour(minute):
    breakpoint1 = convertHourToMinute(6, 50)
    breakpoint2 = convertHourToMinute(9, 30)
    breakpoint3 = convertHourToMinute(12, 30)
    breakpoint4 = convertHourToMinute(14, 40)
    classTime = -1
    if minute < breakpoint1:
        classTime = -1
    elif minute >= breakpoint1 and minute < breakpoint2:
        classTime = 1
    elif minute >= breakpoint2 and minute < breakpoint3:
        classTime = 2
    elif minute >= breakpoint3 and minute < breakpoint4:
        classTime = 3
    else:
        classTime = -1
    return classTime


def findClass(weekday, classHour):
    for clazz in classes:
        ca = clazz[3]
        thu = clazz[2]
        if ca == 'unknown' and thu == 'unknown':
            continue
        if int(ca) == int(classHour) and int(thu) == int(weekday):
            return clazz
    return None


def main():
    print("Welcome to join zoom tool")
    print(tabulate(classes, headers=['Stt', 'Mon', 'Thu', 'Ca', 'Tiet', 'ID', 'Password'], tablefmt='grid'))

    now = datetime.now()
    hour = int(now.hour)
    minute = int(now.minute)

    classPickByTime = findClass(int(now.weekday()) + 2, getClassHour(convertHourToMinute(hour, minute)))
    if classPickByTime is not None:
        print("\nNow is", now.strftime('%A %H:%M'))
        print("Your current class supposed to be")
        print(tabulate([classPickByTime], headers=['Stt', 'Mon', 'Thu', 'Ca', 'Tiet', 'ID', 'Password'], tablefmt='grid'))
        confirm = input("Do you want to join this class (y/n): ")
        if confirm == 'y':
            chosenCourseId = classPickByTime[5]
            chosenCoursePassword = classPickByTime[6]
            joinZoomMeeting(chosenCourseId, zoomName, chosenCoursePassword)
            print("Join success")
            return 0
    courseId = int(input("Enter class want to join: "))
    chosenCourse = classes[courseId - 1]
    print("joining course: ", chosenCourse[1], "....")
    print(tabulate([chosenCourse], headers=['Stt', 'Mon', 'Thu','Ca', 'Tiet', 'ID', 'Password'], tablefmt='grid'))
    chosenCourseId = chosenCourse[5]
    chosenCoursePassword = chosenCourse[6]
    joinZoomMeeting(chosenCourseId, zoomName, chosenCoursePassword)
    print("Join success")
    return 0

main()
