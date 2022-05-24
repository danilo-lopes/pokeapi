from logging import exception
import requests
import json
import csv

apiBaseUrl = "https://pokeapi.co/api/v2"
pokemonsLimit = 10

def retrievePokemons( intLimit ):
    pokemonNames = []

    request = json.loads( requests.get( apiBaseUrl + f"/pokemon/?limit={intLimit}" ).text )

    for pokemon in request["results"]:
        pokemonNames.append( pokemon["name"] )

    return pokemonNames

def retrievePokemonAttr( pokemon ):
    data = {}
    pokemonTypes = []
    pokemonAbilities = []

    request = requests.get( apiBaseUrl + f"/pokemon/{pokemon}" )

    if request.status_code != 200:
        return request.status_code

    JSON = json.loads( request.text )

    data['name'] = JSON['name']
    for types in JSON["types"]:
        pokemonTypes.append( types["type"]["name"] )

    for abilities in JSON["abilities"]:
        pokemonAbilities.append( abilities["ability"]["name"] )

    data['types'] = pokemonTypes
    data['abilities'] = pokemonAbilities

    return json.dumps(data)

if __name__ == "__main__":
    ans=True
    while ans:
        print ("""
        1.List Pokemons
        2.List Specific Pokemon
        3.Save Pokemons to csv
        4.Exit/Quit
        """)
        ans = input("What would you like to do?: ")

        if ans == "1":
            pokemons = retrievePokemons( pokemonsLimit )
            for pokemon in pokemons:
                print( retrievePokemonAttr( pokemon ) )

        elif ans=="2":
            pokemon = input("Enter Pokemon Name: ")
            print( retrievePokemonAttr( pokemon ) )

        elif ans=="3":
            file = open("sample.svc", "w+")
            pokemons = retrievePokemons( pokemonsLimit )
            for pokemon in pokemons:
                pokemonAttr = json.loads( retrievePokemonAttr( pokemon ) )
                print(pokemonAttr)
                file.write( pokemonAttr["name"] + "," )
                for type in pokemonAttr["types"]:
                    file.write( type + "," )

            file.close()

        elif ans=="4":
            exit(0)

        else:
            print("\n Not Valid Choice Try again")
