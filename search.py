import requests
import re
from bs4 import BeautifulSoup
import csv

# Extract names from CSV
def collect_data(file):

    f = open(file, "r")
    names = [] # Empty list to contain all names

    # Loop through each line of file
    for line in f:

        details = line.split(",") # Split line by comma

        if details[0] != "Name": # Make sure it's not the category line

            # Strip of excess punctuation & format correctly for search
            last_name = details[0].strip('"')
            first_name = details[1].strip('"')
            name = first_name + " " + last_name

            # Add name to list
            names.append(name)

    f.close()
    return names

# Execute Google search
def search(query_list):

    all_links = ["Result"] # List to contain links, starting with a results line

    # Loop through name list
    for name in query_list:

        # Format for search by splitting and adding plus signs
        n = name.split(" ")
        query = ""
        for i in range(len(n)):
            query += n[i]
            if i != (len(n)-1) and i != 0:
                query += "+"
        query += "+professor+Missouri"
        print(query)

        # Using requests, load the page
        page = requests.get("https://www.google.com/search?q=" + query)

        # Using bs4 & lxml, read the page
        soup = BeautifulSoup(page.content, "lxml")

        prof_link = [] # Empty list to contain links for each name

        # Loop through each link found on the first page of Google search
        for link in soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
            a = link.get('href')

            # Clean up link
            a = a.strip("/url?q=")
            a = a.split("&")
            wanted_link = a[0]

            # If the link has a .edu and is a cache, add the link to the page
            if ".edu" in wanted_link and "webcache" not in wanted_link:
                prof_link.append(wanted_link)
            # Otherwise, continue
            else:
                pass
        # If the Google search for this name yielded no links with a .edu ending, no results were found
        if len(prof_link) == 0:
                prof_link.append("No results found")

        # Add the first link of each prof to the all links list, for debugging later (if no link, "No results found"
        # added)
        all_links.append(prof_link[0])

    return all_links

# Write the text file
def write_file(L, filename):
    f = open(filename, "w")

    # Loop through list and create a new line for each item in the list
    for i in range(len(L)):
        f.write(str(L[i]) + "\n")

    f.close()




# Main function that collects data, executes the search, and connects the two spreadsheets
def main(file, second_file):

    names = collect_data(file) # Collect data from CSV
    link_list = search(names) # Execute Google search
    write_file(link_list, second_file) # Write text file of links

    # Convert .txt file to .csv
    with open(second_file, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open('results.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)


