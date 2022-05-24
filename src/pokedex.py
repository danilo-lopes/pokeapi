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

def returnPokemons():
    pokemons = retrievePokemonsName( pokemonsLimit )
    for pokemon in pokemons:
        print( retrievePokemonAttr( pokemon ) )

def returnSpecificPokemon():
    pokemon = input("Enter Pokemon Name: ")

    print( retrievePokemonAttr( pokemon ) )

def savePokemonsToCsv():
    csvHeader = ["name", "type", "abilities"]

    pokemonsName = retrievePokemonsName( pokemonsLimit )
    pokemonsDetail = []

    for pokemonName in pokemonsName:
        pokemonsDetail.append( json.loads( retrievePokemonAttr( pokemonName ) ) )

    pokemonsDetail.sort( key=lambda x: x["abilities"] )
    with open(f'sample-{YEAR}-{MONTH}-{DATE}-{HOUR}-{MINUTE}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(csvHeader)

        for pokemon in pokemonsDetail:
            writer.writerow([pokemon['name'], pokemon['types'], pokemon['abilities']])

def retrievePokemonsName( intLimit ):
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
            returnPokemons()

        elif ans=="2":
            returnSpecificPokemon()

        elif ans=="3":
            savePokemonsToCsv()

        elif ans=="4":
            exit(0)

        else:
            print("\n Not Valid Choice Try again")
