import requests
import datetime
import json
import csv

YEAR = datetime.date.today().year
MONTH = datetime.date.today().month
DATE = datetime.date.today().day
HOUR = datetime.datetime.now().hour
MINUTE = datetime.datetime.now().minute

apiBaseUrl = "https://pokeapi.co/api/v2"
pokemonsLimit = 10

menu_options = {
    1: 'See All Pokemons',
    2: 'See Specific Pokemon',
    3: 'Save Pokemons to csv',
    4: 'Exit/Quit',
}

def returnPokemons():
    pokemonsList = []

    pokemonsNameList = retrieveListOfPokemonsName( pokemonsLimit )
    for pokemon in pokemonsNameList:
        pokemonsList.append( json.loads( retrievePokemonAttrs( pokemon ) ) )

    pokemonsList.sort( key=lambda x: x["abilities"] )

    for pokemon in pokemonsList:
        print( f"Name {pokemon['name']}" )
        print( f"Types {pokemon['types']}" )
        print( f"Abilities {pokemon['abilities']}" )
        print("--")

def returnSpecificPokemon():
    pokemonInput = input("Enter Pokemon Name: ")

    pokemon = json.loads( retrievePokemonAttrs( pokemonInput ) )

    print( f"Name {pokemon['name']}" )
    print( f"Types {pokemon['types']}" )
    print( f"Abilities {pokemon['abilities']}" )
    print("--")

def savePokemonsToCsv():
    pokemonsNameList = retrieveListOfPokemonsName( pokemonsLimit )
    pokemonsList = []

    for pokemonName in pokemonsNameList:
        pokemonsList.append( json.loads( retrievePokemonAttrs( pokemonName ) ) )

    pokemonsList.sort( key=lambda x: x["abilities"] )

    csvHeader = ["name", "type", "abilities"]
    with open(f'sample-{YEAR}-{MONTH}-{DATE}-{HOUR}-{MINUTE}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(csvHeader)

        for pokemon in pokemonsList:
            writer.writerow([pokemon['name'], pokemon['types'], pokemon['abilities']])

def retrieveListOfPokemonsName( intLimit ):
    pokemons = []

    request = json.loads( requests.get( apiBaseUrl + f"/pokemon/?limit={intLimit}" ).text )

    for pokemon in request["results"]:
        pokemons.append( pokemon["name"] )

    return pokemons

def retrievePokemonAttrs( pokemon ):
    data = {}
    pokemonTypes = []
    pokemonAbilities = []

    request = requests.get( apiBaseUrl + f"/pokemon/{pokemon}" )

    if request.status_code != 200:
        return "Pokemon Not Found or Doesnt Exists"

    JSON = json.loads( request.text )

    data['name'] = JSON['name']
    for types in JSON["types"]:
        pokemonTypes.append( types["type"]["name"] )

    for abilities in JSON["abilities"]:
        pokemonAbilities.append( abilities["ability"]["name"] )

    data['types'] = pokemonTypes
    data['abilities'] = pokemonAbilities

    return json.dumps(data)

def menu():
    for key in menu_options.keys():
        print (f"[{key}]", '-', menu_options[key] )

if __name__ == "__main__":
    ans=True
    while ans:
        menu()

        ans = input("What would you like to do?: ")

        if ans == "1":
            returnPokemons()

        elif ans=="2":
            returnSpecificPokemon()

        elif ans=="3":
            savePokemonsToCsv()

        elif ans=="4":
            exit(0)

        else:
            print("\n Not Valid Choice Try again")
