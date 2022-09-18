import discord


async def maj_meilleurs_trophés(liste_joueurs:list,client_discord:discord.Client):
    salon = client_discord.get_channel(859386512129654794)
    liste_joueurs.sort(key=lambda x:x.trophies,reverse=True)
    message=f"liste des plus hauts trophés de l'empire:\n\n"
    
    print(liste_joueurs)
    for i,j in enumerate(liste_joueurs[0:50]):
        
        
        message+=f"\n{i+1}:{j.trophies} tr:   {j.name}"
    message+="\n50"+"-"*10
    for i,j in enumerate(liste_joueurs[50:80]):
        message+=f"\n{i+51}:{j.trophies} tr:   {j.name}"
    await salon.send(message)
    