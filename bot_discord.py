import discord
import commandes.dispatch
import database_outils
from config import config
import boucle_infinie_coc
import signal


class discordClient(discord.Client):
    
    def __init__(self,connectionBDD,cocClient):
        intents= discord.Intents().all()
        self.cocClient=cocClient
        self.connectionBDD=connectionBDD
        discord.Client.__init__(self,intents=intents)
        self.loop = self.cocClient.loop
    
    def handler_sigterm(self):
        print("Signal fin execution attrapé!!!!!!","\n"*10)
        self.loop.stop()
    
    
    async def on_ready(self):
        print("\033[92m démarage du bot")
        await boucle_infinie_coc.demarage(config, self.connectionBDD,self.cocClient,self)
        self.cocClient.loop.add_signal_handler(signal.SIGTERM,lambda:self.handler_sigterm())
        
    async def on_message(self,message):
        if message.author.bot or message.channel.guild== None or not message.content.startswith(config["Discord"]["prefix"]):
            return
        
        commande = message.content[1:]
        args = commande.split(' ')
        commande = args[0]
              
        if commande =="ping":
            await message.channel.send("bien connecté")
              
        if commande=="trophés":
            await message.channel.send("{0.name} est a {0.trophies} trophés".format(await self.cocClient.get_player(args[1])))
              
        if commande in ["ajouter","claim","add"]:
              return await commandes.dispatch.claim.claim(self,self.connectionBDD,args,message)
        
        if commande in ["retirer","unclaim"]:
              return await commandes.dispatch.claim.unclaim(self,self.connectionBDD,args,message)
        
        if commande in ["add_clan"]:
              return await commandes.dispatch.claim.add_clan(self,self.cocClient,self.connectionBDD,args,message)
        
        if commande == "scan":
            return await commandes.dispatch.scan.scan(self,self.connectionBDD,message,args)
        
        if commande == "gc":#couleur embed: #F6C471
            """afficher tous les comptes associés a un joueur """
            return await commandes.dispatch.gc.gc(self,message,args)
              
        if commande == "retirer":
            """retirer un tag associé a un joueur"""
            pass
        
        if commande in ["VL","vl"]:# probleme de recuperation de member a partir member.id
            """commandes en SQL"""
            return await commandes.dispatch.VL.VL(self,message,args)
            
        if commande in ["DL" ,"classementdef"]:
            return await commandes.dispatch.VL.def_leader(self,message,args)
        
        if commande== "CD":
            return await commandes.dispatch.VL.dons_leader(self,message,args)
        
        if commande == "SQL" and message.author.id==397116327887896576:
            return await message.channel.send("résultat:\n"+" ".join(map(
                                                                        str,
                                                                        self.connectionBDD.appel_bdd(" ".join(args[1:])
                                                                                                    )
                                                                         )   
                                                                      ) 
                                             )

