import discord
from discord import utils
import coc
from coc import utils
import sqlite3
import configparser
import os

# import donnés
config={"Coc":{"mail":os.environ.get("mail"),
              "password":os.environ.get("password")},
        "Discord":{"token":os.environ.get("Token"),
                  "prefix":os.environ.get("prefix")},
        "bddlink":os.environ.get("DATABASE_URL")
       }
clan_tags=["#2PU29PYPR","#29Q29PRY9","#29U9YR0QP","#2LL0UCY89","#2LR9RP20J","#2PYR2V202","#2Y2UVR99P","#2L0JQYUPU","#2LLCPYV9P","#2YU08J8UU"]# mettre ça dans une bdd
tagsJoueurs=[]
con= sqlite3.connect(config["bddlink"])
cur = con.cursor()
print("ope en cour")
cur.execute("""CREATE TABLE "nommage" ( `tagIG` TEXT, `IdDiscord` TEXT, `pseudoIG` TEXT, `th` INTEGER, PRIMARY KEY(`tagIG`) )""")
print("millieu")
cur.execute("""CREATE TABLE "scores" ( `tag` TEXT NOT NULL, `Perf` INTEGER DEFAULT 0, `bi` INTEGER DEFAULT 0, `one` INTEGER DEFAULT 0, 
`black` INTEGER DEFAULT 0, `donne` INTEGER DEFAULT 0, `recu` INTEGER DEFAULT 0, `Perfdips` INTEGER DEFAULT 0, `bidips` INTEGER DEFAULT 0,
`onedips` INTEGER DEFAULT 0, `blackdips` INTEGER DEFAULT 0, `th` INTEGER, PRIMARY KEY(`tag`,`th`) )""")
con.commit()
con.close()
print("opé réussie")      
con= sqlite3.connect(config["bddlink"])
cur.execute("SELECT tagIG FROM nommage")
for l in cur:
    tagsJoueurs.append(l[0])
con.commit()
con.close()

# connection client coc
cocClient= coc.login(email=config["Coc"]["mail"],password=config["Coc"]["password"],client=coc.EventsClient)#TODO: changer les mails....

# bot discord
class discordClient(discord.Client):
    async def on_message(self,message):
        if message.author.bot or message.channel.guild== None:
            return
        if not message.content.startswith(config["Discord"]["prefix"]):
            return
        commande = message.content[1:]
        args = commande.split(' ')
        commande = args[0]
        if commande =="ping":
            await message.channel.send("bien connecté")
        if commande=="trophés":
            await message.channel.send("{0.name} est a {0.trophies} trophés".format(await cocClient.get_player(args[1])))
        if commande == "ajouter"or commande == "claim" or commande == "add" :
            """ajouter un tag a un discord, #coc+@xx#XXXX/me"""
            if len(args)!=3 and len(message.mentions)!=1:
                return await message.channel.send("nombre d'arguments incorect")
            tag=utils.correct_tag(args[1])
            idDiscord=message.mentions[0].id
            try:
                player= await cocClient.get_player(tag)
            except coc.NotFound:
                return await message.channel.send("ce tag ne correspond a aucun joueur")
            except coc.Maintenance:
                return await message.channel.send("maintenance en cour, a plus tard :)")
            except coc.GatewayError:
                return await message.channel.send("une erreur inconue s'est produite dans la vérification du tag :(")
            else:
                connectionBDD = sqlite3.connect(config["bddlink"])
                Curseur = connectionBDD.cursor()

                try:
                    Curseur.execute("INSERT INTO nommage VALUES (?,?,?,?)",(tag,idDiscord,player.name,player.town_hall))
                    connectionBDD.commit()
                    connectionBDD.close()
                except sqlite3.IntegrityError:
                    await message.channel.send("déjà enregistré par le passé")
                else:
                    cocClient.add_player_updates(tag)
                    await message.channel.send("operation réussie")
        if commande == "gc":#couleur embed: #F6C471
            """afficher tous les comptes associés a un joueur """
            if len(message.mentions)!=1:# cas nb de tags incoherents 
                return await message.channel.send("merci de tag __une__ personne")
            idDiscord=message.mentions[0].id
            pseudo=message.mentions[0].display_name
            connectionBDD = sqlite3.connect(config["bddlink"])
            Curseur = connectionBDD.cursor()
            Curseur.execute("SELECT tagIG,PseudoIG FROM nommage where idDiscord = (?)",(idDiscord,))
            tags=[]
            for l in Curseur:
                tags.append(l[0])
            connectionBDD.commit()
            connectionBDD.close()
            if len(tags)==0:#cas pas dans bdd
                return await message.channel.send("pas encore de comptes associés")
            rep=discord.Embed(colour=0xf6c471)
            rep.set_author(name="Profil de "+str(pseudo))
            async for player in cocClient.get_players(tags):
                rep.add_field(name=player.name,value="<:HdvBot:884202091793506324> Hdv : {} \n<:ExpBot:884202964896608266> Niveau : {} \n<:TagBot:884204003070705754> Tag : {}".format(player.town_hall,player.exp_level,player.tag))
            rep.set_image(url="https://media.discordapp.net/attachments/859386512129654794/884100318936330261/comptes_lie.png")
            rep.set_thumbnail(url=message.mentions[0].avatar_url)
            rep.set_footer(text="créé par av#2616",icon_url="https://cdn.discordapp.com/avatars/397116327887896576/93f6ce8dde153200b213ba4ec531dd8f.webp?size=128")
            await message.channel.send(embed=rep)
        if commande == "retirer":
            """retirer un tag associé a un joueur"""
            pass
        if commande== "VL" or commande== "vl":# probleme de recuperation de member a partir member.id
            """commandes en SQL"""
            await message.channel.send("pas encore opé^^")
            con = sqlite3.connect(config["bddlink"])
            cur=con.cursor()
            cur.execute("""SELECT n.idDiscord,s.Perf,s.bi,s.one,s.black,s.Perfdips,s.bidips,s.onedips,s.blackdips,s.donne,s.recu FROM nommage n,scores s WHERE n.tagIG=s.tag AND s.th={} ORDER BY s.Perf ASC ,s.bi ASC""".format(args[1]))
            res=[]
            reponse="""```pseudo          3|2|1|0| dips: 3|2|1|0|| ratio"""
            
            for l in cur:
                res.append(l)
                member= await message.guild.fetch_member(int(l[0]))
                reponse+="\n{} {}|{}|{}|{}   ||||   {}|{}|{}|{}||    {}".format(member.display_name,l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9]/l[10] if l[10]!=0 else "NA")
            await message.channel.send(reponse+"```")
            con.close()
@cocClient.event
@coc.WarEvents.war_attack(tags=clan_tags)
async def current_war_stats(attack, war):
    print("an attack occured",attack.attacker.name,"de",attack.attacker.clan.name,"a fait:",attack.stars,"étoiles")
    if attack.attacker.clan.tag in clan_tags and attack.attacker.town_hall>=attack.defender.town_hall:
        print("tag:",attack.attacker_tag,"etoiles:",attack.stars,"th",attack.attacker.town_hall,attack.defender.town_hall,sep="\n\n")
        ajouter_bdd(tag=attack.attacker_tag,
                    etoiles=attack.stars,
                    dips=attack.attacker.town_hall!=attack.defender.town_hall,
                    th=attack.attacker.town_hall)




@cocClient.event  
@coc.ClanEvents.member_donations(tags=clan_tags)
async def on_clan_member_donation(old,new):#TODO controller les odns négatifs
    print("on a ", old," qui a donné ",new.donations-old.donations,"troupes dans ",old.clan)
    if old.clan.tag!=new.clan.tag:
        print("quitté clan ",old.clan.name,"nouveau:",new.clan.name)
        return
    prof=await cocClient.get_player(old.tag)
    ajouter_bdd(old.tag,donne=new.donations-old.donations,th=prof.town_hall)

@cocClient.event  
@coc.ClanEvents.member_received(tags=clan_tags)
async def on_clan_member_received(old,new):
    print("on a ", old," qui a reçu ",new.received-old.received,"troupes dans ",old.clan)
    if old.clan.tag!=new.clan.tag:
        return
    prof=await cocClient.get_player(old.tag)
    ajouter_bdd(old.tag,recu=new.received-old.received,th=prof.town_hall)


@cocClient.event
@coc.PlayerEvents.name(tags= tagsJoueurs)
async def on_name_change(old,new):
    con= sqlite3.connect(config["bddlink"])
    cur= con.cursor()
    cur.execute("UPDATE nommage SET pseudoIG = (?) WHERE tagIG= (?)",(new.name,new.tag))
    con.commit()
    con.close()
@cocClient.event
@coc.PlayerEvents.town_hall(tags= tagsJoueurs)
async def on_th_change(old,new):
    con= sqlite3.connect(config["bddlink"])
    cur= con.cursor()
    cur.execute("UPDATE nommage SET th = (?) WHERE tagIG= (?)",(new.townhall,new.tag))
    con.commit()
    con.close()

def ajouter_bdd(tag,etoiles=None,recu=None,donne=None,dips=False,th=None):#TODO:pour les dons
    connectionBDD = sqlite3.connect(config["bddlink"])
    Curseur = connectionBDD.cursor()
    Curseur.execute("SELECT COUNT (*) FROM (SELECT tag FROM `scores` WHERE tag=(?))",(tag,))#[0]==1#on prend le nb de tag egaux a celui de l'attaque, 1=> deja dans Bdd; 0=>pas encore dans BDD
    for r in Curseur:
        nb=r[0]
    if not nb==1:
        Curseur.execute("INSERT INTO scores (tag,th) VALUES (?,?)",(tag,th))
        connectionBDD.commit()
    if etoiles is not None and not dips:
        Curseur.execute("SELECT black,one,bi,Perf FROM scores WHERE tag=(?) AND th=(?)",(tag,th))
        for r in Curseur:
            Score = list(r)
            Score[etoiles]+=1
        Curseur.execute("UPDATE scores SET black=(?),one=(?),bi=(?),Perf=(?) WHERE tag=(?) AND th=(?)",(Score[0],Score[1],Score[2],Score[3],tag,th))
    elif etoiles is not None and dips:
        Curseur.execute("SELECT blackdips,onedips,bidips,Perfdips FROM scores WHERE tag=(?) AND th=(?)",(tag,th))
        for r in Curseur:
            Score = list(r)
            Score[etoiles]+=1
        Curseur.execute("UPDATE scores SET blackdips=(?),onedips=(?),bidips=(?),Perfdips=(?) WHERE tag=(?) AND th=(?)",(Score[0],Score[1],Score[2],Score[3],tag,th))
    elif donne is not None:
        Curseur.execute("SELECT donne FROM scores WHERE tag=(?) AND th=(?)",(tag,th))
        for r in Curseur:
            don = list(r)[0]
            don+=donne 
        Curseur.execute("UPDATE scores SET donne=(?) WHERE tag=(?) AND th=(?)",(don,tag,th))
    elif recu is not None:
        Curseur.execute("SELECT recu FROM scores WHERE tag=(?) AND th=(?)",(tag,th))
        for r in Curseur:
            anteRecu = list(r)[0]
            anteRecu+=recu 
        Curseur.execute("UPDATE scores SET recu=(?) WHERE tag=(?) AND th=(?)",(anteRecu,tag,th))
    connectionBDD.commit()
    connectionBDD.close()



discordClient().run(config["Discord"]["token"])
