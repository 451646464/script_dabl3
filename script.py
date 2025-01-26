import time
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from colorama import Fore, Style, init
import pyfiglet


init(autoreset=True)


welcome_message = pyfiglet.figlet_format("(R_$_Script_$_L)", font="slant")
print(Fore.RED + Style.BRIGHT + welcome_message)


server_ip = input(Fore.GREEN + "(^_^) Please enter the LDAP server IP: ")


server = Server(f'ldap://{server_ip}', get_info=ALL)

conn = None 

try:
  
    conn = Connection(server, auto_bind=True)
    print(Fore.GREEN + "Connected to the server successfully!")

    print(Fore.YELLOW + "\nLoading, please wait...")
    time.sleep(1) 
    print(Fore.GREEN + "Welcome message shown.")

    while True:
        print(Fore.CYAN + "\nChoose an operation:")
        print(Fore.BLUE + "1. Search Users")
        print(Fore.BLUE + "2. Gather Domain Information")
        print(Fore.BLUE + "3. Display All Users")
        print(Fore.BLUE + "4. Display All Groups")
        print(Fore.BLUE + "5. Display Admin Information")
        print(Fore.BLUE + "6. Add User")
        print(Fore.BLUE + "7. Update User")
        print(Fore.BLUE + "8. Delete User")
        print(Fore.BLUE + "9. Display Windows Server Information")
        print(Fore.BLUE + "10. Exit")

        choice = input(Fore.CYAN + "Enter your choice: ")

        if choice == '1':
            search_term = input(Fore.CYAN + "Enter search term (e.g., username): ")
            conn.search('dc=ust,dc=local', f'(sAMAccountName={search_term})', attributes=['*'])
            print(Fore.YELLOW + f"Results found: {len(conn.entries)}")
            if conn.entries:
                print(Fore.YELLOW + "Search results:")
                for entry in conn.entries:
                    print(Fore.MAGENTA + str(entry))
            else:
                print(Fore.YELLOW + "No results found.")

        elif choice == '2':
       
            domain_info = conn.server.info
            print(Fore.YELLOW + "Domain Information:")
            print(Fore.MAGENTA + str(domain_info))

        elif choice == '3':
         
            conn.search('dc=ust,dc=local', '(objectClass=person)', attributes=['*'])
            print(Fore.YELLOW + f"Results found: {len(conn.entries)}")
            if conn.entries:
                print(Fore.YELLOW + "All Users:")
                for entry in conn.entries:
                    print(Fore.MAGENTA + str(entry))
            else:
                print(Fore.YELLOW + "No users found.")

        elif choice == '4':
         
            conn.search('dc=ust,dc=local', '(objectClass=group)', attributes=['cn', 'description'])
            print(Fore.YELLOW + f"Results found: {len(conn.entries)}")
            if conn.entries:
                print(Fore.YELLOW + "All Groups:")
                for entry in conn.entries:
                    print(Fore.MAGENTA + str(entry))
            else:
                print(Fore.YELLOW + "No groups found.")

        elif choice == '5':
      
            conn.search('dc=ust,dc=local', '(sAMAccountName=Administrator)', attributes=['*'])
            print(Fore.YELLOW + f"Results found: {len(conn.entries)}")
            if conn.entries:
                print(Fore.YELLOW + "Admin Information:")
                for entry in conn.entries:
                    print(Fore.MAGENTA + str(entry))
            else:
                print(Fore.YELLOW + "Admin not found.")

        elif choice == '6':
       
            new_user_dn = input(Fore.CYAN + "Enter new user DN (e.g., cn=newuser,ou=Users,dc=ust,dc=local): ")
            new_user_attributes = {
                'objectClass': ['inetOrgPerson', 'organizationalPerson', 'person', 'top'],
                'cn': input("Enter common name (cn): "),
                'sn': input("Enter surname (sn): "),
                'userPassword': input("Enter password: ")
            }
            if conn.add(new_user_dn, attributes=new_user_attributes):
                print(Fore.GREEN + "User added successfully!")
            else:
                print(Fore.LIGHTYELLOW_EX + f"Failed to add user: {conn.result['description']}")

        elif choice == '7':
   
            user_dn_to_update = input(Fore.CYAN + "Enter the DN of the user to update: ")
            attribute_to_update = input("Enter the attribute to update (e.g., cn, sn, userPassword): ")
            new_value = input(f"Enter new value for {attribute_to_update}: ")
            if conn.modify(user_dn_to_update, {attribute_to_update: [(MODIFY_REPLACE, [new_value])]}) and conn.result['result'] == 0:
                print(Fore.GREEN + "User updated successfully!")
            else:
                print(Fore.RED + f"Failed to update user: {conn.result['description']}")

        elif choice == '8':
            user_dn_to_delete = input(Fore.CYAN + "Enter the DN of the user to delete: ")
            if conn.delete(user_dn_to_delete) and conn.result['result'] == 0:
                print(Fore.GREEN + "User deleted successfully!")
            else:
                print(Fore.RED + f"Failed to delete user: {conn.result['description']}")

        elif choice == '9':
         
            print(Fore.YELLOW + "Windows Server Information:")
            print(Fore.MAGENTA + f"Server Name: {server_ip}")

        elif choice == '10':
            print(Fore.YELLOW + "Exiting...")
            break

        else:
            print(Fore.RED + "Invalid choice. Please try again.")

except Exception as e:
    print(Fore.RED + f"An error occurred: {e}")

finally:
    if conn:
        conn.unbind()
