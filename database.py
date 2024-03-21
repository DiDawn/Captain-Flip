import csv
import hashlib


# creating a class for the different accounts
class Database:

    def __init__(self, file):
        self.file = file
        self.victories = 0
        self.draws = 0
        self.defeats = 0

    # creating a function to encrypt the different passwords
    @staticmethod
    def encryption(password):
        return hashlib.sha256(password.encode()).hexdigest()

    # function to sign up
    def sign_up(self, identifier, password):
        with open(self.file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            password_hash = self.encryption(password)
            writer.writerow([identifier, password_hash, 0, 0, 0])

    # function to sign in and recover the statistics of the player
    def sign_in(self, identifier, password):
        with open(self.file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            password_hash = self.encryption(password)
            for row in reader:
                if row[0] == identifier and row[1] == password_hash:
                    self.victories = row[2]
                    self.draws = row[3]
                    self.defeats = row[4]
                    return True
        return False

    # function to return the stats of the player
    def return_stats(self):
        return self.victories, self.draws, self.defeats

    # function to add a win to the stats of a player and update it in the csv file
    def add_victory(self, identifier):
        self.victories += 1

        # Open the CSV file for reading and writing
        with open(self.file, 'r+', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)  # Convert the rows to a list to modify them

            # Iterate through the rowss
            for i, row in enumerate(rows):
                # Check if the identifier matches
                if row[0] == identifier:
                    # Increment the number of victories for the player
                    row[2] = str(int(row[2]) + 1)
                    # Update the class statistics
                    self.victories += 1
                    # Move the cursor to the beginning of the file
                    csvfile.seek(0)
                    # Create a CSV writer object
                    writer = csv.writer(csvfile)
                    # Write all the rows back to the file
                    writer.writerows(rows)
                    # Truncate the file to the current length
                    csvfile.truncate()
                    return

    # function to add a draw to the stats of a player and update it in the csv file
    def add_draw(self, identifier):
        self.draws += 1

        # Open the CSV file for reading and writing
        with open(self.file, 'r+', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)  # Convert the rows to a list to modify them

            # Iterate through the rows
            for i, row in enumerate(rows):
                if row[0] == identifier:
                    # Increment the number of draws for the player
                    row[3] = str(int(row[3]) + 1)
                    # Update the class statistics
                    self.draws += 1
                    # Move the cursor to the beginning of the file
                    csvfile.seek(0)
                    # Create a CSV writer object
                    writer = csv.writer(csvfile)
                    # Write all the rows back to the file
                    writer.writerows(rows)
                    # Truncate the file to the current length
                    csvfile.truncate()
                    return

    # function to add a defeat to the stats of a player and update it in the csv file
    def add_defeat(self, identifier):
        self.defeats += 1
        # Open the CSV file for reading and writing
        with open(self.file, 'r+', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)  # Convert the rows to a list to modify them

            # Iterate through the rows
            for i, row in enumerate(rows):
                if row[0] == identifier:
                    # Increment the number of draws for the player
                    row[4] = str(int(row[4]) + 1)
                    # Update the class statistics
                    self.draws += 1
                    # Move the cursor to the beginning of the file
                    csvfile.seek(0)
                    # Create a CSV writer object
                    writer = csv.writer(csvfile)
                    # Write all the rows back to the file
                    writer.writerows(rows)
                    # Truncate the file to the current length
                    csvfile.truncate()
                    return
