#!/usr/bin/python
import sys
import csv
import datetime

  
# COMPSCI 383 Homework 0 
#  
# Fill in the bodies of the missing functions as specified by the comments and docstrings.


# Exercise 0. (8 points)
#  
def read_data(file_name):
    """Read in the csv file and return a list of tuples representing the data.

    Transform each field as follows:
      date: datetime.date
      mileage: integer
      location: string
      gallons: float
      price: float (you'll need to get rid of the '$')

    Do not return a tuple for the header row.  While you can process the raw text using string
    functions, to receive full credit you must use Python's built in csv module.

    If the field is blank, you should put a None value in the tuple for that field (for the 
    other functions below, you'll need to check for None values when making calculations).  

    Hint: to parse the date field, use the strptime function in the datetime module, and then
    use datetime.date() to create a date object.

    See: 
      https://docs.python.org/3/library/csv.html
      https://docs.python.org/3/library/datetime.html

    """
    rows = []  # this list should contain one tuple per row

    with open('mustard_data.csv') as csvfile:
        mustard = csv.reader(csvfile, delimiter=',')            # opens csv file, separating
        next(mustard)                                           # eliminates header

        for row in mustard:                                     # iterate through CSV with row variable
            if row[0] == "":                                    # checks for blanks in CSV
                date_obj = None                                 # sets variable to None for empty cells
            else:                                               # else cell is not empty
                # converts string to datetime object, denoting string format used in cell
                date_obj = datetime.datetime.strptime(str(row[0]), "%m/%d/%Y").date()

            if row[1] == "":
                mileage = None
            else:
                mileage = int(row[1])                           # first value in row is mileage, save and cast as int

            if row[2] == "":
                location = None
            else:
                location = str(row[2])                          # second index in row is location, save and cast as str

            if row[3] == "":
                gallons = None
            else:
                gallons = float(row[3])                         # third index in row is gallons, save and cast as float

            if row[4] == "":
                price = None
            else:
                strPrice = row[4]                               # fourth index in row is price, save as str
                price = float(strPrice.replace('$', ''))        # replace '$' char with nothing to eliminate

            data = (date_obj, mileage, location, gallons, price)  # set a tuple of the extracted data
            rows.append(data)                                   # append tuple to rows

    return rows  # a list of (date, mileage, location, gallons, price) tuples


# Exercise 1. (5 points)
#
def total_cost(rows):
    """Return the total amount of money spent on gas as a float.
    
    Hint: calculate by multiplying the price per gallon with the  number of gallons for each row.
    """

    total = 0                                       # initial total

    for data in rows:                               # iterate through rows list with data representing tuples
        if data[3] is None or data[4] is None:      # check to make sure data exists
            total += 0                              # do nothing if data does not exist
        else:
            total += data[3] * data[4]              # else compute price for fill up and increment total by this amount

    return total


# Exercise 2. (5 points)
#
def num_single_locs(rows):
    """Return the number of refueling locations that were visited exactly once.
    
    Hint: store the locations and counts (as keys and values, respectively) in a dictionary, 
    then count up the number of entries with a value equal to one.  
    """

    dict = {}                       # empty dictionary
    num = 0                         # initial number of unique visits

    for data in rows:               # iterate through rows with data representing tuples
        location = data[2]          # save location from tuple for readability
        if location in dict:        # check if location has been logged
            dict[location] += 1     # increment visit count if yes
        else:
            dict[location] = 1      # else log location and set visit count to 1

    for location in dict:           # iterate throuhg logged locations
        if dict[location] == 1:     # check if each location has been visited once
            num += 1                # increment counter

    return num


# Exercise 3. (8 points)
#
def most_common_locs(rows):
    """Return a list of the 10 most common refueling locations, along with the number of times
    they appear in the data, in descending order.  
    
    Each list item should be a two-element tuple of the form (name, count).  For example, your
    function might return a list of the form: 
      [ ("Honolulu, HI", 42), ("Shermer, IL", 19), ("Box Elder, MO"), ... ]

    Hint: store the locations and counts in a dictionary as above, then convert the dictionary 
    into a list of tuples using the items() method.  Sort the list of tuples using sort() or 
    sorted().

    See:
      https://docs.python.org/3/tutorial/datastructures.html#dictionaries
      https://docs.python.org/3/howto/sorting.html#key-functions
    """

    dict = {}                           # dictionary to keep track of locations and number of visits
    locs = []                           # array to return

    for data in rows:                   # iterate through rows with data representing tuples
        location = data[2]              # store location in easy to read variable
        if location in dict:            # if location has been visited increase visit count by 1
            dict[location] += 1
        elif location is not None:      # else as long as the location exists, store it in dictionary and set visit to 1
            dict[location] = 1

    arr = dict.items()                  # store the pairs in an array as a tuple

    # sorted(to be sorted, telling sort to sort by value, reverse=True for descending order
    sortArr = sorted(arr, key=lambda x: x[1], reverse=True)

    i = 0
    while i < 10:                       # ensure it is the top most visited locations
        locs.append(sortArr[i])         # append the location and visit count to return array
        i += 1                          # increment i to break loop
    return locs


# Exercise 4. (8 points)
#
def state_totals(rows):
    """Return a dictionary containing the total number of visits (value) for each state as 
    designated by the two-letter abbreviation at the end of the location string (keys).  

    The return value should be a Python dictionary of the form:
      { "CA": 42, "HI": 19, "MA": 8675309, ... }

    Hint: to do this, you'll need to pull apart the location string and extract the state 
    abbreviation.  Note that some of the entries are malformed, and containing a state code but no
    city name.  You still want to count these cases (of course, if the location is blank, ignore
    the entry.
    """
    # instantiate variables
    state__count = {}
    arr = []
    abb = []
    visited = []

    for data in rows:                       # iterate through rows with data representing tuples
        location = data[2]                  # extract location
        if location is not None:            # check if location exists
            arr.append(location)            # append to array

    for i in arr:                           # iterate through array
        length = len(i)                     # store the length of the array in variable length
        abb.append(i[length-2: length])     # extract the last 2 characters (state abbreviations) and store in array

    for j in abb:                           # iterate through array of state abbreviations
        if j not in visited:                # if it is not in the visited array
            visited.append(j)               # append to visited array
            state__count[j] = 1             # set number of visits to 1
        else:
            state__count[j] += 1            # else state has been visited, increment counter by 1
    return state__count


# Exercise 5. (8 points)
#
def num_unique_dates(rows):
    """Return the total number unique dates in the calendar that refueling took place.

    That is, if you ignore the year, how many different days had entries? (This number should be 
    less than or equal to 366!)
 
    Hint: the easiest way to do this is create a token representing the calendar day.  These could
    be strings (using strftime()) or integers (using date.toordinal()).  Store them in a Python set
    as you go, and then return the size of the set.

    See:
      https://docs.python.org/3/library/datetime.html#date-objects
    """
    x = set()                                       # instantiate set

    for data in rows:                               # iterate through rows with data representing tuples
        if data[0] is not None:                     # ensure data exists
            date = data[0]                          # store date as variable for reability
            strDate = date.strftime("%m/%d/%Y")     # convert datatime object to string
            x.add(strDate)                          # add strings to set

    num = len(x)                                    # save length of set for return

    return num


# Exercise 6. (8 points)
#
def month_avg_price(rows):
    """Return a dictionary containing the average price per gallon as a float (values) for each 
    month of the year (keys).

    The dictionary you return should have 12 entries, with full month names as keys, and floats as
    values.  For example:
        { "January": 3.12, "February": 2.89, ... }

    See:
      https://docs.python.org/3/library/datetime.html
    """

    # definitely not the most efficient way, but accomplished the task

    # instantiate variables
    # used variables to sum the average price corresponding to a month
    # count the number of entries for that month
    # divide the total cost by the number of visits that month
    jan = 0.0
    janSum = 0.0

    feb = 0.0
    febSum = 0.0

    mar = 0.0
    marSum = 0.0

    apr = 0.0
    aprSum = 0.0

    may = 0.0
    maySum = 0.0

    jun = 0.0
    junSum = 0.0

    jul = 0.0
    julSum = 0.0

    aug = 0.0
    augSum = 0.0

    sept = 0.0
    septSum = 0.0

    oct = 0.0
    octSum = 0.0

    nov = 0.0
    novSum = 0.0

    dec = 0.0
    decSum = 0.0

    # dictionary of months with values set to 0.0
    # monthly_avg = {
    #     "January": 0.0,
    #     "February": 0.0,
    #     "March": 0.0,
    #     "April": 0.0,
    #     "May": 0.0,
    #     "June": 0.0,
    #     "July": 0.0,
    #     "August": 0.0,
    #     "September": 0.0,
    #     "October": 0.0,
    #     "November": 0.0,
    #     "December": 0.0
    # }

    monthly_avg = {}                                        # empty dictionary to store values for later

    for data in rows:                                       # iterate through rows with data representing tuples
        if data[0] is not None and data[4] is not None:     # check to make sure data exists
            date = data[0]                                  # extracts date from tuple
            strDate = date.strftime("%m/%d/%Y")             # creates a string of the date time object

            if strDate[0:2] == "12":                        # checks first 2 characters of string with month as an int
                decSum += data[4]                           # increase the average price total for specified month
                dec += 1.0                                  # increases visit count for that specified month by 1

            if strDate[0:2] == "11":
                novSum += data[4]
                nov += 1.0

            if strDate[0:2] == "10":
                octSum += data[4]
                oct += 1.0

            if strDate[0:2] == "09":
                septSum += data[4]
                sept += 1.0

            if strDate[0:2] == "08":
                augSum += data[4]
                aug += 1.0

            if strDate[0:2] == "07":

                julSum += data[4]
                jul += 1.0

            if strDate[0:2] == "06":

                junSum += data[4]
                jun += 1.0

            if strDate[0:2] == "05":

                maySum += data[4]
                may += 1.0

            if strDate[0:2] == "04":

                aprSum += data[4]
                apr += 1.0

            if strDate[0:2] == "03":

                marSum += data[4]
                mar += 1.0

            if strDate[0:2] == "02":

                febSum += data[4]
                feb += 1.0

            if strDate[0:2] == "01":

                janSum += data[4]
                jan += 1.0

    monthly_avg["January"] = janSum/jan         # calculates average cost per month and updates dictionary with
    monthly_avg["February"] = febSum/feb
    monthly_avg["March"] = marSum/mar
    monthly_avg["April"] = aprSum/apr
    monthly_avg["May"] = maySum/may
    monthly_avg["June"] = junSum/jun
    monthly_avg["July"] = julSum/jul
    monthly_avg["August"] = augSum/aug
    monthly_avg["September"] = septSum/sept
    monthly_avg["October"] = octSum/oct
    monthly_avg["November"] = novSum/nov
    monthly_avg["December"] = decSum/dec

    return monthly_avg


# EXTRA CREDIT (+10 points)
#
def highest_thirty(rows):
    """Return the start and end dates for top three thirty-day periods with the most miles driven.

    The periods should not overlap.  You should find them in a greedy manner; that is, find the
    highest mileage thirty-day period first, and then select the next highest that is outside that
    window).
    
    Return a list with the start and end dates (as a Python datetime object) for each period, 
    followed by the total mileage, stored in a tuple:  
        [ (1995-02-14, 1995-03-16, 502),
          (1991-12-21, 1992-01-16, 456),
          (1997-06-01, 1997-06-28, 384) ]
    """
    #
    # fill in function body here
    #
    return []


# The main() function below will be executed when your program is run.
# Note that Python does not require a main() function, but it is
# considered good style (as is including the __name__ == '__main__'
# conditional below)
#
def main(file_name):
    rows = read_data(file_name)
    print("Exercise 0: {} rows\n".format(len(rows)))

    cost = total_cost(rows)
    print("Exercise 1: ${:.2f}\n".format(cost))

    singles = num_single_locs(rows)
    print("Exercise 2: {}\n".format(singles))

    print("Exercise 3:")
    for loc, count in most_common_locs(rows):
        print("\t{}\t{}".format(loc, count))
    print("")

    print("Exercise 4:")
    for state, count in sorted(state_totals(rows).items()):
        print("\t{}\t{}".format(state, count))
    print("")

    unique_count = num_unique_dates(rows)
    print("Exercise 5: {}\n".format(unique_count))

    print("Exercise 6:")
    for month, price in sorted(month_avg_price(rows).items(),
                               key=lambda t: datetime.datetime.strptime(t[0], '%B').month):
        print("\t{}\t${:.2f}".format(month, price))
    print("")

    print("Extra Credit:")
    for start, end, miles in sorted(highest_thirty(rows)):
        print("\t{}\t{}\t{} miles".format(start.strftime("%Y-%m-%d"),
                                          end.strftime("%Y-%m-%d"), miles))
    print("")


#########################

if __name__ == '__main__':
    
    data_file_name = "mustard_data.csv" 
    main(data_file_name)




