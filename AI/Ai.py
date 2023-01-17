import requests
from datetime import datetime

key = '882B75E94431CD842CCD402F7E9C1A73'
steamId = '76561198111929702'
appId = '367520'

# news = requests.get(f'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appId}&count=3&maxlength=300&format=json')
# newsJson = news.json()

achievements = requests.get(f'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={appId}&format=json')
achJson = achievements.json()

playerSum = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamId}')
sumJson = playerSum.json()

# playerAchievements = requests.get(f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appId}&key={key}&steamid={steamId}')
# plyAch = playerAchievements.json()

ownedGames = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamId}&format=json&include_appinfo=True&include_played_free_games=True')
oGa = ownedGames.json()

#Algemene statistiek functies______________________________________
def mergeSort(lst):
    """
    Sorteer functie met behulp van de divide en conquer methode.
    Args:
        lst(list): Een lijst met getallen.
    Returns:
        list: Een list die gesorteerd is.
    """
    #Hier begint het divide gedeelte van de sorteerfunctie
    if len(lst) == 1:       #Als de lst maar een getal heeft, dan is deze lijst al gesorteerd
        return lst          #en returnt het de lijst

    helft = int(len(lst) / 2)
    lstA = lst[:helft]      #Hier wordt de lijst gesplitst in twee lijsten mocht dat mogelijk zijn
    lstB = lst[helft:]

    listA = mergeSort(lstA) #Hier komt de recursie call naar voren. Dus dan splitst het de lijst verder mocht dat mogelijk zijn
    listB = mergeSort(lstB)

    #Hier gebeurt de conquer gedeelte van de sorteerfunctie
    return merge(listA, listB)  #Hier wordt een de merge functie aangeroepen om de losse lijsten te mergen

def merge(lstA, lstB):
    """
    Deze functie zorgt voor het sorteren en mergen van de lijsten.
    Het principe van deze functie is dat de functie al gedeeltelijk gesorteerde lijsten binnen krijgt.
    Hierdoor is de vergelijking alleen nodig voor de eerste index.
    :param lstA (list): lijst met getallen
    :param lstB (list): lijst met getallen
    :return: list: De gemerged en gesorteerde lijst van de twee parameters
    """
    lstC = []               #Start met een lege lijst, wat uit eindelijk de nieuwe gesorteerde lijst wordt

    while len(lstA) != 0 and len(lstB) != 0:
        if lstA[0] > lstB[0]:       #Als de waarde van lstA op index 0 groter is dan die van lstB
            lstC.append(lstB[0])    #Dan wordt de kleinere waarde in de nieuwe lijst gestopt op het einde, omdat dat dan de laatste en grootste waarde zal zijn die toegevoegd zal zijn.
            lstB.remove(lstB[0])    #Vervolgens wordt diezelfde waarde uit de lijst gehaald
        else:
            lstC.append(lstA[0])    #Mocht de waarde van lstA[0] niet groter zijn, dan wordt er hetzelfde gedaan als hierboven maar dan voor lstA
            lstA.remove(lstA[0])

    #Mocht de ene lijst langer zijn dan de ander, vanwege een oneven lengte bijvoorbeeld, dan worden die waarden
    #nog aan het einde van de nieuwe lijst geplakt
    while len(lstA) != 0:
        lstC.append(lstA[0])
        lstA.remove(lstA[0])

    while len(lstB) != 0:
        lstC.append(lstB[0])
        lstB.remove(lstB[0])

    return lstC

def bigToSmallSort(lst):
    """
    Sorteert op grootste waarde eerst naar kleinste
    :param lst:
    Te soorteren lijst
    :return:
    Gesoorterde lijst
    """
    revLst = mergeSort(lst)
    revLst.reverse()
    return revLst

def freq(lst):
    """
    Bepaal de frequenties van alle getallen in een lijst.
    Args:
        lst (list): Een lijst met gehele getallen.
    Returns:
        dict: Een dictionary met als 'key' de waardes die voorkomen in de lijst
            en als 'value' het aantal voorkomens (de frequentie) van die waarde.
    Examples:
        >> freq([0, 0, 4, 7, 7])
        {0: 2, 4: 1, 7: 2}
        >> freq([1, 1, 2, 3, 2, 1])
        {1: 3, 2: 2, 3: 1}
    """
    freqs = {}
    for getal in lst:                       #Een teller met behulp van een dictionary, met als getal de key en het aantal de value van de key
        if getal not in freqs.keys():       #Als een waarde niet in de dictionary zit, wordt er een nieuwe key gemaakt met de getal
            freqs[getal] = 1
        else:                               #Als het er wel al in staat gaat de teller 1 omhoog
            freqs[getal] += 1
    return freqs

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

#Specifieke methoden met API-calls_________________________________

def friendlistData(steamId):
    """
    Deze functie zorgt ervoor dat er een API call gedaan wordt die de info
    request voor alle vrienden van een bepaalde steam user. Deze informatie
    wordt verwerkt in een dictionary.
    Args:
        steamid: steamId van de gevraagde user
    Returns:
    Een dictionary van alle vrienden met de steamid als de key en de naam als waarde
    """
    #Mocht de profiel prive zijn, dan zal er een error ontstaan, dus alles in een try gezet.
    try:
        # Data van API krijgen
        friendlist = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={steamId}&relationship=friend')
        frnJson = friendlist.json()

        # Aantal vrienden
        friends = 0
        for friend in frnJson['friendslist']['friends']:
            friends = friends + 1

        # Maakt lange string aan met de ID's uit de friendslist die
        frnsIDs = ''
        for friend in frnJson['friendslist']['friends']:
            frnsIDs += f'{friend["steamid"]},'

        request = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={frnsIDs}')
        friendsJson = request.json()
        frnDic = {}
        for friend in friendsJson['response']['players']:
            frnDic[friend['steamid']] = {'name': friend['personaname'], 'avatar':friend['avatarmedium']}
    except:     #Is de profiel prive, dan is de dictionary leeg
        frnDic = {}
    return frnDic

def flipIDData(dic):
    """
    Flipt een dictionary mocht het handig zijn om te sorteren op alfabetische volgorde ipv id's
    Args:
        dic: Dictionary met id als key en naam als waarde
    Returns:
    De geflipte dictionary
    """
    cid = {}
    for id, data in dic.items():
        cid[data['name']], data['name'] = data, id
    return cid

def games2Weeks(steamId):
    """
    Zoekt op wat de laatste games zijn die de user heeft gespeeld afgelopen twee weken
    Args:
        steamId: Steamid van gevraagde user
    Returns:
    Een dictionary met de id van de game als key en naam van de game als value
    """
    #Als de profiel prive is gaat er een error komen
    try:
        #De API call
        recentlyGames = requests.get(
            f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamId}&format=json')
        recGa = recentlyGames.json()

        games2weeks = {}
        for game in recGa['response']['games']:
            games2weeks[game['appid']] = {'name': game['name'], 'playtime_2weeks': game['playtime_2weeks'], 'playtime': game['playtime_forever']}

    except: #Dus als het prive is dan geeft het een lege dictionary terug
        games2weeks = {}
    return games2weeks

def ownedGames(steamId):
    """
    Pakt alle informatie over owned games
    Args:
        steamId: steamid van user
    Returns:
    Dictionary met id als key en data als value
    """
    # Als de profiel prive is gaat er een error komen
    oGaDic = {}
    try:
        #De API call
        ownedGames = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamId}&format=json&include_appinfo=True&include_played_free_games=True')
        oGa = ownedGames.json()

        for game in oGa['response']['games']:
            oGaDic[game['appid']] = {'name': game['name'], 'playtime': game['playtime_forever']}

    except: #Dus als het prive is dan geeft het een lege dictionary terug
        pass
    return oGaDic


def allAchievements(steamId, appId):
    """
    Gets achievements data
    :param steamId:
    :param appId:
    :return:
    """
    achDic = {}

    try:
        playerAchievements = requests.get(
            f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appId}&key={key}&steamid={steamId}')
        plyAch = playerAchievements.json()

        count = 0
        achieved = 0
        for achievement in plyAch['playerstats']['achievements']:
            achDic[achievement['apiname']] = {'achieved': achievement['achieved'], 'unlocktime': achievement['unlocktime']}
            if achievement['achieved']:
                achieved += 1
            count += 1
        achDic['achCount'] = count          #Aantal achievements
        achDic['achAchieved'] = achieved    #Aantal behaalde achievements
        achDic['achProcent'] = (achieved/count) * 100 #Percentage achievements

    except:
        pass

    return achDic
def recentGamesAchievements(steamId, appId):
    """
    Returns the recently achieved achievements of a certain game
    :param steamId: steamid van user waarvan je info wil hebben
    :param appId: appid van de app die gevraagd wordt
    :return:
    dictionary met twee lijsten
    """
    recAchDic = {}

    try:
        achDic = allAchievements(steamId, appId)

        ciDhca = {}
        for name, data in achDic.items():
            if type(data) == int or type(data) == float:
                pass
            else:
                ciDhca[data['unlocktime']], data['unlocktime'] = data, name

        times = []
        for time in ciDhca.keys():
            times.append(time)
        recUnlockTime = bigToSmallSort(times)

        recAch = []
        for time in recUnlockTime[:11]:
            recAch.append(ciDhca[time]['unlocktime'])

        recAchDic = {'time': recUnlockTime[:11], 'name': recAch}
    except:
        pass

    return recAchDic

'''print(datetime.utcfromtimestamp(1284101485).strftime('%Y-%m-%d %H:%M:%S'))  #https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
print(friendlistData(steamId))
print(flipIDData(friendlistData(steamId)))
print(games2Weeks(steamId))
print(flipIDData(games2Weeks(steamId)))
print(ownedGames(steamId))
print(flipIDData(ownedGames(steamId)))
#print(newsJson) skip?
print(achJson)
print(sumJson)
playerAchievements = requests.get(f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appId}&key={key}&steamid={steamId}')
plyAch = playerAchievements.json()
print(plyAch)
print(allAchievements(steamId,appId))
print(recentGamesAchievements(steamId, appId))
#1145360 Hades
print(oGa)'''