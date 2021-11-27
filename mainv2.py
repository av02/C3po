import os
import database_outils#?
import boucle_infinie_coc
import bot_discord
# import donnés
from config import config
import coc

def main():
    cocClient= coc.login(email=config["Coc"]["mail"],
                        password=config["Coc"]["password"],
                        client=coc.EventsClient)
    
    #connection Bdd, non bloquant
    connectionBDD=database_outils.appelsBDD(config["bddlink"])
    connectionBDD.set_cocClient(cocClient)
    #définition du bot
    discordClient=bot_discord.discordClient(connectionBDD,cocClient)
    
    
    #lancement des evenements coc
    
    boucle_infinie_coc.boucle_infinie_coc(config,connectionBDD,discordClient,cocClient)
    #connectionBDD.appel_bdd("DELETE FROM new WHERE tagig='#2UGJVQGQU'")#SUPPRIMER UN COMPTE, NE PAS METTRE SANS TAG
    
    discordClient.run(config["Discord"]["token"])#commande blocante pour lancer le bot

    


if __name__=="__main__":
    main()
    
