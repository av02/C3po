import os
import database_outils#?
import boucle_infinie_coc
import bot_discord
# import donnés
from config import config
import coc
import signal

def handler_sigterm(arg1,arg2):
    print("FIN EXECUTION RECUE")
    
print("l13 main")
signal.signal(signal.SIGINT,handler_sigterm)
print("l15 main")
def main():
    
    cocClient= coc.login(email=config["Coc"]["mail"],
                        password=config["Coc"]["password"],
                        client=coc.EventsClient,
                        key_count =10,
                        throttle_limit=30)
    cocClient.loop.add_signal_handler(signal.SIGTERM,handler_sigterm)
    #connection Bdd, non bloquant
    connectionBDD=database_outils.appelsBDD(config["bddlink"],config["liste_clans"])
    connectionBDD.set_cocClient(cocClient)
    
    config["liste_clan_empire"]=connectionBDD.get_all_clans()
    #définition du bot
    discordClient=bot_discord.discordClient(connectionBDD,cocClient)
    
    
    #lancement des evenements coc
    
    boucle_infinie_coc.boucle_infinie_coc(config,connectionBDD,discordClient,cocClient)
    #connectionBDD.appel_bdd("DELETE FROM new WHERE tagig='#2UGJVQGQU'")#SUPPRIMER UN COMPTE, NE PAS METTRE SANS TAG
    
    discordClient.run(config["Discord"]["token"])#commande blocante pour lancer le bot

    


if __name__=="__main__":
    main()
    

    
