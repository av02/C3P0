import coc
import coc.errors
import database_outils
import commandes.dispatch
import asyncio



async def demarage(config,connection_bdd,cocClient,discordClient):
    liste_joueurs=[]
    tagsJoueurs=connection_bdd.get_all_tag()
    print("démarage")
    
    for tag in tagsJoueurs:
        try:
            player = await cocClient.get_player(tag)
        except coc.errors.NotFound:
            await discordClient.get_user(397116327887896576).send(f"ce tag fous la merde:{tag}")
        
            
            
            
            
            connection_bdd.maj_info(tag=player.tag,
                                clan=player.clan.tag if player.clan is not None else None,
                                pseudo=player.name,
                                town_hall=player.town_hall)
            if player.clan is not None and player.clan.tag in [x.tag for x in config["liste_clan_empire"]]:
                    liste_joueurs.append(player)
                    
    await commandes.dispatch.meilleurs_trophes.maj_meilleurs_trophés(liste_joueurs,discordClient)
            
            
            
    print("parcourt mb discord")        
    for member in discordClient.get_guild(config["id_serveur_discord"]).members:
        id_membre_discord=member.id
        if member.bot or 830742603187617842 in map(lambda r:r.id,member.roles) or 999717064946241556 in map(lambda r:r.id,member.roles) or 998664888153018428 in map(lambda r:r.id,member.roles):#bot  ou padawan ou storm ou clone
            continue
        tags_comptes_coc = [e[0] for e in connection_bdd.get_comptes_coc(id_membre_discord)]
        if len(tags_comptes_coc)==0 :#sans comptes ajoutés 
            await discordClient.get_channel(863026482576883742).send(f"cet utilisateur n'a pas de compte compte coc:<@{member.id}>")
            continue
            
        
        
        liste_clans_rejoint=[]
        liste_hdv=[] 
        async for player in cocClient.get_players(tags_comptes_coc):
            if player.clan is not None:
                liste_clans_rejoint.append(player.clan.tag)
                liste_hdv.append(player.town_hall)
        await commandes.dispatch.changement_roles.maj_role(discordClient,id_membre_discord,liste_hdv,*liste_clans_rejoint)
            
            
            
 #   async for player in cocClient.get_players(tagsJoueurs):
        
 #       connection_bdd.maj_info(tag=player.tag,
 #                               clan=player.clan.tag if player.clan is not None else None,
 #                               pseudo=player.name,
 #                               town_hall=player.town_hall)

def boucle_infinie_coc(config,connection_bdd,discordClient,cocClient):
    clan_tags = [e.tag for e in config["liste_clan_empire"]]
    tagsJoueurs = connection_bdd.get_all_tag()
    # connection client coc, non bloquant
    
    
    
    
    
    # quand une attaque de guerre survient
    @cocClient.event
    @coc.WarEvents.war_attack(tags=clan_tags)
    async def current_war_stats(attack, war):
        if attack.attacker.clan.tag in clan_tags and attack.attacker.town_hall>=attack.defender.town_hall:# on controle qu'il est dans un de nos clans
            if attack.attacker.town_hall != attack.defender.town_hall and  attack.attacker.town_hall != attack.defender.town_hall+1: # ce n'est un un x vs x , ni un x vs x-1
                return   
            connection_bdd.add_score_gdc(attack.attacker_tag,
                                        attack.stars,
                                        attack.attacker.town_hall,
                                        attack.attacker.name,
                                        attack.attacker.clan.tag,
                                        attack.attacker.town_hall != attack.defender.town_hall)
            return
        else:
            if attack.attacker.town_hall != attack.defender.town_hall:
                return
            connection_bdd.add_def_gdc(
                                        attack.defender_tag,
                                        attack.stars==3,
                                        attack.defender.town_hall,
                                        attack.defender.name,
                                        attack.defender.clan.tag
                                       )




    @cocClient.event  
    @coc.ClanEvents.member_donations(tags=clan_tags)
    async def on_clan_member_donation(old,new):#TODO controller les odns négatifs
        if new.donations<old.donations:# si donné negatifs, alors c'est que debut saison ou quitté le clan
            return
        profil=await cocClient.get_player(old.tag)# on recupere le profil
        connection_bdd.add_don(old.tag,new.donations-old.donations,profil.town_hall,profil.name,old.clan.tag)
    

    @cocClient.event#mise a jour de la bdd quand un membre reçoit
    @coc.ClanEvents.member_received(tags=clan_tags)
    async def on_clan_member_received(old,new):
        if new.received<old.received:# si le joueur a des reçus negatifs, soit quitté le clan, soit debut de saison
            return
        profil = await cocClient.get_player(old.tag)# on recupere le profil 
        connection_bdd.add_recu(old.tag,new.received-old.received,profil.town_hall,profil.name,old.clan.tag)
        


    @cocClient.event#mise a jour de la bdd quand un membre change de pseudo
    @coc.PlayerEvents.name(tags= tagsJoueurs)
    async def on_name_change(old,new):
        connection_bdd.edit_pseudo(old.tag,new.name)
    @cocClient.event# mise a jour de la bdd quand un membre change d'hdv
    @coc.PlayerEvents.town_hall(tags= tagsJoueurs)
    async def on_th_change(old,new):
        
        connection_bdd.up_hdv(old.tag,new.town_hall)
    
    
    
    @cocClient.event  
    @coc.PlayerEvents.clan(tags=tagsJoueurs)
    async def on_clan_status_change(old,new):
        new_clan_tag = new.clan.tag if new.clan is not None else None
        connection_bdd.edit_clan(old.tag,new_clan_tag)
        compte_discord_id=connection_bdd.get_discord_id(old.tag)
        if compte_discord_id is not None:
            member = discordClient.get_guild(config["id_serveur_discord"]).get_member(compte_discord_id)
            if member is None or member.bot or 830742603187617842 in map(lambda r:r.id,member.roles):#bot  ou padawan
                return
            await asyncio.sleep(3600)
            tags_comptes_coc = [e[0] for e in connection_bdd.get_comptes_coc(compte_discord_id)]
            liste_clans_rejoint=[]
            liste_hdv=[] 
            async for player in cocClient.get_players(tags_comptes_coc):
                if player.clan is not None:
                    liste_clans_rejoint.append(player.clan.tag)
                    liste_hdv.append(player.town_hall)
            await commandes.dispatch.changement_roles.maj_role(discordClient,compte_discord_id,liste_hdv,*liste_clans_rejoint)