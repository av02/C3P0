import psycopg2
#import sqlite3 as psycopg2  #dans le cas de tests locaux.

def attrapeur_d_exception(fonction_requete):
    """un décorateur pour faire genre je maitrise alors que j'y comprend pas beaucoup plus que vous, et que j'ai la flemme d'ajouter des try partout"""
    def fonction_avec_exceptions(*args,**kwargs):
        try:
            return fonction_requete(*args,**kwargs)
        except Exception as e:
            print("""une exception est survenue:""",e,"""avec la fonction:""",fonction_requete.__name__,sep="\n")

    return fonction_avec_exceptions

def echap_appostrophe(texte):
    return texte.replace("'","''")

class Clan_empire:
    def __init__(self,tag,nom,id_role_associe):
        self.tag = tag
        self.nom = nom
        self.id_role_associe = int(id_role_associe)
    def __repr__(self):
        return self.tag

    
class Joueur_empire:
    def __init__(self,**kwargs):
                self.tagIG=kwargs.get("tagig",None)
                self.discordID=kwargs.get("discordID",None)
                self.pseudoIG=kwargs.get("pseudoIG",None)
                self.thIG=kwargs.get("thIG",None)
                self.donne=kwargs.get("donne",None)
                self.recu =kwargs.get("recu",None)
                self.nbattaques=kwargs.get("nbattaques",None)
                self.perf=kwargs.get("perf",None)
                self.bi=kwargs.get("bi",None)
                self.one=kwargs.get("one",None)
                self.black=kwargs.get("black",None)
                self.nbdips=kwargs.get("nbdips",None)
                self.perfdips=kwargs.get("perfdips",None)
                self.bidips=kwargs.get("bidips",None)
                self.onedips=kwargs.get("onedips",None)
                self.blackdips=kwargs.get("blackdips",None)
                self.perfdefs=kwargs.get("perfdefs",None)
                self.nbdefs=kwargs.get("nbdefs",None)
                self.clantag=kwargs.get("clantag",None)

class Clan_empire:
    def __init__(self,tag,nom,id_role_associe):
        self.tag = tag
        self.nom = nom
        self.id_role_associe = int(id_role_associe)

class appelsBDD:
    def __init__(self, bddlink,liste_tag_clans):
        self.bddlink = bddlink
        self.liste_tag_clans=liste_tag_clans
    
    def set_cocClient(self,cocClient):#utilité?????
        self.cocClient = cocClient
    
    def appel_bdd(self, instruction:str,data=None, commit=True) -> list:
        """instructions SQL
        execute les instructions passées en arguments sur la Bdd
        """
        con = psycopg2.connect(self.bddlink,sslmode='require')
        Curseur = con.cursor()

        try:
            Curseur.execute(instruction,data)
        except Exception as e:
            print("\033[93merreur d'éxecution!!!!:" ,e,end="\n")
            print("instruction:",instruction,data)
            return []
        retour = []
        try:
            for l in Curseur:
                retour.append(l)
        except psycopg2.ProgrammingError:
            pass
        except Exception as e:
            print("\033[93merreur de lecture!!!!:" ,e)
            print("resultat:",Curseur)
        if commit:
            con.commit()
        con.close()
        return retour


    def check_presence_database(self, tag, th, pseudo, clan):
        """ verifie si le tag passé en argument est dans la base de donnée 
        sinon , l'ajoute avec l'hdv et le pseudo 
        """
        data={"tagIG":tag,
        "thIG":th,"pseudoIG":pseudo,
        "clantag":clan}
        if len(self.appel_bdd("SELECT * FROM empire WHERE tagIG = %(tagIG)s",data=data)) == 0:
            self.appel_bdd("""INSERT INTO empire (tagIG,pseudoIG,thIG,clantag,
                                donne,recu,
                                nbattaquesmemehdv,nbperfmemehdv,nbbimemehdv,nbonememehdv,nbblackmemehdv,
                                nbattaquesdips,nbperfdips,nbbidips,nbonedips,nbblackdips,
                                nbattaqueshdvanterieur,nbperfhdvanterieur,nbbihdvanterieur,nbonehdvanterieur,nbblackhdvanterieur,
                                nbperfdefmemehdv,nbdefmemehdv) 
                           VALUES (%(tagIG)s,%(pseudoIG)s,%(thIG)s,%(clantag)s,    0,0, 0,0,0,0,0, 0,0,0,0,0, NULL,NULL,NULL,NULL,NULL,  0,0)""",
                           data=data
                           )
        return

#TODO:retirer les format
    def add_discord_id(self, tag, id, permission_ecraser=False):
        """ajoute l'identifiant discord associé a un compte
        ecrase le tag précédent si permission_ecraser==True
        """
        if len(self.appel_bdd("SELECT discordID FROM empire WHERE tagIG=%(tagIG)s",data={"tagIG":tag}))!=1:
            raise ValueError()
        if not permission_ecraser and self.appel_bdd("SELECT discordID FROM empire WHERE tagIG=%(tagIG)s",data={"tagIG":tag})[0] != (None,):
            raise PermissionError()
        if id is None:
            id=None
        else:
            id=str(id)
        self.appel_bdd("UPDATE empire SET discordID=%(discordID)s WHERE tagIG=%(tagIG)s",data={"discordID":id,"tagIG":tag})
        return 

    def get_discord_id(self, tag) -> int:  # TODO controler si non enregistré
        """renvoie l'identifiant discord , None si non enregistré
        """
        try:
            return int(self.appel_bdd("SELECT discordID FROM empire WHERE tagIG=%(tagIG)s",data={"tagIG":tag})[0][0])
        except TypeError:
            return None

    def edit_pseudo(self, tag, pseudo):
        """modifie le pseudo du joueur, ecrase le précdent
        """
        self.appel_bdd(
            "UPDATE empire SET pseudoIG=%(pseudoIG)s WHERE tagIG=%(tagIG)s",data={"pseudoIG":pseudo,"tagIG":tag})

    def edit_clan(self, tag, clan=None):
        """met a jour le clan du joueur avec son nouveau clan"""
        self.appel_bdd(
            """UPDATE empire SET clantag=%(clantag)s WHERE tagIG=%(tagIG)s""",data={"clantag":clan,"tagIG": tag})

    def up_hdv(self, tag, th):# a deplacer vers hdv ante, hdv-1 == dips
        """a appeler dans le cas d'un changement d'hdv
        modifie l'hdv du joueur, deplace les attaques vers hdv -1 
        reset les def/hdv idem
        ecrase le précdent
        """
        stats = self.appel_bdd(
            "SELECT thIG,nbattaquesmemehdv,nbperfmemehdv,nbbimemehdv,nbonememehdv,nbblackmemehdv FROM empire WHERE tagIG=%(tagIG)s",data={"tagIG":tag})[0]
        if stats[0] != th:
            self.appel_bdd(
                "UPDATE empire SET thIG=%(thIG)s,nbattaqueshdvanterieur=%(nbattaqueshdvanterieur)s,nbperfhdvanterieur=%(nbperfhdvanterieur)s,nbbihdvanterieur=%(nbbihdvanterieur)s,nbonehdvanterieur=%(nbonehdvanterieur)s,nbblackhdvanterieur=%(nbblackhdvanterieur)s, nbattaquesdips=0,nbperfdips=0,nbbidips=0,nbonedips=0,nbblackdips=0, nbattaquesmemehdv=0,nbperfmemehdv=0,nbbimemehdv=0,nbonememehdv=0,nbblackmemehdv=0,nbperfdefmemehdv=0,nbdefmemehdv=0 WHERE tagIG=%(tagIG)s",
                data={"thIG":th,"nbattaqueshdvanterieur": stats[1],"nbperfhdvanterieur": stats[2],"nbbihdvanterieur": stats[3],"nbonehdvanterieur": stats[4],"nbblackhdvanterieur": stats[5],"tagIG": tag}
                )

    def add_score_gdc(self, tag, etoiles,th,pseudo,clan, dips=False):
        """
        ajoute au joueur avec le tag le nombre d'étoiles,
        etoiles est le nombre d'étoiles de l'attaque (∈ ⟦0;3⟧)
        dips doit etre passé true si l'hdv ennemi est inferieur de 1
        ne pas appeler si Δhdv>1
        """
        self.check_presence_database(tag,th,pseudo,clan)
        fin_dips = "dips" if dips else "memehdv"  # si c'est un dips, on change la catégorie dans la bdd
        def _transcription_etoiles_strbdd(nbetoiles):
            return ["nbblack", "nbone", "nbbi", "nbperf"][nbetoiles]
        valeurs_anterieures = self.appel_bdd("""SELECT nbattaques{},{} 
                                            FROM empire WHERE tagIG=%(tagIG)s""".format(fin_dips,
                                                                                   _transcription_etoiles_strbdd(
                                                                                                                etoiles) +fin_dips,
                                                                                                            ),data={
                                                                                                                "tagIG":tag
                                                                                                            })[0]
        if valeurs_anterieures[0] is None:
            
            valeurs_anterieures=(0,valeurs_anterieures[1])
        if valeurs_anterieures[1] is None:
            valeurs_anterieures=(valeurs_anterieures[0],0)
        self.appel_bdd("""UPDATE empire SET "nbattaques{}"=%(nbatt)s, "{}"={} 
                        WHERE tagIG=%(tagIG)s""".format( fin_dips,
                                                    _transcription_etoiles_strbdd(
                                                                             etoiles)+fin_dips,
                                                    valeurs_anterieures[1]+1,
                                                    ),
                                                    data={"nbatt":valeurs_anterieures[0]+1,
                                                    "tagIG":tag})
        
        
    def add_def_gdc(self, tag, perf: bool,th,pseudo,clan):
        """N'APPELER QUE SI LES HDV SONT ÉGAUX
        ajoutes 1 au nombre total de defs enregistrées, 
        et la valeur numerique associé au booléen perf
        dans la colone nbperfdef
        """
        self.check_presence_database(tag,th,pseudo,clan)
        valeurs_anterieures = self.appel_bdd(
            """SELECT nbdefmemehdv,nbperfdefmemehdv FROM empire WHERE tagIG='{}'""".format(tag)
                                            )[0]
        if valeurs_anterieures[0] is None:
            
            valeurs_anterieures=(0,valeurs_anterieures[1])
        if valeurs_anterieures[1] is None:
            valeurs_anterieures=(valeurs_anterieures[0],0)
           
        self.appel_bdd("""UPDATE empire SET nbdefmemehdv={},nbperfdefmemehdv={} WHERE tagIG='{}'""".format(
            valeurs_anterieures[0]+1, valeurs_anterieures[1]+int(perf), tag))

    def add_don(self, tag, dons,th,pseudo,clan):
        """ajoute dons au dons associés au tag
        """
        
        self.check_presence_database(tag,th,echap_appostrophe(pseudo),clan)
        
        valeur_anterieur = self.appel_bdd("""SELECT donne FROM empire 
                                        WHERE tagIG='{}'""".format(tag))[0][0]
        
        self.appel_bdd("""UPDATE empire SET donne={} WHERE tagIG='{}'""".format(
            int(valeur_anterieur)+dons, tag))
        #dons de décembre
        #valeur_anterieur_mois = self.appel_bdd("""SELECT donmois FROM new 
        #                                WHERE tagIG='{}'""".format(tag))[0][0]
        #if valeur_anterieur_mois is None:
         #   valeur_anterieur_mois = 0
        #self.appel_bdd("""UPDATE new SET donmois={} WHERE tagIG='{}'""".format(
        #    int(valeur_anterieur_mois)+dons, tag))
        

    def add_recu(self, tag, recu,th,pseudo,clan):
        """ajoute recu au recu associés au tag
        """
        self.check_presence_database(tag,th,pseudo,clan)
        valeur_anterieur = self.appel_bdd("""SELECT recu FROM empire 
                                        WHERE tagIG='{}'""".format(tag))[0][0]
        self.appel_bdd("""UPDATE empire SET recu={} WHERE tagIG='{}'""".format(
            int(valeur_anterieur)+recu, tag))

    def classement_dons(self, limit, *, clan=None) -> list:
        """renvoie une liste de tupples (idDiscord,tag,pseudo,donné,recu,ratio)"""
        requete_clan = " AND clantag='"+clan+"'" if clan is not None else ""
        return self.appel_bdd("""SELECT  discordid ,MIN(tagig) AS TAGIG,MAX(pseudoig) AS pseudo,SUM(donne) AS DON ,SUM(recu) AS recu,(SUM(donne)+0.00000000000001)/(SUM(recu)+0.00000000000001) AS ratio FROM empire WHERE  discordid IS NOT NULL AND clantag NOT LIKE('éxterieur') {} GROUP BY discordid ORDER BY DON DESC LIMIT {}""".format(requete_clan, limit))
   
    def get_comptes_coc(self, idDiscord):
        """renvoie une liste des comptes associés a cet identifiant, sous forme d'une liste de tupple
        (tagIG [0],discordID [1],pseudoIG [2],thIG [3], donne[4],recu [5],nbattaques[6],perf[7],bi[8],one[9],black[10],nbdips[11],perfdips[12],bidips[13],onedips[14],blackdips[15],perfdefs[16],nbdefs[17],clan[18)
        """
        return self.appel_bdd("""SELECT * FROM empire WHERE discordID='{}'""".format(str(idDiscord)))

    def get_data(self, tag) -> tuple:
        """renvoie un tuple des donnés  du compte associé a ce tag, sous forme d'un tupple
        (tagIG [0],discordID [1],pseudoIG [2],thIG [3], donne[4],recu [5],nbattaques[6],perf[7],bi[8],one[9],black[10],nbdips[11],perfdips[12],bidips[13],onedips[14],blackdips[15],perfdefs[16],nbdefs[17],clan[18])
        """
        return self.appel_bdd("""SELECT * FROM empire WHERE tagIG='{}'""".format(tag))[0]

    def get_classement_attaques(self, hdv, *, dips=False, clan=None, nb_etoiles=3) -> list:
        """renvoir les meilleurs selons les critères"""
        fin_dips = "dips" if dips else "memehdv"
        requete_clan = ",clantag="+clan if clan is not None else ""
        str_score = ["nbblack", "nbone", "nbbi", "nbperf"][nb_etoiles]
        return self.appel_bdd("""SELECT tagIG,discordID,pseudoIG,"nbattaques{1}","nbperf{1}","nbbi{1}","nbone{1}","nbblack{1}",
                                    (("{3}{1}"+0.00000000001)/("nbattaques{1}"+0.00000000001)) as X, clantag 
                                FROM empire 
                                WHERE thIG={0}{2} AND "nbattaques{1}">10  AND clantag NOT LIKE('éxterieur')
                                ORDER BY   X DESC 
                                """.format(hdv, fin_dips, requete_clan, str_score)) # TODO : ajouter la verif de clan

    def get_classement_defenses(self, hdv, *, limit=10, clan=None) -> list:
        """renvoie la liste de tuple des 10 meilleurs defs sur l'hdv"""
        requete_clan = ",clantag="+clan if clan is not None else ""
        return self.appel_bdd("""SELECT tagIG,discordID,pseudoIG,nbdefmemehdv,nbperfdefmemehdv,clantag,((nbperfdefmemehdv+0.00000000001)/(nbdefmemehdv+0.00000000001)) AS X FROM empire
                                 WHERE thIG={0}{2} AND nbdefmemehdv >4 AND clantag NOT LIKE('éxterieur') ORDER BY X DESC LIMIT {1}
                                """.format(hdv, limit, requete_clan))

    
    
    def reduire_dons(self, facteur=2):
        """divise l'ensemble des dons par facteur"""
        self.appel_bdd(
            """UPDATE empire SET donne=donne/{0},recu=recu/{0}""".format(facteur))
    
    
    
    def get_all_tag(self):
        """ renvoie l'ensemble des tags inclus dans la BDD"""
        return map(lambda e:e[0],self.appel_bdd("""SELECT tagig FROM empire"""))
    
   


    def edit_clan(self,tag,empire_clan_tag):
        """change le tag du clan du joueur"""
        if empire_clan_tag is None:
            empire_clan_tag="éxterieur"
        return self.appel_bdd("""UPDATE empire SET clantag = '{}' WHERE tagIG='{}'""".format(empire_clan_tag,tag))
   
    def maj_info(self,tag,clan,pseudo,town_hall):
        """mise a jour des elements dans la bdd

        Args:
            clan ([str,None]): [tag du clan du joueur]
            pseudo ([str]): [pseudo coc du joueur]
            town_hall ([int]): [hdv du joueur]
        """
        self.edit_pseudo(tag,pseudo)
        self.edit_clan(tag,clan if clan in self.liste_tag_clans else None)
        self.up_hdv(tag,town_hall)

    def add_clan(self,tag,nom,id_role_discord):
        if len(self.appel_bdd(f"""SELECT * FROM clans_empire WHERE tag LIKE('{tag}')"""))>=1:
            raise ValueError("clan déjà dans la base de données")
        self.appel_bdd(f"""
                        INSERT INTO clans_empire (tag,nom,id_role_discord) VALUES ('{tag}','{nom}','{id_role_discord}')""")

    def get_all_clans(self):
        liste_clans = self.appel_bdd(f"""SELECT tag,nom,id_role_discord FROM clans_empire """)
        return [Clan_empire(*clan) for clan in liste_clans]
    
def main():#pour  des tests locaux
    pass

if __name__=="__main__":
    main()
    

