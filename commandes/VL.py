import discord
def display_str_calibrated(chaine:str,longueur:int)->str:
    """renvoie une chaine str calibrée

    Args:
        chaine ([str]): [chaine a travailler]
        longueur ([type]): [longeur de la chaine a renvoyer]

    Returns:
        [str]: [chaine, avec une longeur de longeur]
        chaine vide si trop long
    """    
    if len(chaine)==longueur:
        return chaine
    if len(chaine)<longueur:
        return chaine+(" "*(longueur-len(chaine)))
    return chaine[:longueur]

async def VL(DiscordClient,message,args):
    async with message.channel.typing():
        if len(args)==1 or  not args[1].isdigit() or int(args[1])>15 or int(args[1]) < 2 :
            return
        dips = False
        if len(args)>2 and "dips" in args:
            dips=True
        clan=None
        if len(args)>2+dips:
            clan = args[2+dips] 
            
        liste=DiscordClient.connectionBDD.get_classement_attaques(int(args[1]), dips=dips, limit=25, clan=clan, nb_etoiles=3)
        if len(liste)==0:
            return await message.channel.send("pas de donnés")
        reponse = "      __**classement des membres hdv {}{}{}**__".format(int(args[1])," dips" if dips else ""," "+clan if clan is not None else "")
        reponse +="```{}|⭐⭐⭐| ⭐⭐ | ⭐ | ☆ |nb| % |tag".format(display_str_calibrated("",33))
        for e in liste:
            nom=await DiscordClient.cocClient.get_player(e[0])
            nom=nom.name
            if e[1] is not None:
                try:
                    discordmember = await message.guild.fetch_member(int(e[1]))
                except discord.errors.NotFound:
                    pass
                else:
                    nom = discordmember.display_name
            reponse+="\n{}|{}|{}|{}|{}|{}|{}|{}".format(display_str_calibrated(nom,33),
                                                  display_str_calibrated(str(e[4]),3),
                                                  display_str_calibrated(str(e[5]),3),
                                                  display_str_calibrated(str(e[6]),3),
                                                  display_str_calibrated(str(e[7]),3),
                                                  display_str_calibrated(str(e[3]),3),
                                                  display_str_calibrated(str(e[8]*100),2)+"%",
                                                  e[0])
        reponse+="""```"""
        return await message.channel.send(reponse)

    
    
    
async def def_leader(DiscordClient,message,args):
    if args==[] or not args[1].isdigit() or int(args[1])>15 or int(args[1]) < 2 :
        return
    liste=DiscordClient.connectionBDD.get_classement_defenses(int(args[1]), limit=10, clan=None)
    if len(liste)==0:
        return await message.channel.send("pas de donnés")
    reponse = "      __**classement des defs des membres hdv {}**__".format(int(args[1]))
    reponse +="``` perf | pas perf | total | % |{}|{}".format(display_str_calibrated("tag",7),display_str_calibrated("pseudo",33))
    for e in liste:
        nom=e[2] if e[2] is not None else "XXpseudoXX"
        if e[1] is not None:
            discordmember=await DiscordClient.fetch_member(int(e[1]))
            nom = discordmember.display_name
        reponse+="\n{}|{}|{}|{}|{}|{}".format(display_str_calibrated(nom,33),#pseudo
                                              display_str_calibrated(str(e[4]),6),#perfdef
                                              display_str_calibrated(str(e[3]-e[4]),9),#pasperfdef
                                              display_str_calibrated(str(e[3]),7),#total
                                              display_str_calibrated(str(e[6]*100),3)+"%",#%
                                              display_str_calibrated(str(e[0]),7),#tag
                                              display_str_calibrated(nom,33)#pseudo
                                             )
    reponse+="""```"""
    await message.channel.send(reponse)
    

    
    
    
    
async def dons_leader(DiscordClient,message,args):
    """ clan: avec le #tag"""
    clan=args[1] if len(args)>1 else None
    
    liste_dons= DiscordClient.connectionBDD.classement_dons( limit=15, clan=clan)#[(idDiscord,tag,pseudo,donné,recu,ratio)]
    nom_clan="du clan:"+clan
    reponse = "      __**classement des donateurs {}**__".format(nom_clan)
    reponse+="\n  don | recu | ratio |   pseudo"
    for e in liste:
        nom=e[2] if e[2] is not None else "XXpseudoXX"
        
        if e[1] is not None:
            try:
                discordmember = await message.guild.fetch_member(int(e[1]))
            except discord.errors.NotFound:
                pass
            else:
                nom = discordmember.display_name
            
        reponse+=f"\n{display_str_calibrated(str(e[3]),6)}|{display_str_calibrated(str(e[4]),6)}|{display_str_calibrated(str(e[5]),6)}:{nom}"
    reponse+="""```"""
    await message.channel.send(reponse)
    
    
