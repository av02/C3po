import os
import database_outils#?
import boucle_infinie_coc
import bot_discord
# import donnés
from config import config





def main():
    
    #connection Bdd, non bloquant
    connectionBDD=database_outils.appelsBDD(config["bddlink"])

    #lancement des evenements coc
    cocClient=boucle_infinie_coc.boucle_infinie_coc(config,connectionBDD)
    
    bot_discord.discordClient(connectionBDD,cocClient).run(config["Discord"]["token"])#commande blocante pour lancer le bot

    


if __name__=="__main__":
    main()
    