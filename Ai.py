import requests

key = '882B75E94431CD842CCD402F7E9C1A73'
friendlist = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid=76561197960435530&relationship=friend')
frnJson = friendlist.json()
news = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=440&count=3&maxlength=300&format=json')
newsJson = news.json()
achievements = requests.get('http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=440&format=xml')
playerSum = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids=76561197960435530')
sumJson = playerSum.json()
playerAchievements = requests.get(f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=440&key={key}&steamid=76561197972495328')
plyAch = playerAchievements.json()
userStats = requests.get(f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=440&key={key}&steamid=76561197972495328')
stats = userStats.json()
ownedGames = requests.get(f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=440&key={key}&steamid=76561197972495328')
oGa = ownedGames.json()
recentlyGames = requests.get(f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid=76561197960434622&format=json')
recGa = recentlyGames.json()
def insert(lst, grens, waarde):
    """
    Voeg gegeven waarde in op de juiste plek van het gesorteerde deel van gegeven lijst.
    Er wordt gekeken vanaf de gegeven grens.

    Args:
        lst (list): Een lijst met elementen van gelijk type, bijvoorbeeld gehele getallen. Deze lijst
            is reeds gesorteerd van index 0 tot en met index `grens`, dus het deel `lst[0]` tot en
            met `lst[grens]`.
        grens (int): De index tot waar gegeven lijst `lst` al is gesorteerd.
        waarde (int): Het element dat op de juiste plek moet worden ingevoegd in het reeds gesorteerde
            deel van de lijst.
    """
    # Aanpak: begin bij index `grens` en verplaats elementen groter dan `waarde` naar rechts.
    # Als je een waarde tegenkomt die kleiner is dan `waarde` (of het begin van lijst `lst`),
    # dan voeg je `waarde` in op de vrijgekomen plek.
    sorted = False
    for gre in range(grens, -1, -1):    #Gaat door alle waarden in de lijst vanaf rechts naar links
        if lst[gre] >= waarde:          #Er wordt gecheckt of de getal dat bekeken wordt, hoger is dan de nieuwe waarde.
                lst[gre + 1], lst[gre] = lst[gre], waarde   #Als dat zo is, is die index niet correct voor de nieuwe waarde, dus wordt het getal een plek naar rechts verplaatst.
        else:       #Is het niet groter, dan breekt de loop
            sorted = True
            break
    if sorted == False: #Als de sub-array nog steeds niet helemaal gesorteerd is, betekent dat de nieuwe waarde de laagste is, dus meest linker index = de nieuwe waarde
        lst[0] = waarde
    return lst


def insertion_sort(lst):
    """
    Sorteer gegeven lijst volgens het insertion sort algoritme.

    Zorg dat de gegeven lijst niet verandert, maar geef een nieuwe, gesorteerde variant van de lijst terug.

    Args:
        lst (list): Een lijst met elementen van gelijk type, bijvoorbeeld gehele getallen.

    Returns:
        list: Een nieuwe, gesorteerde variant van lijst `lst`.
    """
    # Kopieer de lijst, zodat de originele lijst niet verandert
    lst_sorted = lst.copy()
    index = -1
    for getal in lst_sorted:    #Gaat door hele ongesorteerde lijst
        insert(lst_sorted, index, getal)
        index += 1
    return lst_sorted

def binary_search_index(lst, target):
    """
    Bepaal de positie van gegeven element in de lijst volgens het binair zoekalgoritme.

    Args:
        lst (list): Een lijst met elementen van gelijk type, bijvoorbeeld gehele getallen.
        target (int): Een gezocht element.

    Returns:
        int: De index waar het element in de lijst staat, of -1 als het element niet in de lijst voorkomt.
    """
    found = False
    lst_part = lst
    index = []
    foundIn = -1
    for i in range(0, len(lst)):
        index.append(i)
    while found == False:  # hoelang ga je door met zoeken?
        half = int(len(lst_part) / 2)
        if len(lst_part) == 0:
            break
        elif target < lst_part[half]:
            lst_part = lst_part[:half]  #lower half
            index = index[:half]
        elif target > lst_part[half]:
            lst_part = lst_part[half + 1:]  #Upper half
            index = index[half + 1:]
        elif target == lst_part[half]:
            foundIn = index[half]
            found = True
    return foundIn

print(insertion_sort([15,7,2,3,92,6]))
print(binary_search_index(insertion_sort([15,7,2,3,92,6]),3))
print(frnJson)
print(newsJson)
print(sumJson)
print(plyAch)
print(stats)
print(oGa)
print(recGa)