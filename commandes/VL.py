def display_str_calibrated(chaine:str,longeur:int)->str:
    """renvoie une chaine str calibrée

    Args:
        chaine ([str]): [chaine a travailler]
        longeur ([type]): [longeur de la chaine a renvoyer]

    Returns:
        [str]: [chaine, avec une longeur de longeur]
        chaine vide si trop long
    """    
    if len(chaine)==longeur:
        return chaine
    if len(chaine)<longeur:
        return chaine+(" "*(longueur-len(chaine)))
    return " "*longeur

async def VL(DiscordClient,message,args):
    if len(args)==1 or int(args[1])>15 or int(args[1]) < 2 :
        return
    dips = False
    if len(args)>2 and args[2]=="dips":
        dips=True
    liste=DiscordClient.connectionBDD.get_classement_attaques(int(args[1]), dips, limit=10, clan=None, nb_etoiles=3)
    if len(liste)==0:
        return await message.channel.send("pas de donnés")
    reponse = "      __**classement des membres hdv {}{}**__".format(int(args[1])," dips" if dips else "")
    reponse +="```{}| 3 | 2 | 1 | 0 |nb |tag".format(display_str_calibrated("pseudo",33))
    for e in liste:
        nom=e[2]
        if e[2] is not None:
            discordmember = await DiscordClient.fetch_member(int(e[1]))
            nom = discordmember.display_name
        reponse+="\n{}|{}|{}|{}|{}|{}|{}".format(display_str_calibrated(nom,33),
                                              display_str_calibrated(str(e[5]),3),
                                              display_str_calibrated(str(e[6]),3),
                                              display_str_calibrated(str(e[7]),3),
                                              display_str_calibrated(str(e[8]),3),
                                              display_str_calibrated(str(e[4]),3),
                                              e[0])
    reponse+="""```"""
    return await message.channel.send(reponse)
