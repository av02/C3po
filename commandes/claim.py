import coc
import discord
from config import *

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
        connectionBDD.add_discord_id(tag,idDiscord,821743088296919041 in list(map(lambda r: r.id , message.author.roles)))#TODO: ajouter une verification de roles
    except PermissionError:
        return await message.channel.send("déjà enregistré par le passé, vous n'avez pas les permissions d'éditer ce lien.")
    except ValueError:
        try:
            player=await client_discord.cocClient.get_player(tag)
        except coc.NotFound:
            return await message.channel.send("tag ne correspondant a aucun joueur")
          
        except coc.Maintenance:
            return await message.channel.send("maintenance")
        
        th = player.town_hall
        pseudo= player.name
        clan = player.clan.name if player.clan is not None else None
        connectionBDD.check_presence_database(tag, th, pseudo, clan)
        connectionBDD.add_discord_id(tag,idDiscord,False)#TODO: ajouter une verification de roles
    return await message.channel.send("operation réussie")


async def unclaim(client_discord,


                        connectionBDD,
                        args,
                        message):
    """[permet de délier un joueur de la bdd]

    Args:
        client_discord ([discord.Client]): [un client pour l'API discord]
        connectionBDD ([database_outils.appelsBDD]): [un connecteur a la BDD]
        args ([list]): [les arguments de la commande]
        message ([discord.message]): [le message génerateur]
    Returns:
        [None]: [rien]
    """
    if len(args) != 2 and len(message.mentions) != 0:
        return await message.channel.send("nombre d'arguments incorect")
    tag=coc.utils.correct_tag(args[1])
    
    #on verifie qu'on a 2 arguments, la commande, le tag 
    
    if message.author.id in config["liste_sous_admins"]:
      try:
        connectionBDD.add_discord_id(tag,None,True)
      except ValueError:
        return await message.channel.send("ce joueur n'existe pas a mes yeux")
      else:
        return await message.channel.send("operation réussie")
      return await message.channel.send("vous n'avez pas les permissions")

    
    
  
async def add_clan(client_discord,

                        ClientCOC,
                        connectionBDD,
                        args,
                        message):
  if len(args) != 3 and len(message.raw_role_mentions) != 1:
    return await message.channel.send("nombre d'arguments incorect")
  tag=coc.utils.correct_tag(args[1])
  try: 
    clan = await ClientCOC.get_clan(tag)
  except NotFound:
    return await message.channel.send("On me dit dans l'oreillette que ce clan n'existe pas ")
  except Maintenance:
    return await message.channel.send("Il y a actuellement une maintenance de l'api")
  except GatewayError:
    return await message.channel.send("erreur de gateway")
  #on verifie qu'on a 2 arguments, la commande, le tag 
  if discord.utils.find(lambda role:role.id==message.raw_role_mentions[0],message.guild.roles) is None:
    return await message.channel.send("merci d'indiquer un role valide")
  if message.author.id in config["liste_id_administratifs"]:
    try:
      connectionBDD.add_clan(args[1],clan.name,str(message.raw_role_mentions[0]))
    except ValueError:
      return await message.channel.send("vous n'avez pas les permissions")
    else:
      return await message.channel.send("operation réussie")
      





