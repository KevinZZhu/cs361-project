# Course: CS-361
# Name: Sam Pai
# Assignment: Sprint 3 - Life Generator
# Description: A Python program that uses Tkinter as the GUI to display toy data to the user.

from tkinter import *
import csv


def GUI(categories, data):
    """ This is the function that handles all the GUI processes (using TKinter) for grabbing user input
    for category and desired  output number. After user clicks submit, then program extracts the right data
      from Kaggle and then outputs to the Tkinter GUI as well as outputs an output.csv file in same directory."""
    category = []
    toyCount = []
    root = Tk()

    variable = StringVar(root)
    variable.set(categories[3])
    menu = OptionMenu(root, variable, *categories)
    menu.pack()

    def ok():
        print("Drop Down Menu: ", variable.get())
        print("Number of Toys: ", entry1.get())
        category.append(variable.get())
        toyCount.append(entry1.get())

        # here we need to output the results onto the GUI
        outputData = getDesiredData2(variable.get(), entry1.get(), data)
        titles = Label(root, text="input_item_type, input_item_category, input_number_to_generate, output_item_name, output_item_rating, output_item_num_reviews")
        titles.pack()
        for row in outputData:
            row = str(row)
            values = Label(root, text=row)
            values.pack()

    inputLabel = Label(root, text="Number of Toys")
    inputLabel.pack(side= LEFT)
    entry1 = Entry(root, bd=5)
    entry1.pack(side=RIGHT)

    button = Button(root, text="Submit", command=ok)
    button.pack(side=BOTTOM)

    root.mainloop()

    return category[0], toyCount[0]


def sortData(toys, toyCount, category):
    """ This function accepts the collection of toys, the desired toy count, and the category of these toys. It then
    sorts this data based on the top 10 algorithm and creates an output.csv file. It says returns a list of the
    final results so that the GUI function can use it. """
    # first sort by the uniq id
    toys.sort()

    # then sorted by number of reviews, if the review nummber is '', I just replaced it with 0 so it's at the bottom
    toys.sort(key=lambda x: int(x[5]) if x[5].isnumeric() == True else 0, reverse=True)

    num = int(toyCount) * 10

    sorted1 = []
    # grabbing the top X * 10 toys, so this loop runs toyCount * 10 times.
    for _ in range(num):
        # if there are still items in the original toys input, then we append to the sorted1 which will have x*10 items
        if toys:
            sorted1.append(toys.pop(0))
        else:
            break
    # this target represents the actual number of ____ category items there are
    target = len(sorted1)
    counter = 1

    # then making sure it is sorted by uniq_id again
    sorted1.sort()

    # sorted by review rating
    sorted1.sort(key=lambda y: float(y[7].split(" ")[0]), reverse=True)
    finalOutPut = []
    for toy in range(int(toyCount)):
        # this is needed in the case of when the user wants more output rows than there are available.
        if counter > target:
            break
        #                                       output item name, output item rating, output item number of reviews
        collection = ['Toys', category, toyCount, sorted1[toy][1], sorted1[toy][7], sorted1[toy][5]]
        finalOutPut.append(collection)
        counter += 1

    # creates the output.csv file with the sorted data.
    with open("lg_output.csv", mode="w") as output_file:
        outputWriter = csv.writer(output_file, delimiter=",")
        outputWriter.writerow(["input_item_type", "input_item_category", "input_number_to_generate", "output_item_name",
                               "output_item_rating", "output_item_num_reviews"])
        for row in finalOutPut:
            outputWriter.writerow(row)

    return finalOutPut


def getDesiredData(category, toyCount, allToys):
    """Function for getting the data that matches the input category and toy count. This is only for
    INPUT CSV data, and not the user entered data from GUI."""
    category = category.split("=")[1]
    toyCount = toyCount.split("=")[1]
    toys = []  # ALL TOYS FROM KAGGLE
    filteredToys = []  # ONLY TOYS THAT MATCH INPUT CATEGORY
    for row in allToys:
        toys.append(list(row))
    for toy in toys:
        if toy[8].split(" >")[0].lower() == category.lower():
            filteredToys.append(toy)
    toys.clear()  # clearing the toys list to save memory
    sortData(filteredToys, toyCount, category)


def getDesiredData2(category, toyCount, allToys):
    """Function for getting the data that matches the input category and toy count entered in by user from Tkinter."""

    toys = []  # ALL TOYS FROM KAGGLE
    filteredToys = []  # ONLY TOYS THAT MATCH INPUT CATEGORY
    for row in allToys:
        toys.append(list(row))
    for toy in toys:
        if toy[8].split(" >")[0].lower() == category.lower():
            filteredToys.append(toy)
    toys.clear()
    return sortData(filteredToys, toyCount, category)

selected_category = None
selected_count = None


with open("amazon_co-ecommerce_sample 2.csv", "r") as file:
    data = csv.reader(file)

    # IF an input.csv file is provided, code will enter the try block
    try:
        with open("input.csv", "r") as input_file:

            input_data = csv.reader(input_file)
            for row in input_data:
                item_category = row[1]
                num_toys = row[2]
                getDesiredData(item_category, num_toys, data)
    # IF an input.csv file is NOT provided, then code will enter the except block to use the GUI.
    except:
        print("in except")
        allCategories = set()  # using a set so there are no duplicate categories.
        allData = []  # will store all the toy data from Kaggle CSV file.
        for row in data:
            allData.append(list(row))
            categories = row[8].split(" >")[0]
            allCategories.add(categories)
        allCategories = list(allCategories)  # changing the set into a list
        allCategories = [x for x in allCategories if x != '']  # only grabbing categories with a name

        data = allData
        GUI(allCategories, data)


