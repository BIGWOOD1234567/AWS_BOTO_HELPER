import sys
import time
import boto3
import oschmod
from tkinter import Tk
from os.path import expanduser
from tkinter.filedialog import askopenfilename

home = expanduser("~")

# menu input lists -----------------------------------------------------------------------------------------------------

display_buckets_mm = ["DISPLAY BUCKETS", "DSBKT"]
create_bucket_mm = ["CREATE BUCKET", "CRBKT"]
delete_bucket_mm = ["DELETE BUCKET", "DLBKT"]
display_items_mm = ["DISPLAY ITEMS", "DSITM"]
upload_item_mm = ["UPLOAD ITEM", "UPITM"]

create_aws_Key_mm = ["CREATE AWS KEY", "CAWSK"]
show_aws_Keys_mm = ["SHOW AWS KEYS", "SAWKY"]

create_ec2_instance_mm = ["CREATE EC2 INSTANCE", "CEC2I"]
stop_ec2_instance_mm = ["STOP EC2 INSTANCE", "SEC2I"]
terminate_ec2_instance_mm = ["TERMINATE EC2 INSTANCE", "TEC2I"]

delete_item_mm = ["DELETE ITEM", "DLITM"]
quit_mm = ["QUIT", "Q"]
yes_mm = ["YES", "Y"]
no_mm = ["NO", "N"]
done_mm = ["DONE", "D"]
all_mm = ["ALL", "A"]

# welcome/main menu/etc messages ---------------------------------------------------------------------------------------

welcome_msg = """
|<  < < << <<< <<<< <<<<< <<<<<<{{ {  Welcome to the AWS  } }}>>>>>> >>>>> >>>> >>> >> > >  >|
|   ██████╗  ██████╗ ████████╗ ██████╗     ██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗   |   
|   ██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗    ██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗  |   
|   ██████╔╝██║   ██║   ██║   ██║   ██║3   ███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝  |   
|   ██╔══██╗██║   ██║   ██║   ██║   ██║    ██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗  |   
|   ██████╔╝╚██████╔╝   ██║   ╚██████╔╝    ██║  ██║███████╗███████╗██║     ███████╗██║  ██║  |   
|   ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝  |
|<<<================{==={{=={{{={{={ by Zachary Smallwood }=}}=}}}==}}===}================>>>|
             *Make a selection from the menu by typing it and pressing enter* 
 """

main_menu_msg = """
|<<<================{==={{=={{{={{={       MAIN MENU      }=}}=}}}==}}===}================>>>|
                                   /-------S3 BUCKET------\\                                                          
 Display Buckets..................................................or the shortcut->.....DSBKT
 Create Bucket....................................................or the shortcut->.....CRBKT
 Delete Buckets...................................................or the shortcut->.....DLBKT
 Display Items....................................................or the shortcut->.....DSITM
 Upload Item......................................................or the shortcut->.....UPITM
 Delete Item......................................................or the shortcut->.....DLITM
                                                                         
                                   /--------AWS KEY-------\\                                       
 Show AWS Keys....................................................or the shortcut->.....SAWKY              
 Create AWS Key...................................................or the shortcut->.....CAWSK

                                                                      
                                   /------EC2 INSTANCE----\\                    
 Create EC2 Instance..............................................or the shortcut->.....CEC2I
 Stop EC2 Instance................................................or the shortcut->.....SEC2I
 Terminate EC2 Instance...........................................or the shortcut->.....TEC2I

 Quit.............................................................or the shortcut->.........Q
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
  ({number} Total buckets)

~Please type the number of the bucket you would like to delete and press enter.
~Enter them one at a time, and press enter each time.
~When done type DONE and press enter to stop entering, before confirming your selections a final time:
"""

delete_bucket_completed_msg = """
~Bucket deletion Successful!
~Would you like to view your current buckets(YES or NO)?

"""

bucket_view_msg = """
Please type the number of the bucket whose contents you would like to see and press enter:

"""

bucket_select_msg = """
Please type the number of the bucket to upload to and press enter:

"""

item_selection_msg = """
Please type the item name you would like to delete or ALL to delete all items and press enter:
"""

item_key_name_msg = """
Please type the key name for the item to be uploaded and press enter:

"""

invalid_input_msg = "Invalid input, please try again.\n"

upload_success_msg = """
~Item upload Successful!
~Would you like to display the items in one of your buckets(YES or NO)?S
"""

bad_file_path_msg = """
Oops looks like that didn't work, press ENTER to try again or type QUIT to quit:
"""

bad_item_del_msg = """Something may have went wrong with your bucket deletions... returning to the main menu."""

empty_bucket_warning = """                    (one or more of your buckets may not be empty)"""

delete_all_conf_msg = """
If you would like to delete all the items in this bucket type YES ALL and press enter, 
or type NO to return to the main menu:
"""

full_buckets_msg = """looks like {number} of your bucket selections have items in them and cannot be deleted as is.
"""

num_itm_remv_msg = """Successfully removed {itm_amount} items from Bucket {bkt_name}!
"""

bkt_contains_msg = """Bucket {bkt_name} contains {itm_amount} items/folders"""

quit_msg = "Thanks! quitting.. now"


# Funcs ----------------------------------------------------------------------------------------------------------------

def print_slow(slow_string):    # func to print to the command line slowly
    for letter in slow_string:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(1)


def display_buckets_func():    # func to show current buckets
    s3 = boto3.client('s3')
    response = s3.list_buckets()  # getting info on the buckets
    print("These are your current buckets:\n")
    for bucket in response["Buckets"]:
        print(f'  {bucket["Name"]}')
    print(f'  ({len(response["Buckets"])} Total buckets)')
    quit_checker(input(to_continue_msg))


def create_bucket_func():    # func to generate a new S3 bucket
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    bucket_name_input = input(bucket_name_msg)
    while True:
        names_checked = 0
        quit_checker(bucket_name_input)
        for bucket in response["Buckets"]:  # checking if username is already a current bucket name
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
                y_or_n = input(invalid_input_msg).upper()
    except:
        print("Something may have went wrong with your bucket creation... returning to the main menu.")
    return False


def delete_bucket_func():    # func to delete a selection of buckets and all items in those buckets if user wants
    s3 = boto3.client('s3')
    response = s3.list_buckets()  # getting info on the buckets
    print("A bucket may only be deleted when empty.\nThese are your current buckets:\n")  # tips about deletion
    bucket_name_dict = {}
    bucket_number_list = []
    bucket_number = 0
    no_itm_bucket_list = []
    for bucket in response["Buckets"]:
        bucket_number += 1
        bucket_name_dict[bucket_number] = bucket["Name"]
        print(f'  {bucket_number}. {bucket["Name"]}')    # printing the buckets each numbered
    print(delete_bucket_selection.format(number=len(response["Buckets"])))    # asking which buckets to delete
    while True:    # looping until user finishes entering bucket selections
        bkt_name_number = input()
        if bkt_name_number.upper() not in done_mm:
            bucket_number_list.append(int(bkt_name_number))
        elif bkt_name_number.upper() in done_mm:
            break
    print("\n~Are you sure you would like to delete the following buckets? :\n")    # confirmation of selection
    for bucket_numbers in bucket_number_list:
        print("  " + str(bucket_name_dict[bucket_numbers]))
    while True:
        y_or_n = input("\n").upper()
        quit_checker(y_or_n)
        if y_or_n in yes_mm:
            try:
                empty_bucket_count = 0    # checking if all buckets from selection are empty
                buckets_w_items_dict = {}
                s3 = boto3.resource('s3')
                for bucket_numbers in bucket_number_list:
                    my_bucket = s3.Bucket(bucket_name_dict[bucket_numbers])
                    item_name_list = []
                    for my_bucket_object in my_bucket.objects.all():
                        item_name_list.append(my_bucket_object.key)
                    if not len(item_name_list):
                        empty_bucket_count += 1
                        no_itm_bucket_list.append(bucket_name_dict[bucket_numbers])    # making list of empty bucket
                        continue
                    buckets_w_items_dict[bucket_name_dict[bucket_numbers]] = item_name_list
                if buckets_w_items_dict:    # if any buckets from selection contained items
                    buk_num = len(buckets_w_items_dict)
                    print(full_buckets_msg.format(number=buk_num))    # informing user buckets contained items
                    for non_empty_bucket in buckets_w_items_dict:    # stepping through item deletions for each bucket
                        itm_amount = len(buckets_w_items_dict[non_empty_bucket])
                        print(bkt_contains_msg.format(bkt_name=non_empty_bucket, itm_amount=itm_amount))
                        for item in buckets_w_items_dict[non_empty_bucket]:    # printing bucket and its items
                            print("  ~ ", item)
                        y_or_n = input(delete_all_conf_msg).upper()    # warning to confirm delete all items for bucket
                        while True:
                            quit_checker(y_or_n)
                            if y_or_n in "YES ALL":
                                for item in buckets_w_items_dict[non_empty_bucket]:    # attempting to delete each item
                                    try:
                                        s3.Object(non_empty_bucket, item).delete()
                                    except:
                                        print(bad_item_del_msg)    # in case of failure inform user and return to menu
                                        return False
                                no_itm_bucket_list.append(non_empty_bucket)
                                itm_amount = len(buckets_w_items_dict[non_empty_bucket])
                                print(num_itm_remv_msg.format(itm_amount=itm_amount, bkt_name=non_empty_bucket))
                                break
                            elif y_or_n in no_mm:    # if user declines delete all message return to menu
                                return False
                            else:
                                y_or_n = input(invalid_input_msg).upper()    # if input is bad retry
                if no_itm_bucket_list:    # if any buckets from selection were item-less and ready for deletion
                    try:
                        s3 = boto3.resource('s3')
                        for bucket_name in no_itm_bucket_list:    # delete them one at a time
                            bucket = s3.Bucket(bucket_name)
                            bucket.delete()
                    except:
                        print(bad_item_del_msg)
                        return False
            except:
                print(bad_item_del_msg)
                return False
            y_or_n = input(delete_bucket_completed_msg).upper()    # if deletions are all good ask about viewing buckets
            while True:
                quit_checker(y_or_n)
                if y_or_n in yes_mm:
                    return True
                elif y_or_n in no_mm:
                    return False
                else:
                    y_or_n = input(invalid_input_msg).upper()
        elif y_or_n in no_mm:    # if no return to the menu
            print("\nBucket deletion canceled, returning to main menu.")
            return False
        else:    # if input was unrecognized restart the input loop
            print(invalid_input_msg)


def display_items_func():    # func to show all bucket items
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    print("These are your current buckets:\n")
    bucket_name_list = {}
    bucket_number = 0
    for bucket in response["Buckets"]:    # show each bucket in a numbered list
        bucket_number += 1
        bucket_name_list[bucket_number] = bucket["Name"]
        print(f'  {bucket_number}. {bucket["Name"]}')
    print(f'  ({len(response["Buckets"])} Total buckets)')    # shows total number of buckets
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name_list[int(input(bucket_view_msg))])    # gets bucket to check from number selection
    print("\n")
    item_name_list = []
    for my_bucket_object in my_bucket.objects.all():    # prints each item key name in the selected bucket
        item_name_list.append(my_bucket_object.key)
        print("  ~" + my_bucket_object.key)
    if not len(item_name_list):    # if no items in the bucket, inform user and return to menu
        print("There are no items in this bucket... returning to the main menu.\n")
    return


def upload_item_func():    # func to add items to S3 buckets
    s3 = boto3.client('s3')
    response = s3.list_buckets()  # getting info on the buckets
    print("These are your current buckets:\n")  # output the bucket names
    bucket_name_list = {}
    bucket_number = 0
    for bucket in response["Buckets"]:
        bucket_number += 1
        bucket_name_list[bucket_number] = bucket["Name"]
        print(f'  {bucket_number}. {bucket["Name"]}')
    print(f'  ({len(response["Buckets"])} Total buckets)')
    s3 = boto3.resource("s3")
    bucket_name = bucket_name_list[int(input(bucket_select_msg))]
    root = Tk()    # using tkinter to help user find filepath to file they want to upload
    root.withdraw()  # I didn't full tkinter GUI, so keep the root window from appearing
    root.wm_attributes('-topmost', 1)    # printing the file selection prompt on top of other windows
    print("PLease select a file on your system for upload, look for the \"Open File\" dialog box, then return here.\n")
    file_name_path = askopenfilename()    # getting the file path and assigning it to a variable
    while True:    # looping to make sure a filepath is selected
        if not file_name_path:
            quit_checker(input(bad_file_path_msg).upper())
            file_name_path = askopenfilename()
        elif file_name_path:
            print(file_name_path, "\nThanks looks good!\n")
            break
    root.destroy()    # get rid of the tkinter completely
    data = open(file_name_path, "rb")  # opening data
    try:
        s3.Bucket(bucket_name).put_object(Key=input(item_key_name_msg), Body=data)  # adding the data/key to the bucket
    except:
        data.close()  # closing the data
        print("Something may have went wrong with your item upload... returning to the main menu.")
        return False
    data.close()  # making sure the data is closed
    y_or_n = input(upload_success_msg).upper()    # inform user of good upload and ask about viewing items in a bucket
    while True:
        quit_checker(y_or_n)
        if y_or_n in yes_mm:
            return True
        elif y_or_n in no_mm:
            return False
        else:
            y_or_n = input(invalid_input_msg).upper


def delete_item_func():    # func to delete items from a bucket
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    print("These are your current buckets:\n")
    bucket_name_list = {}
    bucket_number = 0
    for bucket in response["Buckets"]:
        bucket_number += 1
        bucket_name_list[bucket_number] = bucket["Name"]
        print(f'  {bucket_number}. {bucket["Name"]}')
    print(f'  ({len(response["Buckets"])} Total buckets)')
    s3 = boto3.resource('s3')
    bucket_name = bucket_name_list[int(input(bucket_view_msg))]    # getting the bucket the user selects
    my_bucket = s3.Bucket(bucket_name)
    print("\n")
    item_name_list = []
    for my_bucket_object in my_bucket.objects.all():    # show all item key names in the bucket
        print("   ~  " + my_bucket_object.key)
        item_name_list.append(my_bucket_object.key)
    if not len(item_name_list):
        y_or_n = input("There are no items in this bucket... would you like to check another bucket?\n").upper()
        while True:    # inform user and ask about checking another bucket
            quit_checker(y_or_n)
            if y_or_n in no_mm:
                return False
            elif y_or_n in yes_mm:
                return delete_item_func()
            else:
                y_or_n = input(invalid_input_msg).upper()
    item_selection = input(item_selection_msg)    # ask which item to delete
    while True:
        quit_checker(item_selection.upper())    # make sure the user isn't trying to quit
        if item_selection.upper() in all_mm:    # users enter all to delete all items
            try:
                for item_name in item_name_list:
                    print(bucket_name)
                    s3.Object(bucket_name, item_name).delete()    # delete all the items
                y_or_n = input("Your items were all deleted! Would you like to delete a bucket?\n").upper()
                while True:    # inform user and ask about deleting a bucket
                    quit_checker(y_or_n)
                    if y_or_n in no_mm:
                        return False
                    elif y_or_n in yes_mm:
                        return True
                    else:
                        y_or_n = input(invalid_input_msg).upper()
            except:
                print("Something may have went wrong with your item deletions... returning to the main menu.")
                return False    # problem inform the user and return to menu
        elif item_selection in bucket_name_list.values():    # if one item is selected by the user
            try:
                print(bucket_name)
                s3.Object(bucket_name, item_selection).delete()    # delete the item
                y_or_n = input("Your item was deleted! ... would you like to delete another item?\n").upper()
                while True:
                    quit_checker(y_or_n)
                    if y_or_n in no_mm:
                        return False
                    elif y_or_n in yes_mm:
                        break
                    else:
                        y_or_n = input(invalid_input_msg).upper()
            except:
                print("Something may have went wrong with your item deletion... returning to the main menu.")
                return False
            else:
                item_selection = input(item_selection_msg)
                continue
        else:
            item_selection = input(invalid_input_msg)


def create_new_aws_keys():    # func to ask user about making a new AWS key pair
    print("After creating a aws key-pair your private key will be saved as a .pem file in the home directory.")
    new_key = input("Please enter a new name for a key using only letters, numbers and underscores:\n")
    try:
        create_key(new_key)    # attempting to make the key
    except:
        print("Something may have went wrong with your key creation... returning to the main menu.")
        return False
    print("Your key-pair " + new_key + " has been created. ")    # inform user, return to menu
    return


def create_key(new_key_name):    # func to actually create key pair
    ec2 = boto3.client("ec2")
    response = ec2.create_key_pair(KeyName=new_key_name)    # make the key pair
    key_p = home + "/" + new_key_name + "_Private_Key.pem"    # absolute path to new file including the filename
    priv_key_file = open(key_p, "w")    # writing the file in the users home directory with an easy to find name
    priv_key_file.write(response["KeyMaterial"])
    priv_key_file.close()    # closing the file for better performance
    oschmod.set_mode(key_p, 0o400)    # changing permissions to read only for owner and nothing for everyone else


def show_aws_keys():    # func to show all aws key pairs
    try:
        key_count = 0
        ec2 = boto3.client("ec2")
        response = ec2.describe_key_pairs()
        print("These are your current AWS keys:\n")    # printing each key pair name
        for key_pair in response["KeyPairs"]:
            key_count += 1
            print(f'  {key_count}. {key_pair["KeyName"]}')
        print(f'  ({key_count} Total AWS keys)')    # printing total number of keys
    except:
        print("Something may have went wrong when displaying your keys... returning to the main menu.")
        return


def check_instance_health_meta(new_instance_id):    # func to return instance health check status
    ec2 = boto3.resource("ec2")
    for status in ec2.meta.client.describe_instance_status()["InstanceStatuses"]:
        if status["InstanceId"] == new_instance_id:
            return status["InstanceStatus"]["Status"]


def get_instance_pub_ip(new_instance_id):    # func to get the newly created instances public IP address
    ec2 = boto3.resource("ec2")
    instances = ec2.instances.filter(
        InstanceIds=[
            new_instance_id,
        ],
    )
    for instance in instances:
        return instance.public_ip_address


def create_instance():    # func to create a new EC2 instance with a key of the users choice (everything else hardcoded)
    ec2 = boto3.resource("ec2")    # making a new security group
    sg = ec2.create_security_group(GroupName="My_Boto3_Helper_Security_Group",
                                   Description="Security Group attached to Boto3 Helper Instance")
    ec2 = boto3.client("ec2")    # assigning permissions to the new security group
    data = ec2.authorize_security_group_ingress(
        GroupId=sg.group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,    # port for SSH
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    security_group_id = sg.group_id
    print(' This will create new a T2.Micro instance with the name "my-boto3-helper-instance" ')
    print(" You will need the name of and access to an AWS private key (usually a .pem or .ppk file) ")
    new_instance_key = input(" Enter a key name you have access to for your instance:\n")    # ask for a key name
    ami_id = "ami-0c02fb55956c7d316"
    ec2 = boto3.resource("ec2")
    new_instance = ec2.create_instances(    # make the instance
        MinCount=1,    # just one
        MaxCount=1,
        ImageId=ami_id,    # a free tier ami id
        InstanceType="t2.micro",    # again free tier eligible
        KeyName=new_instance_key,    # key the user selected
        SecurityGroupIds=[security_group_id],    # attaching the new security group to the instance
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "my-boto3-helper-instance"    # naming the instance so the user can easily find it
                    },
                ]
            },
        ]
    )
    for instance in new_instance:
        print(f' EC2 instance "{instance.id}" has been launched, and is currently pending.')
        instance.wait_until_running()    # waiting for instance to graduate from pending state to running state
        print(f' EC2 instance "{instance.id}" has been started, and is waiting on health checks.')
        print(" This may take a few minutes.")
        timer = 1
        while check_instance_health_meta(instance.id) != "ok":    # waiting for health checks to complete
            if timer == 1:    # checking every 5 seconds and every 30 seconds printing the current status
                sys.stdout.write(" Initializing")
                sys.stdout.flush()
                time.sleep(1)
                print_slow("...." + "\n")    # the 5-second status print includes a 1-second print delay between each .
                timer += 1
            if timer == 6:
                time.sleep(5)
                timer = 1
                continue
            else:
                time.sleep(5)
            timer += 1
        new_pub_ip = get_instance_pub_ip(instance.id)    # when health checks pass inform user and print public IP
        print(f'\n Your instance "{instance.id}" has passed the health checks and is now finished!')
        print(f' Its name is: "my-boto3-helper-instance" and Its Public IPv4 address is: "{new_pub_ip}"\n')
        return


def stop_instances():    # func to stop instance using input ID
    ids_list = []
    stop_id = input(" Enter the Instance ID to stop and press enter: ")
    try:
        ids_list = [stop_id]
        ec2 = boto3.resource("ec2")
        ec2.instances.filter(InstanceIds=ids_list).stop()
    except:
        print(" Something may have went wrong with your instance stop... returning to the main menu. ")
        return
    print(" Your Instance was successfully stopped! ")
    return


def terminate_instances():    # func to terminate instance using input ID
    ids_list = []
    stop_id = input(" Enter the Instance ID to terminate and press enter: ")
    try:
        ids_list = [stop_id]
        ec2 = boto3.resource("ec2")
        ec2.instances.filter(InstanceIds=ids_list).terminate()
    except:
        print("Something may have went wrong with your instance termination... returning to the main menu. ")
        return
    print(" Your Instance was successfully terminated! ")
    return


def quit_checker(user_input_to_check):    # func to immediately quit if a user inputs quit anywhere during the program
    if str(user_input_to_check).upper() in quit_mm:
        sys.exit(quit_msg)
    return


# start menu -----------------------------------------------------------------------------------------------------------

def main_menu():    # main menu loop (the frame or skeleton of the program)
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
        elif mm_input in create_aws_Key_mm:
            create_new_aws_keys()
            continue
        elif mm_input in show_aws_Keys_mm:
            show_aws_keys()
            continue
        elif mm_input in create_ec2_instance_mm:
            create_instance()
            continue
        elif mm_input in stop_ec2_instance_mm:
            stop_instances()
            continue
        elif mm_input in terminate_ec2_instance_mm:
            terminate_instances()
            continue
        elif mm_input in quit_mm:
            sys.exit(quit_msg)
        else:
            print(invalid_input_msg)


# begin ----------------------------------------------------------------------------------------------------------------

print(welcome_msg)    # prints welcome message

time.sleep(1)    # one moment to enjoy the welcome title

main_menu()    # begin main menu loop

# Created by Zachary Smallwood
