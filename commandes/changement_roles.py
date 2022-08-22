from config import config
import discord
async def maj_role(client_discord,discord_id,liste_hdv,*tags_clans_rejoints):
    """ajouter les roles de clan

    Args:
        discordClient ([discordClient]): [le client discord]
        discord_id ([int]): [l'identifiant du joueur]
        clan_rejoint ([list]):[liste des tags des differents clans de l'empire du joueur]
    """    
    
    serveur_empire = client_discord.get_guild(config["id_serveur_discord"])
    
    if serveur_empire is None:
        return print("erreur dans maj_role, serveur introuvable")
    compte_membre_discord = serveur_empire.get_member(discord_id)
    
    if compte_membre_discord is None:
        return 
    liste_roles_initiale = compte_membre_discord.roles
    LISTE_ID_ROLES_CLANS = [r.id_role_associe for r in config["liste_clan_empire"]]     
              
    liste_roles_clans_rejoints = [clan.id_role_associe for clan in config["liste_clan_empire"] if clan.tag in tags_clans_rejoints]
    liste_roles_clans_iniale = list(set(
                                     map(lambda role:role.id,liste_roles_initiale)
                                        )&set(LISTE_ID_ROLES_CLANS))
    
    
    liste_roles_clans_en_trop=list(set(liste_roles_clans_iniale)-set(liste_roles_clans_rejoints))
    liste_roles_clans_a_ajouter=list(set(liste_roles_clans_rejoints)-set(liste_roles_clans_iniale))
    
    role_jedi=serveur_empire.get_role(729577094866141185)
    role_storm=serveur_empire.get_role(729581221616812084)
    
    
    if liste_roles_clans_en_trop!=[]:
        roles = [role for role in serveur_empire.roles if role.id in liste_roles_clans_en_trop]
        try:
            await compte_membre_discord.remove_roles(*roles,reason="bot: clan quitté")
        except discord.Forbidden:
            print("\033[91m Permissions manquantes pour supprimer des roles a:",compte_membre_discord.id)
        except discord.HTTPException:
            print("probleme résau avec la supression de roles a:",compte_membre_discord.id)
    if liste_roles_clans_a_ajouter!=[]:
        roles = [role for role in serveur_empire.roles if role.id in liste_roles_clans_a_ajouter]
        try:
            await compte_membre_discord.add_roles(*roles,reason="bot: clan rejoint")
        except discord.Forbidden:
            print("\033[91m Permissions manquantes pour ajouter des roles a:",compte_membre_discord.id)
        except discord.HTTPException:
            print("probleme résau avec la ajouter de roles a:",compte_membre_discord.id)
    
    
    if liste_roles_clans_rejoints==[]:#Cas stormtrooper
        try:
            await compte_membre_discord.add_roles(role_storm,reason="bot: pas de clans")
            await compte_membre_discord.remove_roles(*[role for role in serveur_empire.roles if role.id in config["roles_hdv"].values()])
            await compte_membre_discord.remove_roles(role_jedi)
        except discord.Forbidden:
            print("\033[91m Permissions manquantes pour ajouter des roles a:",compte_membre_discord.id)
        except discord.HTTPException:
            print("probleme résau avec la ajouter de roles a:",compte_membre_discord.id)
    else:
        roles_hdv=[config["roles_hdv"][str(e)]for e in set(liste_hdv) if e>=10]
        try:
            await compte_membre_discord.remove_roles(role_storm,reason="bot: clan rejoint")
            await compte_membre_discord.add_roles(*[role for role in serveur_empire.roles if role.id in roles_hdv ])
            await compte_membre_discord.add_roles(role_jedi)
        except discord.Forbidden:
            print("\033[91m Permissions manquantes pour ajouter des roles a:",compte_membre_discord.id)
        except discord.HTTPException:
            print("probleme résau avec la ajouter de roles a:",compte_membre_discord.id)

    
