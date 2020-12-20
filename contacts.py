# check out the video for this project here: https://youtu.be/0rByHLhpnuU
from os import system

# global var
# {"Alfredo" : "(123) 123-1234"}
CONTACTS = {}


def add_contact(contact_name, contact_phone_number):
    override_contact = True
    contacts = search_contacts(contact_name)

    if contacts:
        print("A contact with that name already exists")
        override_contact = prompt_for_verification(
            "Do you want to override this contact"
        )

    if override_contact:
        CONTACTS[contact_name] = contact_phone_number

    else:
        print("No changes made")


def get_all_contacts():
    # alternative using list comprehensions
    # return [(name, phone_number) for name, phone_number in CONTACTS.items()]
    contacts = []

    for name, phone_number in CONTACTS.items():
        contacts.append((name, phone_number))

    return contacts


def format_contact(contact):
    name, phone_number = contact
    return f"{name} : {phone_number}"


# contacts -> list of contacts
# a contact is a tuple
# [("Alfredo", "123-123-1234"), ("Tim", "123-123-1235")]
def print_contacts(contacts):
    # print("-" * 3 + " CONTACTS " "-" * 3)
    # print(f"{'- * 3'} CONTACTS {'-' *3}")
    print("\n--- CONTACTS ---")

    for contact in contacts:
        print(format_contact(contact))

    print()


def search_contacts(search_query=""):
    # return [(name, phone_number) for name, phone_number in CONTACTS.items() if search_query in name or search_query in phone_number]
    contacts = []

    for name, phone_number in CONTACTS.items():
        if search_query in name or search_query in phone_number:
            # search for Alfredo
            # dict item = Alfredo1
            # then True
            contacts.append((name, phone_number))

    return contacts


def prompt_for_verification(prompt):
    verified = False
    prompt_user = True

    while prompt_user:
        option = input(f"{prompt} YES/NO: ").lower()

        if option == "yes" or option == "y":
            verified = True
            prompt_user = False
        elif option == "no" or open == "n":
            verified = False
            prompt_user = False
        else:
            print("invalid option")

    return verified


# delete a contact using a name or number
def delte_contact(delete_query):
    # deletion_confirmed = True
    contact_to_delete = None

    # contacts = [(),(),()]
    contacts = search_contacts(delete_query)
    number_of_contacts = len(contacts)

    # if there are no contacts inside the list
    if not contacts:
        print("That contact does not exists")
    elif number_of_contacts > 1:
        print("Duplicate contacts found, which one do you want to delete:")

        for index in range(number_of_contacts):
            print(f"\t{index}) {format_contact(contacts[index])}")

        prompt_user = True

        while prompt_user:
            index_to_delete = input("Enter number to delete: ")

            if (
                not index_to_delete.isnumeric()
                or int(index_to_delete) > number_of_contacts - 1
            ):
                print("invalid option")
            else:
                prompt_user = False

        contact_to_delete = contacts[int(index_to_delete)]

    else:
        contact_to_delete = contacts[0]

    # confirming with user to delete contact
    print(format_contact(contact_to_delete))
    if prompt_for_verification("Are you sure that you want to delete this contact"):
        # contact_to_delete = ("alfredo", "123-123-123")
        del CONTACTS[contact_to_delete[0]]


# def print_all_contacts():
#     for name, phone_number in CONTACTS.items():
#         # Alfredo : 123-123-1234
#         # print(name + " : " + phone_number)
#         print(f"{name} : {phone_number}")


def menu():
    system("cls")
    print("1) Add a contact")
    print("2) Search for a contact")
    print("3) Print all contacts")
    print("4) Delete a contact")
    print("5) Quit")

    option = input("Enter option: ")

    if option == "1":
        contact_name = input("Enter contact name: ")
        contact_phone_number = input("Enter contact phone number: ")

        add_contact(contact_name, contact_phone_number)

    if option == "2":
        search_query = input("Enter a name or number: ")
        print_contacts(search_contacts(search_query))

    if option == "3":
        # list_of_contacts = get_all_contacts()
        # print_contacts(list_of_contacts)

        print_contacts(get_all_contacts())

    if option == "4":
        delete_query = input("Enter a name or number to delete: ")
        delte_contact(delete_query)

    if option == "5":
        exit()


while True:
    menu()
    input("press [ENTER] to return to the main menu")
