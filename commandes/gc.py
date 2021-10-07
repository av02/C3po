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
    pseudo=message.mentions[0].display_name
    liste_comptes=DiscordClient.connectionBDD.get_comptes_coc(idDiscord)
    if len(liste_comptes)==0:#cas pas dans bdd
        return await message.channel.send("pas encore de comptes associés")
    rep=discord.Embed(colour=0xf6c471)
    rep.set_author(name="Profil de "+str(pseudo))
    tags = map(lambda tupple_data:tupple_data[0],liste_comptes)
    async for player in DiscordClient.cocClient.get_players(tags):
        rep.add_field(name=player.name,value="<:HdvBot:884202091793506324> Hdv : {} \n<:ExpBot:884202964896608266> Niveau : {} \n<:TagBot:884204003070705754> Tag : {}".format(player.town_hall,player.exp_level,player.tag))
    rep.set_image(url="https://media.discordapp.net/attachments/859386512129654794/884100318936330261/comptes_lie.png")
    rep.set_thumbnail(url=message.mentions[0].avatar_url)
    rep.set_footer(text="Développement av#2616 | Design YohSama | Empire Galactique YohKun#7447",icon_url="https://cdn.discordapp.com/avatars/397116327887896576/93f6ce8dde153200b213ba4ec531dd8f.webp?size=128")
    await message.channel.send(embed=rep)
