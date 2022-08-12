import os
import database_outils#?
import boucle_infinie_coc
import bot_discord
# import donnés
from config import config
import coc
import signal


def main():
    def handler_sigterm(arg1,arg2):
        print("FIN EXECUTION RECUE")
    
    signal.signal(signal.SIGINT,handler_sigterm)

    
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
    
    
    discordClient.run(config["Discord"]["token"])#commande blocante pour lancer le bot

    


if __name__=="__main__":
    main()
    

