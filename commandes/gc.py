
import discord


async def gc(DiscordClient, message,args):#TODO: ajouter le cas de l'autotag, pas besoin de s'autotag
    """commande du bot pour voir l'ensembles des comptes coc associés a un utilisateur discord
    Args:
        DiscordClient ([discord.discord.Client]): [un cient discord]
        message ([discord.message]): [le message invocateur]
        args ([list]): [la liste des arguments]
    Returns:
        [None]: [ne retourne rien]
    """    
    if len(message.mentions)!=1:# cas nb de tags incoherents 
        return await message.channel.send("merci de tag __une__ personne")
    idDiscord=message.mentions[0].id
    pseudo = message.mentions[0].display_name
    liste_comptes =DiscordClient.connectionBDD.get_comptes_coc(idDiscord)
    
    if len(liste_comptes)==0:#cas pas dans bdd
        return await message.channel.send("pas encore de comptes associés")
    
    rep=discord.Embed(colour=0xf6c471)
    rep.set_author(name="Profil de "+str(pseudo))

    tags = map(lambda tupple_data:tupple_data[0],liste_comptes)

    liste_profils=[]
    async for player in DiscordClient.cocClient.get_players(tags):
        liste_profils.append(player)
    liste_profilszip =  list(zip(liste_profils,liste_comptes))
    liste_profilszip.sort(reverse = True,key = lambda p:p[0].town_hall*1000+p[0].exp_level)   
    for player in liste_profilszip:   
        ratio_str = f"\n💯 Ratio Perf : {str(int((player[1][7]*100)//player[1][6]))}%"if player[1][6]!=0 else ""
        rep.add_field(name=player[0].name,value="<:TagBot:884204003070705754> Tag : {}\n<:HdvBot:884202091793506324> Hdv : {} \n<:ExpBot:884202964896608266>\n🏆 trophés : {} Niveau : {} \n🛡️ Clan : {}{}".format(player[0].tag,player[0].town_hall,player[0].exp_level,int(player[0].trophies),player[0].clan.name if player[0].clan is not None else "Pas de clan",ratio_str))#,ligne_BDD[7]/(ligne_BDD[6]+0.000000000001)*100))
    rep.set_image(url="https://media.discordapp.net/attachments/859386512129654794/884100318936330261/comptes_lie.png")
    rep.set_thumbnail(url=message.mentions[0].avatar_url)
    rep.set_footer(text="Développement av#2616 | Design YohKun#7447 | Empire Galactique",icon_url="https://cdn.discordapp.com/avatars/397116327887896576/93f6ce8dde153200b213ba4ec531dd8f.webp?size=128")
    await message.channel.send(embed=rep)
