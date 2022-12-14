import discord
import math


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

def affichage_vl(hdv,dips,clan,numero_page,total_page,liste,message):
    reponse = f"""      __**Classement des membres hdv {hdv}{" dips" if dips else ""}{" "+clan if clan is not None else ""}**__\*page{numero_page}/{total_page}"""
    reponse += "\n <:ExpBot:914306062847459328><:vide:914305895331168317> <:vide:914305895331168317><:Hdvbot:914305924259262524><:vide:914305895331168317> <:vide:914305895331168317><:vide:914305895331168317><:Clan1:914327910796632104><:vide:914305895331168317><:vide:914305895331168317><:vide:914305895331168317><:vide:914305895331168317> <:vide:914305895331168317><:TagBot:914306033655095316>```"
    fin=numero_page*20
    if fin>len(liste):
        fin=len(liste)
    i=1
    for e in liste[(numero_page-1)*20:fin]:  
        nom = ""
        if e[1] is not None:
            discordmember = message.guild.get_member(int(e[1]))
            if discordmember is not None:
                nom = discordmember.display_name
            else:
                nom = e[2]
        reponse += f"""\n{(numero_page-1)*20+i} {display_str_calibrated(str(e[8]*100), 2)+"%"+"    "} {display_str_calibrated(str(e[3]), 8)} {display_str_calibrated(str(e[9]), 18)} {display_str_calibrated(nom, 33)}"""
        i+=1
    reponse += """```"""
    return reponse
async def VL(DiscordClient, message, args):
    async with message.channel.typing():
        if len(args) == 1 or not args[1].isdigit() or int(args[1]) > 15 or int(args[1]) < 2:
            return
        dips = False
        if len(args) > 2 and "dips" in args:
            dips = True
        clan = None
        if len(args) > 2+dips:
            clan = args[2+dips]

        liste = DiscordClient.connectionBDD.get_classement_attaques(int(args[1]),
                                                                    dips=dips,
                                                                    clan=clan,
                                                                    nb_etoiles=3)
        if len(liste) == 0:
            return await message.channel.send("Pas de donnés")

        page = 1
        total_page = math.ceil(len(liste)/20)
        reponse=affichage_vl(hdv=int(args[1]),
                            dips=dips,
                            clan=clan,
                            numero_page=1,
                            total_page=total_page,
                            liste=liste,
                            message=message)
        reponse = await message.channel.send(reponse)
        await reponse.add_reaction("⬅️")
        await reponse.add_reaction("➡️")


async def def_leader(DiscordClient, message, args):
    if args == [] or not args[1].isdigit() or int(args[1]) > 15 or int(args[1]) < 2:
        return
    liste = DiscordClient.connectionBDD.get_classement_defenses(
        int(args[1]), limit=10, clan=None)
    if len(liste) == 0:
        return await message.channel.send("pas de donnés")
    reponse = "      __**classement des defs des membres hdv {}**__".format(
        int(args[1]))
    reponse += "``` perf | pas perf | total | % |{}|{}".format(
        display_str_calibrated("tag", 7), display_str_calibrated("pseudo", 33))
    for e in liste:
        nom = e[2] if e[2] is not None else "XXpseudoXX"
        if e[1] is not None:
            discordmember = await DiscordClient.fetch_member(int(e[1]))
            nom = discordmember.display_name
        reponse += "\n{}|{}|{}|{}|{}|{}".format(display_str_calibrated(nom, 33),  # pseudo
                                                display_str_calibrated(
                                                    str(e[4]), 6),  # perfdef
                                                display_str_calibrated(
                                                    str(e[3]-e[4]), 9),  # pasperfdef
                                                display_str_calibrated(
                                                    str(e[3]), 7),  # total
                                                display_str_calibrated(
                                                    str(e[6]*100), 3)+"%",  # %
                                                display_str_calibrated(
                                                    str(e[0]), 7),  # tag
                                                display_str_calibrated(
                                                    nom, 33)  # pseudo
                                                )
    reponse += """```"""
    await message.channel.send(reponse)


async def dons_leader(DiscordClient, message, args):
    """ clan: avec le #tag"""
    clan = args[1] if len(args) > 1 else None

    liste_dons = DiscordClient.connectionBDD.classement_dons(
        limit=15, clan=clan)  # [(idDiscord,tag,pseudo,donné,recu,ratio)]
    nom_clan = "du clan:"+clan if clan is not None else ""
    reponse = "      __**classement des donateurs {}**__```".format(nom_clan)
    reponse += "\n  don | recu | ratio |   pseudo"
    for e in liste_dons:
        nom = e[2] if e[2] is not None else "XXpseudoXX"

        if e[0] is not None:
            try:
                discordmember = await message.guild.fetch_member(int(e[0]))
            except discord.errors.NotFound:
                pass
            else:
                nom = discordmember.display_name

        reponse += f"\n{display_str_calibrated(str(e[3]),6)}|{display_str_calibrated(str(e[4]),6)}|{display_str_calibrated(str(e[5]),6)}:{nom}"
    reponse += """```"""
    await message.channel.send(reponse)
