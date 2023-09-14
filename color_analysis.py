from collections import Counter
from bs4 import BeautifulSoup
import numpy as np
import psycopg2

# Get the HTML data from the file
with open("templates/index.html", "r") as f:
    html_data = f.read()

# Creating a BeautifulSoup object
soup = BeautifulSoup(html_data, "html.parser")

# Finding the table element
table = soup.find("table")

# Finding the rows in the table
rows = table.find_all("tr")

# Initializing a dictionary to store the data
data = {}

# Looping over the rows
for row in rows:
    # Get the day and colors from the row
    day_data = row.find_all("td")

    if day_data is not None and len(day_data) > 1:
        day = day_data[0].text
        colors = day_data[1].text.split(", ")
        # Store the colors in the dictionary
        data[day] = colors
        # print(colors)


# Getting the mean color
def mean_color():
    # Getting the mean color per day
    for day, colors in data.items():
        counter = Counter(colors)
        mean_color = counter.most_common(1)[0][0]
        print(f"The most common shirt color on {day} is color {mean_color}")

    # Getting the overall mean color
    color_counts = Counter()

    for day, colors in data.items():
        # Updating the color counts
        color_counts.update(colors)

    # Finding the most common color overall
    overall_mean_color = color_counts.most_common(1)[0][0]
    print("")
    print(f"The overall  mean shirt color is color {overall_mean_color}")


# Getting the most common color
def most_common_color():
    color_counts = Counter()

    for day, colors in data.items():
        # Updating the color counts
        color_counts.update(colors)

    # Finding the most common color overall
    mean_color = color_counts.most_common(1)[0][0]

    print(f"The most common color overall is color {mean_color}")


# Getting the median color
def median_color(colors):
    # Sorting the colors
    sorted_colors = sorted(colors)

    # Getting the length of the colors list
    n = len(sorted_colors)

    # Checking if the length is even or odd
    if n % 2 == 0:
        # If even, the median is the average of the two middle elements
        median1 = sorted_colors[n // 2]
        median2 = sorted_colors[n // 2 - 1]
        median = (median1 + median2) / 2
    else:
        # If odd, the median is the middle element
        median = sorted_colors[n // 2]

    return median


# Printing the overall median color
def overall_median():
    all_colors = [color for day, colors in data.items() for color in colors]
    print(f"The median color is color {median_color(all_colors)}")


# Getting the variance of color
def color_to_number(color):
    return len(color)


def variance_color(colors):
    # Converting colors to numerical values
    numerical_colors = [color_to_number(color) for color in colors]

    # Calculating variance
    variance = np.var(numerical_colors)

    return variance


def variance():
    for day, colors in data.items():
        print(f"The variance of colors on {day} is {variance_color(colors)}")


def probability_of_red():

    # Getting all colors
    all_colors = [color for day, colors in data.items() for color in colors]

    # Counting the total number of colors
    total_colors = len(all_colors)

    # Counting the number of times 'red' appears
    red_count = all_colors.count('red')

    # Calculating the probability
    probability = red_count / total_colors

    print(f"The probability that the color is red is {probability}")


# Creating table and saving the color and frequencies
def color_table():
    # Defining the connection string
    conn_string = "host='localhost' dbname='test' user='postgres' password='localhost@password/test'"

    # Establishing a connection to the database
    conn = psycopg2.connect(conn_string)

    # Opening a cursor to perform database operations
    cur = conn.cursor()

    # Executing SQL command to create a table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS colors (
            color TEXT PRIMARY KEY,
            frequency INTEGER
        )
    """)

    # Committing changes
    conn.commit()

    # Counting the frequency of each color
    color_counts = Counter()
    for day, colors in data.items():
        color_counts.update(colors)

    # Inserting the data into the table
    for color, frequency in color_counts.items():
        cur.execute("""
            INSERT INTO colors (color, frequency) 
            VALUES (%s, %s)
            ON CONFLICT (color) 
            DO UPDATE SET frequency = colors.frequency + %s
        """, (color, frequency, frequency))

    # Committing the changes
    conn.commit()

    # Closing the cursor and connection
    cur.close()
    conn.close()

