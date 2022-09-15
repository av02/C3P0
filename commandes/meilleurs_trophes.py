import discord


async def maj_meilleurs_trophés(liste_joueurs:list,client_discord:discord.Client):
    salon = client_discord.get_channel(859386512129654794)
    liste_joueurs.sort(key=lambda x:x.trophies)
    message=f"liste des plus hauts trophés de l'empire:\n"
    for j in liste_joueurs[0:50]:
        message+=f"\n{j.trophies}:      {j.name}"
    message+="50"+"-"*10
    for j in liste_joueurs[50:80]:
        message+=f"\n{j.trophies}:      {j.name}"
    await salon.send(message)