#Exercise 3
#Reading and managing a books database

from datetime import datetime
import time

def tuple_creation(filename, delimiter):
    """The function creates a list of tuples from a file
    and takes filename and delimiter for each value in the line."""

    records = []
    try:
        with open(filename, "r") as file:
            for record in file:
                record = record.strip()
                record = record.split(delimiter)

                for index,value in enumerate(record):
                    try:
                        record[index] = int(value)
                    except:
                        pass

                records.append(tuple(record))

    except FileNotFoundError:
        print("\nSorry! The file you entered doesn't exist")
        print("Try referencing a different file or check the path of the file you entered.\n")
    
    except Exception as error:
        print("\nOops!")
        print(error)

    else:  
        print("\nWelcome to the books database!")          
        return records


def main_menu():
    #Prints the main menu of the program

    print()
    print("What would you like to do?")
    acceptable_options = ["a", "b", "c", "d", "e", "f", "g"]
    input_txt = """Enter the letter:
    a) Display full details of all books
    b) Adding a book to records
    c) Searching a book by ISBN
    d) Sorting books based on publication year
    e) Updating book details
    f) Delete a book
    g) Quit
    >>>"""

    while True:
        print()
        option = input(input_txt)
        option = option.lower().strip()
        if option in acceptable_options:
            break
        elif option == "":
            print("Enter a value!\n")
            continue
        print("Please enter a letter between 'a' and 'g'!\n")

    return option

def check_input(input_message, data_type, condition, error_message):
    """
    Checks input from a user based on a condition until
    the input is within the constraints of the values of 
    the book database
    """
    while True:
        print()
        variable = input(input_message).strip()
        if variable == "":
            print("Please enter a value!!")
            continue

        try:
            variable = int(variable)
            if data_type == "str":
                print("Please enter a valid name without numbers!")
                continue

        except:
            if data_type == "int":
                print("Please enter a digit value!!")
                continue
            
            elif not variable.isalpha() and data_type == "str":
                print("Cannot contain special characters and numbers!")
                continue
           
        if " and " in condition:
            #If there are 2 conditions with 'and' operator, checks the conditions separately
            #and prints customized error messages if either of them return False
            and_condition = condition.split(" and ")
            if eval(and_condition[0]): #eval converts string to source code
                if eval(and_condition[1]):
                    break
                else:
                    print(error_message[1])
            else:
                print(error_message[0])
        else:
            if eval(condition):
                break

            print(error_message)


    print()
    return variable



def display_record(records):
    """Displays the records of the table that have been read from the file
    or display a specific record from the records"""

    print()

    #Headers dictionary contains a list of 2 values:
    #Index of the value of the title in records and 
    #spacing needed between the table, respectively
    headers = {"Author-Lastname":[2, 17], "Book-title":[1, 51], "ISBN":[3, 8], "Publication-Date":[4,20], "access":[0, 7]}

    for header,details in headers.items():
        format_text = "{:^%d}"%(details[1]) #Spacing value
        print(format_text.format(header), end = "")
    print()

    for header,details in headers.items():
        print("*"*(details[1] - 1), end="") 
        print("x", end="")
    print()

    for record in records:
        for index,spacing in headers.values():
            format_text = "{:^%d}"%(spacing)
            print(format_text.format(record[index]), end="")
        print()
    
    print()


filename = input("Please enter the filename from which data is to be collected\n>>>")
records = tuple_creation(filename, ", ")

if records:
    while True:  
        operation = main_menu()

        #Display all records of the table
        if operation == "a":
            display_record(records)

        
        #Add a record to database
        elif operation == "b":
            
            author_lastname = check_input(input_message = "Enter the author last name (Upto 10 characters):", data_type = "str",
                                condition = "len(variable) <= 10", error_message = "Enter upto 10 characters for author's lastname!")

            book_title = check_input(input_message = "Enter the book title (Upto 50 characters):", data_type = "alphanumeric",
                                condition = "len(variable) <= 50", error_message = "Enter upto 50 characters for book title!") 

            
            ISBN = check_input(input_message = "Enter the ISBN of the book (5 digits):", data_type = "int",
                                #The second condition ensures that an already existing ISBN is not added into the records
                                condition = "len(str(variable)) == 5 and variable not in [record[3] for record in records]", 
                                error_message = ["Please enter a 5 digit ISBN", "ISBN already exists in records\nPlease enter a new one!"])
                
                
            pub_date = check_input(input_message = "Enter the publication date:", data_type = "int",
                                   #The second condition checks to see that a date beyond the current year is not mentioned
                                    condition = "len(str(variable)) == 4 and variable <= datetime.now().year", 
                                    error_message = ["Please enter a valid year of publication!", "Enter a year upto the current year!"])

            access = check_input(input_message = "Enter the access code(0 or 1)\n0: Non - updatable\n1: Updatable\n>>>", data_type = "int",
                                condition = "variable in [0,1]", error_message = "Enter a valid access code!")

            record_to_add = (access, book_title, author_lastname.capitalize(), ISBN, pub_date)
            records.append(record_to_add)

            print("Record has been successfully added!")
            display_record([record_to_add])
            

        #Search for a book by ISBN
        elif operation == "c":
            user_isbn = check_input(input_message = "Enter the ISBN for the book (5 digits):", data_type = "int",
                                    #The second condition ensures that the entered ISBN exists in the records
                                    condition = "len(str(variable)) == 5 and variable in [record[3] for record in records]",
                                    error_message = ["Please enter a 5 digit ISBN", "ISBN doesn't exist\nPlease try again!"])
            
            for record in records:
                #record[3] is the index of the ISBN value in records
                if user_isbn == record[3]:
                    display_record([record])
                    break

        #Sorting records based on publication year
        elif operation == "d":
            upper_year = check_input(input_message = "Enter the upper bound for the year:", data_type = "int",
                                    #The second condition checks to see that a date beyond the current year is not mentioned
                                    condition = "len(str(variable)) == 4 and variable <= datetime.now().year", 
                                    error_message = ["Please enter a valid year!!", "Enter a year upto the current year!"])

            lower_year = check_input(input_message = "Enter the lower bound for the year:", data_type = "int",
                                    condition = "len(str(variable)) == 4 and variable <= upper_year", 
                                    error_message = ["Please enter a valid year!!", "Please enter a year lesser than the upper bound!"])
            
            records_in_range = []
            for record in records:
                #record[-1] is the last record, which holds the value of the publication date
                if lower_year <= record[-1] <= upper_year:
                    records_in_range.append(record)

            if len(records_in_range) > 0:
                #The lambda(anonymous function) yields the publication date from the records
                #The key takes that value as the base for sorting the records, that is, publication date
                get_pub_date = lambda record: record[-1]
                records_in_range.sort(key = get_pub_date, reverse = True)
            
                display_record(records_in_range)

            else:
                print("No records are part of this range.")
                
        #Updating a record of the database
        elif operation == "e":
            ans = "y"
            while ans == "y":
                user_isbn = check_input(input_message = "Enter the ISBN of the book you would like to update (5 digits):", data_type = "int",
                                        #The second condition checks to see if the ISBN is present in the database or not
                                        condition = "len(str(variable)) == 5 and variable in [record[3] for record in records]", 
                                        error_message = ["Please enter a 5 digit ISBN!", "ISBN doesn't exist in database\nPlease try again"])

                updatable = False
                for record in records:
                    #record[3] holds the ISBN value in records
                    if user_isbn == record[3]:
                        if record[0] == 1: #record[0] holds the access code.
                            record_to_update = record
                            updatable = True

                if updatable:
                    print("\nOriginal Record:")
                    display_record([record_to_update])
                    
                    author_lastname = check_input(input_message = "Enter the author last name (Upto 10 characters):", data_type = "str",
                                    condition = "len(variable) <= 10", error_message = "Enter upto 10 characters for author's lastname!")

                    book_title = check_input(input_message = "Enter the book title (Upto 50 characters):", data_type = "alphanumeric",
                                    condition = "len(variable) <= 50", error_message = "Enter upto 50 characters for book title!")

                    pub_date = check_input(input_message = "Enter the publication date:", data_type = "int",
                                        #The second condition checks to see that a date beyond the current year is not mentioned
                                        condition = "len(str(variable)) == 4 and variable <= datetime.now().year", 
                                        error_message = ["Please enter a valid year of publication!", "Enter a year upto the current year!"])

                    updated_records = (1,book_title, author_lastname.capitalize(), user_isbn, pub_date)
                    index = records.index(record_to_update)
                    records[index] = updated_records
                    
                    print("Record was successfully updated!!")
                    display_record([updated_records])
                    ans = "n"
                    
                else:
                    print("The record with ISBN {} cannot be updated".format(user_isbn))
                    print()
                    ans = check_input(input_message = "Would you like to update another record?(y/n)\n>>>", data_type = "str",
                                      condition = "variable.lower() in ['y','n']", error_message = "Please enter a valid answer!").lower()
        
        elif operation == "f":
            user_isbn = check_input(input_message = "Enter the ISBN of the book you would like to update (5 digits):", data_type = "int",
                                        #The second condition checks to see if the ISBN is present in the database or not
                                        condition = "len(str(variable)) == 5 and variable in [record[3] for record in records]", 
                                        error_message = ["Please enter a 5 digit ISBN!", "ISBN doesn't exist in database\nPlease try again"])
            for record in records:
                #record[3] stores the ISBN
                if record[3] == user_isbn:
                    record_to_delete = record
                    break

            records.remove(record_to_delete)

            print("Record was successfully deleted!")
            display_record([record_to_delete])

        #Quit the books database
        else:
            print()
            confirm = check_input(input_message = "Are you sure you want to exit(y/n)\n>>>", data_type = "str",
                                condition = "variable.lower() in ['y','n']", error_message = "Please enter a valid answer!").lower()
            if confirm == "y":
                break

            print()

        time.sleep(1)

with open(filename, "w") as file:
    for record in records:
        record = map(str, record)
        file.write(", ".join(record))
        file.write("\n")

print("Thank you for using the books database!")   
#END   
