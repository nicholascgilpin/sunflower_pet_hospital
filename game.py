import json
from os import listdir
from os.path import isfile, join
import os
import sys

# Globals
story = None
life = 3
test_budget = 10

def load_story(file):
    with open(file) as fp:
        data = fp.read()
        return json.loads(data)

def clear():
    # os.system('cls')
    for line in range(0,5):
        print("\n")

def show_intro():
    clear()
    print("\n")
    print(story["title"])
    print("\n")
    print(story["intro"])

def order_test():
    global test_budget
    if test_budget < 1:
        show_loss("You client has run out of money. The patient dies!")

    print("\nBudget for tests: ", test_budget)
    print("\nSelect a test to order:\n")

    test_budget = test_budget - 1
    choices = []

    for i, test in enumerate(dict(story["case"]["tests"]).keys()):
        print(i+1, ") ", test)
        choices.append(test)

    while True:
        selection = int(input())
        if selection < 1 or selection > len(choices):
            print("Invalid choice. Try again.")
        else:
            return choices[selection-1]

def input_choices():
    pass

def show_result(test):
    print("\nYou call your tech Sarah to assist with the test.")
    print("Result:\n", story["case"]["tests"][test])

def show_play_menu():
    while True:
        print("\nChoose an action:")
        print("  1) Order a test")
        print("  2) Attempt Treatment")
        print("  3) Review Case")

        action = input()
        if str(action) == "":
            print("Invalid choice")
        elif int(action) < 1 or int(action) > 3:
            print("Invalid choice. Try again.")
        else:
            return int(action)

def show_win():
    clear()
    print("YOU WIN!")
    print("\nCongradulations! You have healed your patient, the client loves you, and you're a great Vet! ")
    sys.exit(0)

def show_loss(msg):
    clear()
    print("\nGAME OVER!\n")
    print(msg)
    print("\nRestart program to try again.")

    sys.exit(0)

def treat():
    global life
    disease = story["case"]["correct_dianosis"]

    choices = [disease]
    for test in story["case"]["possible_diagnosis"]:
        choices.append(test)

    for j, choice in enumerate(sorted(choices)):
        print(j+1, ") ", choice)

    while True:
        selection = int(input())
        if selection < 1 or selection > len(choices):
            print("Invalid choice. Try again.")
        else:
            break

    if str(sorted(choices)[selection-1]).lower() == disease.lower():
        show_win()
    else:
        life = life - 1
        if life < 1:
            show_loss("Oh no! Your patient died!")
        else:
            print("\nPatient doesn't seem to be responding to treatment")


def choose_story():
    global story
    global life
    global test_budget

    mypath = "./stories/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    print("Choose a story to begin:")
    for i, file in enumerate(onlyfiles):
        print(i+1, ") ", load_story(mypath + file)["title"])
    choice = int(input())
    story = load_story(mypath + onlyfiles[choice-1])
    life = int(story["case"]["life_guesses"])
    test_budget = int(story["case"]["test_budget"])

# test
# choose_story()

if __name__ == "__main__":
    print("\nWelcome to Sunflower Pet Hospital!\n")
    choose_story()
    show_intro()
    while True:
        action = show_play_menu()
        if action == 1:
            test = order_test()
            show_result(test)
        elif action == 2:
            treat()
        elif action == 3:
            show_intro()
        else:
            print("Invalid action")
    # try:
    # except:
    #     print("Error: The world has ended. Please restart the program.")
