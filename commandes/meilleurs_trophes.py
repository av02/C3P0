from email import message
import discord


async def maj_meilleurs_trophés(liste_joueurs:list,client_discord:discord.Client):
    salon = client_discord.get_channel(1021466591961038868)
    liste_joueurs.sort(key=lambda x:x.trophies,reverse=True)
    
    
    message=""
    for i,j in enumerate(liste_joueurs[0:50]):
        
        
        message+=f"\n{i+1}|{j.trophies}|  {j.name}|  {j.clan.name}"
    message+="\n50"+"-"*10
    for i,j in enumerate(liste_joueurs[50:70]):
        message+=f"\n{i+51}|{j.trophies}|  {j.name}|  {j.clan.name}"
    embed = discord.Embed(colour=0xf6c471,description=message)
    embed.set_author(name=f"liste des plus hauts trophés de l'empire:")
    embed.set_footer(text="Développement av#2616 | Design YohKun#7447 | Empire Galactique",icon_url="https://cdn.discordapp.com/avatars/397116327887896576/93f6ce8dde153200b213ba4ec531dd8f.webp?size=128")
    await salon.send(embed=embed)
    