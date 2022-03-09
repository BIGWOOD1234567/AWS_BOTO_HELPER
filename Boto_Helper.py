import sys
import boto3
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# menu input lists -----------------------------------------------------------------------------------------------------

display_buckets_mm = ["DISPLAY BUCKETS", "DSBKT"]
create_bucket_mm = ["CREATE BUCKET", "CRBKT"]
delete_bucket_mm = ["DELETE BUCKET", "DLBKT"]
display_items_mm = ["DISPLAY ITEMS", "DSITM"]
upload_item_mm = ["UPLOAD ITEM", "UPITM"]
delete_item_mm = ["DELETE ITEM", "DLITM"]
quit_mm = ["QUIT", "Q"]
yes_mm = ["YES", "Y"]
no_mm = ["NO", "N"]
done_mm = ["DONE", "D"]
all_mm = ["ALL", "A"]

# welcome/main menu/etc messages ---------------------------------------------------------------------------------------

welcome_msg = """
                <<<<^^^^^^^^^^^^^^^^^^^^^^^^^^>>>>                
< < < << <<< <<<<{{{ Welcome to the S3 Helper }}}>>>> >>> >> > > >
                <<<<==========================>>>>     


 *Make a selection from the menu by typing it and pressing enter* 

 """

main_menu_msg = """
|- - -- -----MAIN MENU----- -- - -|
 Display Buckets.....or.....DSBKT
 Create Bucket.......or.....CRBKT
 Delete Bucket.......or.....DLBKT
 Display Items.......or.....DSITM
 Upload Item.........or.....UPITM
 Delete Item.........or.....DLITM
 Quit................or.........Q

"""

to_continue_msg = "\n-press ENTER to continue or type QUIT to quit-"

bucket_name_msg = """

When naming your bucket, the rules are as follows:

~Bucket names must be between 3 (min) and 63 (max) characters long
~Bucket names can consist only of lowercase letters, numbers, dots (.), and hyphens (-)
~Bucket names must begin and end with a letter or number
~Bucket names must not be formatted as an IP address
~Bucket names must not start with the prefix xn--
~Bucket names must not end with the suffix -s3alias

type QUIT to quit or, enter the name of the bucket to be created and press enter:
"""

bucket_creation_msg = """"
Congratulations! Your name is perfect, creating a new bucket now!
Would you like to view your current buckets(YES or NO)?
"""

name_exists_msg = "\nPlease try again, you already have a bucket with the name:   "

delete_bucket_selection = """
~Please type the number of the bucket you would like to delete and press enter.
~Enter them one at a time, and press enter each time.
~When done type DONE and press enter to stop entering, before confirming your selections a final time:
"""

delete_bucket_completed_msg = """
~Bucket deletion Successful!
~Would you like to view your current buckets(YES or NO)?

"""

bucket_selection_msg = """
Please type the number of the bucket whose contents you would like to see and press enter:

"""

item_selection_msg = """
Please type the item name you would like to delete or ALL to delete all items and press enter:
"""

item_key_name_msg = """
Please type the key name for the item to be uploaded and press enter:

"""

upload_success_msg = """
~Item upload Successful!
~Would you like to display the items in one of your buckets(YES or NO)?
"""

bad_file_path_msg = """
Oops looks like that didn't work, press ENTER to try again or type QUIT to quit:
"""


# Funcs ----------------------------------------------------------------------------------------------------------------

def display_buckets_func():
    s3 = boto3.client('s3')
    response = s3.list_buckets()  # getting info on the buckets
    print("These are your current buckets:\n")  # Output the bucket names
    for bucket in response["Buckets"]:
        print(f'  {bucket["Name"]}')
    print(f'  ({len(response["Buckets"])} Total buckets)')
    quit_checker(input(to_continue_msg))


def create_bucket_func():
    s3 = boto3.client('s3')
    response = s3.list_buckets()  # getting info on the buckets
    bucket_name_input = input(bucket_name_msg)
    while True:
        names_checked = 0
        quit_checker(bucket_name_input)
        for bucket in response["Buckets"]:  # checking if user name is already a current bucket name
            if str(bucket["Name"]) == bucket_name_input:
                bucket_name_input = input(name_exists_msg + bucket_name_input + "\n")
                break
            names_checked += 1
        if names_checked == len(response["Buckets"]):
            break
    try:
        s3.create_bucket(Bucket=bucket_name_input)  # creating bucket with name string
        y_or_n = input(bucket_creation_msg).upper()
        while True:
            quit_checker(y_or_n)
            if y_or_n in yes_mm:  # returning yes or no about viewing current buckets
                return True
            elif y_or_n in no_mm:
                return False
            else:
                y_or_n = input("Invalid input, please try again.\n").upper()

    except:
        print("Something may have went wrong with your bucket creation... returning to the main menu.")
    return False


def delete_bucket_func():
    s3 = boto3.client('s3')
    response = s3.list_buckets()  # getting info on the buckets
    print("A bucket may only be deleted when empty.\nThese are your current buckets:\n")  # Output the bucket names
    bucket_name_list = {}
    bucket_number_list = []
    bucket_number = 0
    for bucket in response["Buckets"]:
        bucket_number += 1
        bucket_name_list[bucket_number] = bucket["Name"]
        print(f'  {bucket_number}. {bucket["Name"]}')
    print(f'  ({len(response["Buckets"])} Total buckets)' + delete_bucket_selection)
    while True:
        bkt_name_number = input()
        if bkt_name_number.upper() not in done_mm:
            bucket_number_list.append(int(bkt_name_number))
        elif bkt_name_number.upper() in done_mm:
            break
    print("\n~Are you sure you would like to delete the following buckets? :\n")
    for bucket_numbers in bucket_number_list:
        print("  " + str(bucket_name_list[bucket_numbers]))
    while True:
        y_or_n = input("\n").upper()
        quit_checker(y_or_n)
        if y_or_n in yes_mm:
            try:
                s3 = boto3.resource('s3')
                for bucket_numbers in bucket_number_list:
                    del_name = str(bucket_name_list[bucket_numbers])
                    print(del_name)
                    bucket = s3.Bucket(del_name)
                    bucket.delete()
                y_or_n = input(delete_bucket_completed_msg).upper()
                while True:
                    quit_checker(y_or_n)
                    if y_or_n in yes_mm:
                        return True
                    elif y_or_n in no_mm:
                        return False
                    else:
                        y_or_n = input("Invalid input, please try again.\n").upper()
            except:
                print("""Something may have went wrong with your bucket deletions... returning to the main menu.
                (one or more of your buckets may not be empty)""")
                return False

        elif y_or_n in no_mm:
            print("\nBucket deletion canceled, returning to main menu.")
            return
        else:
            print("Invalid input, please try again.\n")


def display_items_func():
    s3 = boto3.client('s3')
    response = s3.list_buckets()  # getting info on the buckets
    print("These are your current buckets:\n")  # Output the bucket names
    bucket_name_list = {}
    bucket_number = 0
    for bucket in response["Buckets"]:
        bucket_number += 1
        bucket_name_list[bucket_number] = bucket["Name"]
        print(f'  {bucket_number}. {bucket["Name"]}')
    print(f'  ({len(response["Buckets"])} Total buckets)')
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name_list[int(input(bucket_selection_msg))])
    print("\n")
    item_name_list = []
    for my_bucket_object in my_bucket.objects.all():
        item_name_list.append(my_bucket_object.key)
        print("  ~" + my_bucket_object.key)
    if not len(item_name_list):
        print("There are no items in this bucket... returning to the main menu.\n")
    return


def upload_item_func():
    s3 = boto3.client('s3')
    response = s3.list_buckets()  # getting info on the buckets
    print("These are your current buckets:\n")  # Output the bucket names
    bucket_name_list = {}
    bucket_number = 0
    for bucket in response["Buckets"]:
        bucket_number += 1
        bucket_name_list[bucket_number] = bucket["Name"]
        print(f'  {bucket_number}. {bucket["Name"]}')
    print(f'  ({len(response["Buckets"])} Total buckets)')
    s3 = boto3.resource("s3")
    bucket_name = bucket_name_list[int(input(bucket_selection_msg))]
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    print("PLease select a file on your system for upload, look for the \"Open File\" dialog box, then return here.\n")
    file_name_path = askopenfilename()
    while True:
        if not file_name_path:
            quit_checker(input(bad_file_path_msg).upper())
            file_name_path = askopenfilename()
        elif file_name_path:
            print(file_name_path, "\nThanks looks good!\n")
            break
    data = open(file_name_path, "rb")  # opening data, show Open dialog box, return the path to the file, binary
    try:
        s3.Bucket(bucket_name).put_object(Key=input(item_key_name_msg), Body=data)  # adding the data/key to new bucket
    except:
        data.close()  # closing the data
        print("Something may have went wrong with your item upload... returning to the main menu.")
        return False
    data.close()  # closing the data
    y_or_n = input(upload_success_msg)
    while True:
        quit_checker(y_or_n)
        if y_or_n in yes_mm:
            return True
        elif y_or_n in no_mm:
            return False
        else:
            y_or_n = input("Invalid input, please try again.\n")


def delete_item_func():
    s3 = boto3.client('s3')
    response = s3.list_buckets()  # getting info on the buckets
    print("These are your current buckets:\n")  # Output the bucket names
    bucket_name_list = {}
    bucket_number = 0
    for bucket in response["Buckets"]:
        bucket_number += 1
        bucket_name_list[bucket_number] = bucket["Name"]
        print(f'  {bucket_number}. {bucket["Name"]}')
    print(f'  ({len(response["Buckets"])} Total buckets)')
    s3 = boto3.resource('s3')
    bucket_name = bucket_name_list[int(input(bucket_selection_msg))]
    my_bucket = s3.Bucket(bucket_name)
    print("\n")
    item_name_list = []
    for my_bucket_object in my_bucket.objects.all():
        print("   ~  " + my_bucket_object.key)
        item_name_list.append(my_bucket_object.key)
    if not len(item_name_list):
        y_or_n = input("There are no items in this bucket... would you like to check another bucket?\n").upper()
        while True:
            quit_checker(y_or_n)
            if y_or_n in no_mm:
                return False
            elif y_or_n in yes_mm:
                return delete_item_func()
            else:
                y_or_n = input("Invalid input, please try again.\n").upper()
    item_selection = input(item_selection_msg)
    while True:
        quit_checker(item_selection.upper())
        if item_selection.upper() in all_mm:
            try:
                for item_name in item_name_list:
                    print(bucket_name)
                    s3.Object(bucket_name, item_name).delete()
                y_or_n = input("Your items were all deleted! Would you like to delete a bucket?\n").upper()
                while True:
                    quit_checker(y_or_n)
                    if y_or_n in no_mm:
                        return False
                    elif y_or_n in yes_mm:
                        return True
                    else:
                        y_or_n = input("Invalid input, please try again.\n").upper()
            except:
                print("Something may have went wrong with your item deletions... returning to the main menu.")
                return False
        elif item_selection in bucket_name_list.values():
            try:
                print(bucket_name)
                s3.Object(bucket_name, item_selection).delete()
                y_or_n = input("Your item was deleted! ... would you like to delete another item?\n").upper()
                while True:
                    quit_checker(y_or_n)
                    if y_or_n in no_mm:
                        return False
                    elif y_or_n in yes_mm:
                        break
                    else:
                        y_or_n = input("Invalid input, please try again.\n").upper()
            except:
                print("Something may have went wrong with your item deletion... returning to the main menu.")
                return False
            else:
                item_selection = input(item_selection_msg)
                continue
        else:
            item_selection = input("Invalid input, please try again.\n")


def quit_checker(user_input_to_check):
    if user_input_to_check in quit_mm:
        sys.exit("Thanks! quitting.. now")
    return


# start menu -----------------------------------------------------------------------------------------------------------

def main_menu():
    while True:
        mm_input = input(main_menu_msg).upper()
        if mm_input in display_buckets_mm:
            display_buckets_func()
            continue
        elif mm_input in create_bucket_mm:
            if create_bucket_func():
                display_buckets_func()
            continue
        elif mm_input in delete_bucket_mm:
            if delete_bucket_func():
                display_buckets_func()
            continue
        elif mm_input in display_items_mm:
            display_items_func()
            continue
        elif mm_input in upload_item_mm:
            if upload_item_func():
                display_items_func()
            continue
        elif mm_input in delete_item_mm:
            if delete_item_func():
                if delete_bucket_func():
                    display_buckets_func()
            continue
        elif mm_input in quit_mm:
            quit()
        else:
            print("Invalid input, please try again.\n")


# begin ----------------------------------------------------------------------------------------------------------------

print(welcome_msg)

main_menu()
