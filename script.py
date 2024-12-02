command = ""
while command != "quit":
    command = input(">").lower()
    if command == "start":
        print("The car started....")
    elif command == "stop":
        print("The car stopped...")
    elif command == "help":
        print(""" 
            start - start command
            """)
        
    