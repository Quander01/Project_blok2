import requests

key = '882B75E94431CD842CCD402F7E9C1A73'
steamId = '76561198111929702'
appId = '367520'


# Algemene statistiek functies______________________________________
def mergeSort(lst):
    """
    Sorteer functie met behulp van de divide en conquer methode.
    Args:
        lst(list): Een lijst met getallen.
    Returns:
        list: Een list die gesorteerd is.
    """
    # Hier begint het divide gedeelte van de sorteerfunctie
    if len(lst) == 1:  # Als de lst maar een getal heeft, dan is deze lijst al gesorteerd
        return lst  # en returnt het de lijst

    helft = int(len(lst) / 2)
    lstA = lst[:helft]  # Hier wordt de lijst gesplitst in twee lijsten mocht dat mogelijk zijn
    lstB = lst[helft:]

    listA = mergeSort(lstA)  # Hier komt de recursie call naar voren.
    listB = mergeSort(lstB)  # Dus dan splitst het de lijst verder mocht dat mogelijk zijn

    # Hier gebeurt de conquer gedeelte van de sorteerfunctie
    return merge(listA, listB)  # Hier wordt een de merge functie aangeroepen om de losse lijsten te mergen


def merge(lstA, lstB):
    """
    Deze functie zorgt voor het sorteren en mergen van de lijsten.
    Het principe van deze functie is dat de functie al gedeeltelijk gesorteerde lijsten binnen krijgt.
    Hierdoor is de vergelijking alleen nodig voor de eerste index.
    :param lstA: lijst met getallen
    :param lstB: lijst met getallen
    :return: list: De gemerged en gesorteerde lijst van de twee parameters
    """
    # Start met een lege lijst, wat uit eindelijk de nieuwe gesorteerde lijst wordt
    lstC = []

    while len(lstA) != 0 and len(lstB) != 0:
        # Als de waarde van lstA op index 0 groter is dan die van lstB,
        # dan wordt de kleinere waarde in de nieuwe lijst gestopt op het einde,
        # omdat dat dan de laatste en grootste waarde zal zijn die toegevoegd zal zijn.
        # Vervolgens wordt diezelfde waarde uit de lijst gehaald
        if lstA[0] > lstB[0]:
            lstC.append(lstB[0])
            lstB.remove(lstB[0])

        # Mocht de waarde van lstA[0] niet groter zijn,
        # dan wordt er hetzelfde gedaan als hierboven maar dan voor lstA
        else:
            lstC.append(lstA[0])
            lstA.remove(lstA[0])

    # Mocht de ene lijst langer zijn dan de ander, vanwege een oneven lengte bijvoorbeeld, dan worden die waarden
    # nog aan het einde van de nieuwe lijst geplakt
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
    List = mergeSort(lst)
    revLst = []
    for i in range(-1, -(len(List) + 1), -1):
        revLst.append(List[i])
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
    for getal in lst:
        # Als een waarde niet in de dictionary zit, wordt er een nieuwe key gemaakt met de getal
        if getal not in freqs.keys():
            freqs[getal] = 1
        else:  # Als het er wel al in staat gaat de teller 1 omhoog
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
    while not found:  # hoelang ga je door met zoeken?
        half = int(len(lst_part) / 2)
        if len(lst_part) == 0:
            break
        elif target < lst_part[half]:
            lst_part = lst_part[:half]  # lower half
            index = index[:half]
        elif target > lst_part[half]:
            lst_part = lst_part[half + 1:]  # Upper half
            index = index[half + 1:]
        elif target == lst_part[half]:
            foundIn = index[half]
            found = True
    return foundIn


def mean(lst):
    """
    Bepaal het gemiddelde van een lijst getallen.
    De standaard formule wordt gebruikt van gemiddelde
    namelijk alle waarden van een lijst plus elkaar
    gedeeld door aantal waarden
    Args:
        lst (list): Een lijst met gehele getallen.
    Returns:
        float: Het gemiddelde van de gegeven getallen.
    """
    plus = 0
    for getal in lst:
        plus = plus + getal  # Hier worden alle waarden bij elkaar opgeteld
    return plus / len(lst)  # Hier is de deling met het aantal waarden


# Specifieke methoden met API-calls_________________________________

def privateChecker(steamId):
    """
    Controleert of een account prive is of niet en of de vrienden- en gameslijst prive is of niet
    :param steamId: steamId van gevraagde account
    :return:
    Een dictionary met booleans erin die aangeven wat wel of niet prive is of niet
    """
    try:
        request = requests.get(
                f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamId}')
        userData = request.json()
    except requests.exceptions.JSONDecodeError:
        return None
    # Geeft lege lijst mee als de id invalide is
    if len(userData['response']['players']) == 0:
        return None
    state = {}
    # Geeft 1 als het prive is
    if userData['response']['players'][0]['communityvisibilitystate'] == 1:
        state['friends'], state['games'] = True, True
        return state
    # Geeft 3 als het openbaar is
    if userData['response']['players'][0]['communityvisibilitystate'] == 3:
        state['friends'], state['games'] = False, False

    # Als het profiel publiek is, maar vriendenlijst prive
    friendlist = requests.get(
        f'https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={steamId}&relationship=friend')
    frnJson = friendlist.json()
    if len(frnJson) == 0:
        state['friends'] = True
    # Als het profiel publiek is, maar gamelijst prive
    recentlyGames = requests.get(
        f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamId}&format=json')
    recGa = recentlyGames.json()
    if len(recGa['response']) == 0:
        state['games'] = True
    return state


def friendlistData(steamId):
    """
    Deze functie zorgt ervoor dat er een API call gedaan wordt die de info
    request voor alle vrienden van een bepaalde steam user. Deze informatie
    wordt verwerkt in een dictionary.
    Args:
        steamId: steamId van de gevraagde user
    Returns:
    Een dictionary van alle vrienden met de steamid als de key en de naam en profielfoto als waarde
    """
    # Als de ingevulde steamID invalid is, return 0
    try:
        # Functie dat data van een externe bron binnenhaalt
        friendlist = requests.get(
            f'https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={steamId}&relationship=friend')
        frnJson = friendlist.json()
    # Als de ingevulde steamId niet klopt dan geeft het een 0 terug
    except requests.exceptions.JSONDecodeError:
        return None
    # De API zal een lege dictionary returnen als het profiel geen vrienden heeft
    if len(frnJson['friendslist']['friends']) == 0:
        return {}
    # Aantal vrienden
    friends = 0
    for friend in frnJson['friendslist']['friends']:
        friends = friends + 1
    # Maakt lange string aan met de ID's uit de friendslist die
    # in de Api-call gedaan wordt.
    frnsIDs = ''
    for friend in frnJson['friendslist']['friends']:
        frnsIDs += f'{friend["steamid"]},'
    # frnsIDs wordt in de API als argument ingevuld
    request = requests.get(
        f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={frnsIDs}')
    friendsJson = request.json()
    frnDic = {}
    for friend in friendsJson['response']['players']:
        frnDic[friend['steamid']] = {'name': friend['personaname'], 'avatar': friend['avatarmedium']}
    return frnDic


def sortedFriends(steamId, key):
    """
    Returned vriendenlijst op of alfabetische volgorde, of op id
    :param steamId:
    :param key: 0 of 1: 0 staat voor alfabetisch 1 staat voor op id
    :return:
    Een gesorteerde lijst met namen of id's
    """
    dic = friendlistData(steamId)

    # Als de friendlistData() functie niks terug geeft dan geeft de functie 0 terug
    if len(dic) == 0:
        return {}
    # lst is de lijst met alle id's of namen
    # srtLst is de gesorteerde lijst
    lst = []
    srtLst = []
    # Sorteren op alfabetische volgorde
    if key == 0:
        lstLowerIndexDic = {}
        index = 0
        # Twee dictionaries worden gebruikt om data terug te kunnen vinden
        for name in dic.values():
            # Slaat de naam in lowercase op in lst
            lst.append(name['name'].lower())
            # Andere dictionary met de lowercased naam als key en de oorspronkelijke naam als value
            lstLowerIndexDic[name['name'].lower()] = name['name']
            index += 1
        srtLstLower = mergeSort(lst)
        # Vult de gesorteerde lowercased namen in de dictionary
        # met oude index om de originele naam terug te krijgen
        for name in srtLstLower:
            srtLst.append(lstLowerIndexDic[name])

    # Sorteren op id
    elif key == 1:
        for id in dic.keys():
            lst.append(id)
        srtLst = mergeSort(lst)
    return srtLst


def flipIDData(dic):
    """
    Maakt een nieuwe dictionary aan die de plaats van id en naam verandert
    Args:
        dic: Dictionary met id als key en naam en profielfoto als waarde
    Returns:
    Dezelfde dictionary, maar met naam als key en id en profielfoto als waarde
    """
    cid = {}
    dicCopy = dic
    for id, data in dicCopy.items():
        cid[data['name']] = {'id': id, 'avatar': data['avatar']}
    return cid


def games2Weeks(steamId):
    """
    Zoekt op wat de laatste drie games zijn die de user heeft gespeeld afgelopen twee weken
    Args:
        steamId: Steamid van gevraagde user
    Returns:
    Een dictionary met de id van de game als key en naam, speeltijd van afgelopen
    twee weken en algemene speeltijd van de game als value
    """
    # Als de ingevulde waarde niet klopt dan return 0
    try:
        # De API call
        recentlyGames = requests.get(
            f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamId}&format=json')
        recGa = recentlyGames.json()
    except requests.exceptions.JSONDecodeError:
        return None

    # Als het profiel geen games heeft afgelopen twee weken, dan return 0
    if recGa['response']['total_count'] == 0:
        return {}
    games2weeks = {}
    i = 0
    for game in recGa['response']['games']:
        if i < 3:
            games2weeks[game['appid']] = {'name': game['name'], 'playtime_2weeks': game['playtime_2weeks'],
                                          'playtime': game['playtime_forever']}
        else:
            break
        i += 1
    return games2weeks


def ownedGames(steamId):
    """
    Haalt alle informatie op over owned games
    Args:
        steamId: steamid van user
    Returns:
    Dictionary met id als key en naam en speeltijd als value
    """
    # Als het ingevulde steamID invalide is, dan return 0
    try:
        # De API call
        ownedGames = requests.get(
            f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamId}&format=json&include_appinfo=True&include_played_free_games=True')
        oGa = ownedGames.json()
    except requests.exceptions.JSONDecodeError:
        return None
    # Als het profiel publiek is, maar gameslijst wel prive
    if len(oGa['response']) == 0:
        return {}
    # Als het profiel geen spellen heeft dan is de gamecount 0 dus return 0
    if oGa['response']['game_count'] == 0:
        return {}
    oGaDic = {}
    for game in oGa['response']['games']:
        oGaDic[game['appid']] = {'name': game['name'], 'playtime': game['playtime_forever']}
    return oGaDic


def allAchievements(steamId, appId):
    """
    Haalt de achievementdata op van een bepaalde game van een user
    :param steamId: SteamID van de gevraagde gebruiker
    :param appId: AppID van de gevraagde game
    :return:
    dictionary met totale achievements, aantal behaalde, behaalde percentage
    en een dictionary met alle achievements
    """
    achDic = {}
    # Is de steamID of appID invalide dan returnt het 0
    try:
        playerAchievements = requests.get(
            f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appId}&key={key}&steamid={steamId}')
        plyAch = playerAchievements.json()
    except requests.exceptions.JSONDecodeError:
        return None
    # Als het profiel het spel niet heeft, dan return 0
    if not plyAch['playerstats']['success']:
        return {}
    tot = 0
    achieved = 0
    # Dictionary van de achievements met naam als key en behaalde status en behaalde tijdstip als value
    for achievement in plyAch['playerstats']['achievements']:
        achDic[achievement['apiname']] = {'achieved': achievement['achieved'],
                                          'unlocktime': achievement['unlocktime']}
        if achievement['achieved']:
            achieved += 1
        tot += 1
    achDicStats = {'achTot': tot, 'achAchieved': achieved, 'achprocent': (achieved / tot) * 100,
                   'achievements': achDic}
    return achDicStats


def recentGamesAchievements(steamId, appId):
    """
    Returns the recently achieved achievements of a certain game
    :param steamId: steamid van user waarvan je info wil hebben
    :param appId: appid van de app die gevraagd wordt
    :return:
    dictionary met twee lijsten: een lijst met gesorteerde tijden
    en een lijst met de bijbehorende behaalde achievements op die tijden
    """
    achDic = allAchievements(steamId, appId)

    # Checkt of de lijst leeg is of niet
    if len(achDic) == 0:
        return {}

    # Zorgt ervoor de dat unlocktime de key wordt en de naam de "unlocktime" wordt
    ciDhca = {}
    for name, data in achDic['achievements'].items():
        ciDhca[data['unlocktime']], data['unlocktime'] = data, name
    # Hier wordt alle tijden van de behaalde achievements in een lijst gezet en die wordt
    # gesorteerd op meest recent
    times = []
    for time in ciDhca.keys():
        times.append(time)

    recUnlockTime = bigToSmallSort(times)
    recAch = []
    for time in recUnlockTime[:4]:
        recAch.append(ciDhca[time]['unlocktime'])
    recAchDic = {'time': recUnlockTime[:4], 'name': recAch}
    return recAchDic


def frequencyGamesAllFriends(steamId):
    """
    Telt hoeveel van je vrienden welke games deelt met jou
    :param steamId: steamId van user
    :return:
    dictionary met twee gesorteerde lijsten. Lijst met namen en frequenties
    """
    friendsDic = friendlistData(steamId)

    # Als het profiel leeg is dan geeft het 0 terug
    if len(friendsDic) == 0:
        return {}

    # List met alle namen van alle games die de vrienden heeft van de gebruiker
    lstAllName = []
    for id in friendsDic.keys():
        ownGamDic = ownedGames(id)
        if len(ownGamDic) != 0:
            for name in ownGamDic.values():
                lstAllName.append(name['name'])

    # Telt de frequentie van alle games
    freqDic = freq(lstAllName)
    copyDic = freqDic

    frequencies = []
    for fre in copyDic.values():
        frequencies.append(fre)
    stbFre = mergeSort(frequencies)
    btsFre = bigToSmallSort(stbFre)
    top5 = btsFre[:5]
    copy5 = top5

    names = []
    # Pakt de 5 hoogste frequenties van de frequentieteller van de games
    # Gaat door alle games heen om te kijken welke dezelfde frequentie heeft
    # Verwijdert uit beide de lijst en dictionary om dubbele data te verkomen
    while len(copy5) != 0:
        for name, frequency in copyDic.items():
            if copy5[0] == copyDic[name]:
                names.append(name)
                copy5.pop(0)
                copyDic.pop(name)
                break
    top5MostPlayed = {'name': names, 'frequency': btsFre[:5]}
    return top5MostPlayed


def averageGames2Weeks(steamId):
    """
    Berekent de gemiddelde speeltijd van de spellen
    van afgelopen 2 weken.
    :param steamId:
    De steamId wiens gegevens we willen.
    :return:
    Returnt het aantal minuten gemiddeld tussen alle spellen.
    """
    # Als de ingevulde steamID niet valide is, dan return 0
    try:
        recentlyGames = requests.get(
            f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamId}&format=json')
        recGa = recentlyGames.json()
    except requests.exceptions.JSONDecodeError:
        return None

    # Als het profiel afgelopen twee weken niet gespeeld heeft
    if recGa['response']['total_count'] == 0:
        return {}
    speeltijdenLst = []
    for game in recGa['response']['games']:
        speeltijdenLst.append(game['playtime_2weeks'])
    average = mean(speeltijdenLst)
    return average