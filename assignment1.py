"""
Albums Archive 1.0
YANG HAORAN
https://github.com/Yang-Haoran2005/cp1404-albums
A program to manage a collection of music albums, tracking which ones
are required listening and which have been completed.
Estimate: 4 hours
Actual:
"""

import random
from operator import itemgetter

FILENAME = "albums.csv"
TITLE_INDEX = 0
ARTIST_INDEX = 1
YEAR_INDEX = 2
STATUS_INDEX = 3
REQUIRED = "r"
COMPLETED = "c"


def main():
    """Albums Archive program with menu."""
    print("Albums Archive 1.0 - by YANG HAORAN")
    albums = load_albums(FILENAME)
    print(f"{len(albums)} albums loaded.")

    choice = ""
    while choice != "Q":
        print("\nMenu:")
        print("D - Display albums")
        print("R - Recommend an album")
        print("A - Add new album")
        print("M - Mark an album as completed")
        print("Q - Quit")
        choice = input(">>> ").upper()

        if choice == "D":
            display_albums(albums)
        elif choice == "R":
            recommend_album(albums)
        elif choice == "A":
            add_album(albums)
        elif choice == "M":
            mark_album_completed(albums)
        elif choice == "Q":
            save_albums(FILENAME, albums)
            print(f"{len(albums)} albums saved to {FILENAME}")
            print("Have a nice day :)")
        else:
            print("Invalid menu choice")


def load_albums(filename):
    """Load albums from CSV file into a list of lists."""
    albums = []
    try:
        in_file = open(filename, "r")
        for line in in_file:
            line = line.strip()
            if line:
                parts = line.split(",")
                title = parts[TITLE_INDEX]
                artist = parts[ARTIST_INDEX]
                year = int(parts[YEAR_INDEX])
                status = parts[STATUS_INDEX]
                albums.append([title, artist, year, status])
        in_file.close()
    except FileNotFoundError:
        print(f"{filename} not found. Starting with empty list.")
    return albums


def save_albums(filename, albums):
    """Save albums to CSV file."""
    out_file = open(filename, "w")
    for album in albums:
        print(f"{album[TITLE_INDEX]},{album[ARTIST_INDEX]},{album[YEAR_INDEX]},{album[STATUS_INDEX]}", file=out_file)
    out_file.close()


def display_albums(albums):
    """Display albums sorted by status then year, with alignment."""
    if len(albums) == 0:
        print("No albums to display.")
        return

    # Sort by status (required first) then by year
    sorted_albums = sorted(albums, key=itemgetter(STATUS_INDEX, YEAR_INDEX))

    # Calculate column widths for alignment
    max_title_length = max(len(album[TITLE_INDEX]) for album in sorted_albums)
    max_artist_length = max(len(album[ARTIST_INDEX]) for album in sorted_albums)

    required_count = 0
    for i, album in enumerate(sorted_albums):
        if album[STATUS_INDEX] == REQUIRED:
            marker = "*"
            required_count += 1
        else:
            marker = " "
        print(f"{marker} {i + 1}. {album[TITLE_INDEX]:{max_title_length}s} - "
              f"{album[ARTIST_INDEX]:{max_artist_length}s} ({album[YEAR_INDEX]})")

    if required_count > 0:
        print(f"{required_count} albums still required.")
    else:
        print("No required albums. Awesome!")


def recommend_album(albums):
    """Recommend a random required album."""
    required_albums = [album for album in albums if album[STATUS_INDEX] == REQUIRED]
    if len(required_albums) == 0:
        print("No required albums. Great, you have listened to all of them!")
    else:
        album = random.choice(required_albums)
        print(f"You should listen to {album[TITLE_INDEX]} by {album[ARTIST_INDEX]}")


def add_album(albums):
    """Add a new album to the list."""
    title = get_non_empty_string("Title: ")
    artist = get_non_empty_string("Artist: ")
    year = get_valid_year("Year: ")
    album = [title, artist, year, REQUIRED]
    albums.append(album)
    print(f"{title} by {artist} ({year}) added to album list")


def mark_album_completed(albums):
    """Mark an album as completed."""
    # Check if there are any required albums
    required_albums = [album for album in albums if album[STATUS_INDEX] == REQUIRED]
    if len(required_albums) == 0:
        print("No required albums.")
        return

    display_albums(albums)
    print("Enter the number of an album to mark as completed")

    # Get sorted list to match display order
    sorted_albums = sorted(albums, key=itemgetter(STATUS_INDEX, YEAR_INDEX))

    valid_input = False
    while not valid_input:
        try:
            choice = int(input(">>> "))
            if choice < 1:
                print("Number must be > 0")
            elif choice > len(sorted_albums):
                print("Invalid album number")
            else:
                valid_input = True
        except ValueError:
            print("Invalid input; enter a valid number")

    selected_album = sorted_albums[choice - 1]
    if selected_album[STATUS_INDEX] == COMPLETED:
        print(f"You have already completed {selected_album[TITLE_INDEX]}")
    else:
        selected_album[STATUS_INDEX] = COMPLETED
        print(f"{selected_album[TITLE_INDEX]} by {selected_album[ARTIST_INDEX]} marked as completed")


def get_non_empty_string(prompt):
    """Get a non-empty string from user."""
    string = input(prompt)
    while string.strip() == "":
        print("Input can not be blank")
        string = input(prompt)
    return string


def get_valid_year(prompt):
    """Get a valid year (positive integer) from user."""
    valid_input = False
    while not valid_input:
        try:
            year = int(input(prompt))
            if year <= 0:
                print("Number must be > 0")
            else:
                valid_input = True
        except ValueError:
            print("Invalid input; enter a valid number")
    return year


if __name__ == '__main__':
    main()
