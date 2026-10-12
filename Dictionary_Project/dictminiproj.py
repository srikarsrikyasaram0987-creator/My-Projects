dict={}
while True:
    print("1. Add a word")
    print("2. Search for Meaning")
    print("3. Display all Words")
    print("4. Update the Meaning")
    print("5. Delete the Word")
    print("6. Exit")

    choice=input("Enter the choice: ")

    if choice=="1":
        word=input("Enter a Word: ").lower()
        meaning=input("Enter a Meaning: ").lower()
        dict[word]=meaning
        print("word and meaning added sucessfully....")

    elif choice=="2":
        word=input("Enter a Word: ").lower() 
        if word in dict:
            print("meaning",dict[word])
        else:
            print("Its not in dictionary")    

    elif choice=="3":
        if dict:
            print("print words and meaning")
            for word,meaning in dict.items():
                print(f"{word}:{meaning}")
        else:
            print("Dictionary is empty")

    elif choice=="4":
        word=input("Enter a Word: ").lower()
        if word in dict:
            new_meaning=input("Enter the new meaning: ")
            dict[word]=new_meaning
            print("Meaning update successfully...")
            print("updated Meaning:",dict[word])
        else:
            print("It is not found in Dictionary")

    elif choice=="5":
        word=input("Enter a Word: ")
        if word in dict:
            del dict[word]
            print("word deleted Successfully...")
        else:
            print("It is not found in Dictionary")
    elif choice=="6":
        print("Exited")
        break
    else:
        print("invalid: Give numbers in between 1 to 6.")