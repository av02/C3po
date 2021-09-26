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

        
class appelsBDD:
    def __init__(self, bddlink):
        self.bddlink = bddlink

    @attrapeur_d_exception
    def appel_bdd(self, instruction: str, commit=True) -> list:
        """instructions SQL
        execute les instructions passées en arguments sur la Bdd
        """
        print("connectionBDD:",end="")
        con = psycopg2.connect(self.bddlink,sslmode='require')
        print("reussie  :)))")
        Curseur = con.cursor()
        print("instruction:",instruction)
        try:
            Curseur.execute(instruction)
        except Exception as e:
            print("erreur:" ,e)
            return []
        retour = []
        for l in Curseur:
            retour.append(l)
            print("result:",l)
        if commit:
            con.commit()
        con.close()
        return retour

    def set_cocClient(self,cocClient):#utilité?????
        self.cocClient = cocClient

    def check_presence_database(self, tag, th, pseudo, clan):
        """ verifie si le tag passé en argument est dans la base de donnée 
        sinon , l'ajoute avec l'hdv et le pseudo 
        """
        if len(self.appel_bdd("SELECT * FROM new WHERE tagIG = '{}'".format(tag))) == 0:
            self.appel_bdd("INSERT INTO nommage (tagIG,pseudoIG,thIG,clan) VALUES ('{}','{}',{},'{}')".format(
                tag, pseudo, th, clan))
        return

    def add_discord_id(self, tag, id, permission_ecraser=False):
        """ajoute l'identifiant discord associé a un compte
        ecrase le tag précédent si permission_ecraser==True
        """
        if len(self.appel_bdd("SELECT discordID FROM new WHERE tagIG='{}'".format(tag)))!=1:
            raise ValueError()
        if not permission_ecraser and self.appel_bdd("SELECT discordID FROM new WHERE tagIG='{}'".format(tag))[0] != (None,):
            raise PermissionError()
        self.appel_bdd("UPDATE new SET discordID={} WHERE tagIG='{}'".format(str(id), tag))
        return 

    def get_discord_id(self, tag) -> int:  # TODO controler si non enregistré
        """renvoie l'identifiant discord , None si non enregistré
        """
        return int(self.appel_bdd("SELECT discordID FROM new WHERE tagIG='{}'".format(tag))[0][0])

    def edit_pseudo(self, tag, pseudo):
        """modifie le pseudo du joueur, ecrase le précdent
        """
        self.appel_bdd(
            "UPDATE new SET pseudoIG='{}' WHERE tagIG='{}'".format(pseudo, tag))

    def edit_clan(self, tag, clan=None):
        """met a jour le clan du joueur avec son nouveau clan"""
        self.appel_bdd(
            """UPDATE new SET clan='{}' WHERE tagIG='{}'""".format(clan, tag))

    def up_hdv(self, tag, th):
        """a appeler dans le cas d'un changement d'hdv
        modifie l'hdv du joueur, deplace les attaques vers hdv -1 
        reset les def/hdv idem
        ecrase le précdent
        """
        stats = self.appel_bdd(
            "SELECT thIG,nbattaqueshdv,perfhdv,bihdv,onehdv,blackhdv FROM new WHERE tagIG='{}'".format(tag))[0]
        print("#1")
        if stats[0] != th:
            self.appel_bdd("UPDATE new SET thIG={},'nbattaqueshdvante'={},'perfhdvante'={},'bihdvante'={},'onehdvante'={},'blackhdvante'={}, 'nbattaqueshdv-1'=0,'perfhdv-1'=0,'bihdv-1'=0,'onehdv-1'=0,'blackhdv-1'=0, nbattaqueshdv=0,perfhdv=0,bihdv=0,onehdv=0,blackhdv=0,perfdefhdv=0,nbdefhdv=0 WHERE tagIG='{}'".format(
                th, stats[1], stats[2], stats[3], stats[4], stats[5], tag))

    def add_score_gdc(self, tag, etoiles,th,pseudo,clan, dips=False):
        """
        ajoute au joueur avec le tag le nombre d'étoiles,
        etoiles est le nombre d'étoiles de l'attaque (∈ ⟦0;3⟧)
        dips doit etre passé true si l'hdv ennemi est inferieur de 1
        ne pas appeler si Δhdv>1
        """
        self.check_presence_database(tag,th,pseudo,clan)
        fin_dips = "-1" if dips else ""  # si c'est un dips, on change la catégorie dans la bdd
        print("iteration n°1:")

        def _transcription_etoiles_strbdd(nbetoiles):
            return ["blackhdv", "onehdv", "bihdv", "perfhdv"][nbetoiles]
        print("iteration n°:2")
        valeurs_anterieures = self.appel_bdd("""SELECT nbattaqueshdv{},{} 
                                            FROM new WHERE tagIG='{}'""".format(fin_dips,
                                                                                    _transcription_etoiles_strbdd(
                                                                                        etoiles)+fin_dips,
                                                                                    tag))[0]
        print("iteration n°:3")
        self.appel_bdd("""UPDATE new SET 'nbattaqueshdv{}'={}, '{}'={} 
                        WHERE tagIG='{}'""".format(fin_dips,
                                                     valeurs_anterieures[0]+1,
                                                     _transcription_etoiles_strbdd(
                                                         etoiles)+fin_dips,
                                                     valeurs_anterieures[1]+1,
                                                     tag))
        print("iteration n°:4")

    def add_def_gdc(self, tag, perf: bool):
        """N'APPELER QUE SI LES HDV SONT ÉGAUX
        ajoutes 1 au nombre total de defs enregistrées, 
        et la valeur numerique associé au booléen perf
        dans la colone nbperfdef
        """
        valeurs_anterieures = self.appel_bdd(
            """SELECT nbdefhdv,perfdefhdv FROM nommage WHERE tagIG='{}'""".format(tag))[0]
        self.appel_bdd("""UPDATE new SET nbdefhdv={},perfdefhdv={} WHERE tagIG='{}'""".format(
            valeurs_anterieures[0]+1, valeurs_anterieures[1]+int(perf), tag))

    def add_don(self, tag, dons,th,pseudo,clan):
        """ajoute dons au dons associés au tag
        """
        self.check_presence_database(tag,th,pseudo,clan)
        valeur_anterieur = self.appel_bdd("""SELECT donne FROM new 
                                        WHERE tagIG='{}'""".format(tag))[0][0]
        self.appel_bdd("""UPDATE new SET donne={} WHERE tagIG='{}'""".format(
            int(valeur_anterieur)+dons, tag))

    def add_recu(self, tag, recu,th,pseudo,clan):
        """ajoute recu au recu associés au tag
        """
        self.check_presence_database(tag,th,pseudo,clan)
        valeur_anterieur = self.appel_bdd("""SELECT recu FROM new 
                                        WHERE tagIG='{}'""".format(tag))[0][0]
        self.appel_bdd("""UPDATE new SET recu={} WHERE tagIG='{}'""".format(
            int(valeur_anterieur)+recu, tag))

    def classement_dons(self, limit, *, clan=None) -> list:
        """renvoie une liste de tupples (idDiscord,tag,pseudo,donné,recu,ratio)"""
        requete_clan = "WHERE clan="+clan if clan is not None else ""
        return self.appel_bdd("""SELECT discordID,tagIG,pseudoIG,donne,recu,donne/recu FROM new {} ORDER BY donne/recu DESC LIMIT {}""".format(requete_clan, limit))
   
    def get_comptes_coc(self, idDiscord):
        """renvoie une liste des comptes associés a cet identifiant, sous forme d'une liste de tupple
        (tagIG [0],discordID [1],pseudoIG [2],thIG [3], donne[4],recu [5],nbattaques[6],perf[7],bi[8],one[9],black[10],nbdips[11],perfdips[12],bidips[13],onedips[14],blackdips[15],perfdefs[16],nbdefs[17],clan[18)
        """
        return self.appel_bdd("""SELECT * FROM 'new' WHERE discordID={}""".format(idDiscord))

    def get_data(self, tag) -> tuple:
        """renvoie un tuple des donnés  du compte associé a ce tag, sous forme d'un tupple
        (tagIG [0],discordID [1],pseudoIG [2],thIG [3], donne[4],recu [5],nbattaques[6],perf[7],bi[8],one[9],black[10],nbdips[11],perfdips[12],bidips[13],onedips[14],blackdips[15],perfdefs[16],nbdefs[17],clan[18])
        """
        return self.appel_bdd("""SELECT * FROM new WHERE tagIG='{}'""".format(tag))[0]

    def get_classement_attaques(self, hdv, *, dips=False, limit=10, clan=None, nb_etoiles=3) -> list:
        """renvoir les meilleurs selons les critères"""
        fin_dips = "hdv-1" if dips else ""
        requete_clan = ",clan="+clan if clan is not None else ""
        str_score = ["blackhdv", "onehdv", "bihdv", "perfhdv"][nb_etoiles]
        return self.appel_bdd("""SELECT tagIG,discordID,pseudoIG,nbattaques{1},perfhdv{1},bihdv{1},onehdv{1},blackhdv{1} FROM new WHERE thIG={0}{3} ORDER BY 
                              {4}{1}/nbattaques{1} DESC LIMIT {2} """.format(hdv, fin_dips, limit, requete_clan, str_score))

    def get_classement_defenses(self, hdv, *, limit=10, clan=None) -> list:
        """renvoie la liste de tuple des 10 meilleurs defs sur l'hdv"""
        requete_clan = ",clan="+clan if clan is not None else ""
        return self.appel_bdd("""SELECT tagIG,discordID,pseudoIG,nbdefhdv,perfdefhdv,clan FROM new
                                 WHERE thIG={0}{2} ORDER BY perfdefhdv/nbdefhdv DESC limit {1}
                                """.format(hdv, limit, requete_clan))

    def reduire_dons(self, facteur=2):
        """divise l'ensemble des dons par facteur"""
        self.appel_bdd(
            """UPDATE new SET donne=donne/{0},recu=recu/{0}""".format(facteur))

def main():#pour  des tests locaux
    pass

if __name__=="__main__":
    main()
