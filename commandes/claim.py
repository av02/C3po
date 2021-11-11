import coc


async def claim(client_discord,
                connectionBDD,
                args,
                message):
    """claim:


    Args:
        client_discord ([discord.Client]): [un client pour l'API discord]
        connectionBDD ([database_outils.appelsBDD]): [un connecteur a la BDD]
        args ([list]): [les arguments de la commande]
        message ([discord.message]): [le message génerateur]

    Returns:
        [type]: [descriptio n]
    """
    if len(args) != 3 and len(message.mentions) != 1:
        return await message.channel.send("nombre d'arguments incorect")
    tag=coc.utils.correct_tag(args[1])
    idDiscord=message.mentions[0].id
    #on verifie qu'on a 3 arguments, la commande, le tag et qu'il y a bien une mention
    
    
    try:
        connectionBDD.add_discord_id(tag,idDiscord,False)#TODO: ajouter une verification de roles
    except PermissionError:
        return await message.channel.send("déjà enregistré par le passé, vous n'avez pas les permissions d'éditer ce lien.")
    except ValueError:
        try:
            player=await client_discord.cocClient.get_player(tag)
        except NotFound:
            return await message.channel.send("tag ne correspondant a aucun joueur")
        except Maintenance:
            return await message.channel.send("maintenance")
        
        th = player.town_hall
        pseudo= player.name
        clan = player.clan.name if player.clan is not None else None
        connectionBDD.check_presence_database(self, tag, th, pseudo, clan)
        connectionBDD.add_discord_id(tag,idDiscord,False)#TODO: ajouter une verification de roles
    return await message.channel.send("operation réussie")
