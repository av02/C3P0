from sys import prefix
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
        print("\n"*10,"\033[91mSignal fin execution attrapé!!!!!!","\n"*10)
        
        self.cocClient.close()
        self.loop.stop()
        print("\033[92mtout est correctement arrété")
    
    
    async def on_ready(self):
        print("\033[92m démarage du bot")
        await self.get_user(397116327887896576).send("démarage du bot")
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
            return await message.channel.send("résultat:\n"+"\n".join(map(
                                                                        str,
                                                                        self.connectionBDD.appel_bdd("\n".join(args[1:])
                                                                                                    )
                                                                         )   
                                                                      ) 
                                             )
        
        if commande in ["message_add_role"] and message.author.id in config["liste_id_administratifs"]:
            id_message_cible = args[2]
            count=""
            message_cible = await message.channel_mentions[0].fetch_message(id_message_cible)
            role=message.role_mentions[0]
            for r in message_cible.reactions:

                if r == args[3]:

                    async for reacteur in r.users():

                        await reacteur.add_roles(role)
                        count+=(reacteur.nick+", ")
            await message.channel.send(f"role{role}ajouté avec succès à:```{count}")
        
        if commande in ["help"]:
            await message.channel.send(f"""commndes disponible:
                                       ```-{config["Discord"]["prefix"]}ping
                                       \n-{config["Discord"]["prefix"]}trophés #tag
                                       \n-{config["Discord"]["prefix"]}claim #tag @joueur
                                       \n-{config["Discord"]["prefix"]}unclaim #tag //dispo pour admins
                                       \n-{config["Discord"]["prefix"]}add_clan #tag @&role //admins
                                       \n-{config["Discord"]["prefix"]}scan //admin, avec moderation
                                       \n-{config["Discord"]["prefix"]}gc [@joueur]   voir comptes d'un joueur
                                       \n-{config["Discord"]["prefix"]}VL hdv [dips]  voir classement attaques
                                       \n-{config["Discord"]["prefix"]}DL hdv         voir classement defs
                                       \n-{config["Discord"]["prefix"]}CD             voir classement dons
                                      
                                       ```""")





    async def on_reaction(self,reaction,user):
        if reaction.message.author != self or user==self:
            return
        if reaction.message.startswith("      __**Classement des membres hdv") and reaction.emoji in ["⬅️","➡️"]:
            print("réaction top")
            pass