import json
import webbrowser
import Sensitivedata.credentials
import requests


def get_json_content_from_response(response):
    try:
        content = response.json()
    except json.decoder.JSONDecodeError:
        print("Invalid format",response.text)
    else:
        return content

def get_favourite_cats(userId):
    params = {
        "sub_id" : userId
    }
    r = requests.get(" https://api.thecatapi.com/v1/favourites/", params,
                     headers=Sensitivedata.credentials.headers)

    return get_json_content_from_response(r)

def get_random_cat():
    r = requests.get(" https://api.thecatapi.com/v1/images/search",
                     headers=Sensitivedata.credentials.headers)

    return get_json_content_from_response(r)[0]

def add_favoutite_cat(catId,userId):
    catData = {
        "image_id" : catId,
        "sub_id" : userId
    }
    r = requests.post("https://api.thecatapi.com/v1/favourites/", json=catData,
                      headers=Sensitivedata.credentials.headers)
    return get_json_content_from_response(r)

def remove_favourite_cat(userId,favouriteCatIdToRemove):
    r = requests.delete("https://api.thecatapi.com/v1/favourites/" + favouriteCatIdToRemove,
                        headers=Sensitivedata.credentials.headers)
    return get_json_content_from_response(r)

def display_cats(favouriteCats):
    for count,cat in enumerate(favouriteCats,start=1):
        print(f"My {count} favourite cat [ id: {cat['id']} address url: {cat['image']['url']} ]")

# 1
userId = "dav123"
name = "Dawid"
print("Welcome " + name)

# 2 - start program

password = input("Give your password: ")
if password == Sensitivedata.credentials.password:
    print("Access was granted!!!")

    while True:

        favouriteCats = get_favourite_cats(userId)

        choice = input("""
=======================================================================================        
Select your option!!!
1 -> Display your favourites cats
2 -> Generate a random cat -> If you want we can add it here to your favourites
3 -> Remove the cat
4 -> Finish the program
=======================================================================================  
Select: \n""")

        #favorites cats get
        if choice == '1':
            display_cats(favouriteCats)
            continue
        #random cat get and adding to the favourites
        elif choice == '2':
            randomCat = get_random_cat()
            print("Randomly selected cat: " , randomCat['url'])

            # -> Display on the web site
            displayRandomCatOnTheWebSite = input("Do you want to display this cat on the web site? Y/N \n")
            if displayRandomCatOnTheWebSite.upper() == 'Y':
                webbrowser.open_new_tab(randomCat['url'])
            else:
                print("Okej so next question ...")

            # -> Add it to favourite
            addChoice = input("Do you want to add it to favoutites? Y/N :\n")
            if addChoice.upper() == 'Y':
                print(add_favoutite_cat(randomCat['id'],userId))
            else:
                print("So if you dont want to add it then please select new option again ")
                continue
        #Remove the cat
        elif choice == '3':
            catsAndTheirIds = input("To see your all cats which are into your list and their id's ( click 'enter' ) : ")
            display_cats(favouriteCats)
            catIdToRemove = input("To remove the cat , please give its id: ")
            print(remove_favourite_cat(userId,catIdToRemove))
        #Finish the program
        elif choice == '4':
            print("Good bye!!!")
            break
        # Wrong choice
        else:
            print("Your choice was wrong try again ")
        continue

else:
    print("You wrote the wrong password , you are not " + name)