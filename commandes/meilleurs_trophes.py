from email import message
import discord
def display_str_calibrated(chaine: str, longueur: int) -> str:
    """renvoie une chaine str calibrée

    Args:
        chaine ([str]): [chaine a travailler]
        longueur ([type]): [longeur de la chaine a renvoyer]

    Returns:
        [str]: [chaine, avec une longeur de longeur]
        chaine vide si trop long
    """
    if len(chaine) == longueur:
        return chaine
    if len(chaine) < longueur:
        return chaine+(" "*(longueur-len(chaine)))
    return chaine[:longueur]

async def maj_meilleurs_trophés(liste_joueurs:list,client_discord:discord.Client):
    salon = client_discord.get_channel(1021466591961038868)
    liste_joueurs.sort(key=lambda x:x.trophies,reverse=True)
    
    
    
    message="```Sélection Gdc 50 _______"
    for i,j in enumerate(liste_joueurs[0:50]):
        
        
        message+=f"\n{display_str_calibrated(str(i+1),2)}| {j.trophies}🏆|{display_str_calibrated(j.name,20)}\n             {j.clan.name}"
    message+="\n___Fin des sélections"
    for i,j in enumerate(liste_joueurs[50:70]):
        message+=f"\n{display_str_calibrated(str(i+51),2)}| {j.trophies}🏆|{display_str_calibrated(j.name,20)}\n             {j.clan.name}"
    message+="```"
    embed = discord.Embed(colour=0xf6c471,description=message)
    embed.set_author(name=f"Liste des plus hauts trophés de l'empire :")
    embed.set_footer(text="Développement av#2616 | Design YohKun#7447 | Empire Galactique",icon_url="https://cdn.discordapp.com/avatars/397116327887896576/93f6ce8dde153200b213ba4ec531dd8f.webp?size=128")
    await salon.send(embed=embed)
    