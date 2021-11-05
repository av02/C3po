import discord
import commandes.dispatch
import database_outils
from config import config

class discordClient(discord.Client):
    def __init__(self,connectionBDD,cocClient):
        intents= discord.Intents().all()
        self.cocClient=cocClient
        self.connectionBDD=connectionBDD
        discord.Client.__init__(self,intents=intents)
    
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
            await message.channel.send("{0.name} est a {0.trophies} trophés".format(await self.cocClient.get_player(args[1])))
        if commande == "ajouter"or commande == "claim" or commande == "add" :
            """ajouter un tag a un discord, #coc+@xx#XXXX/me"""
            return await commandes.dispatch.claim.claim(self,self.connectionBDD,args,message)
        
        if commande == "scan":
            return await commandes.dispatch.scan.scan(self,self.connectionBDD,message,args)
        
        if commande == "gc":#couleur embed: #F6C471
            """afficher tous les comptes associés a un joueur """
            return await commandes.dispatch.gc.gc(self,message,args)
        if commande == "retirer":
            """retirer un tag associé a un joueur"""
            pass
        if commande== "VL" or commande== "vl":# probleme de recuperation de member a partir member.id
            """commandes en SQL"""
            return await commandes.dispatch.VL.VL(self,message,args)
            return await message.channel.send("pas encore opérationel, prochaine etape^^")
            con= psycopg2.connect(config["bddlink"],sslmode='require')
            cur=con.cursor()
            cur.execute("""SELECT n.idDiscord,s.Perf,s.bi,s.one,s.black,s.Perfdips,s.bidips,s.onedips,s.blackdips,s.donne,s.recu FROM nommage n,scores s WHERE n.tagIG=s.tag AND s.th={} ORDER BY s.Perf ASC ,s.bi ASC""".format(args[1]))
            res=[]
            reponse="""
            ```pseudo          3|2|1|0| dips: 3|2|1|0|| ratio"""
            
            for l in cur:
                res.append(l)
                member= await message.guild.fetch_member(int(l[0]))
                reponse+="\n{} {}|{}|{}|{}   ||||   {}|{}|{}|{}||    {}".format(member.display_name,l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9]/l[10] if l[10]!=0 else "NA")
            await message.channel.send(reponse+"```")
            con.close()
        if commande=="DL" or commande=="classementdef":
            return await commandes.dispatch.VL.def_leader(self,message,args)

#def run(connectionBDD,token):
 #   discordClient(connectionBDD).run(token)

if __name__=="__main__":
    import database_outils
    from config import config
    discordClient(database_outils.appelsBDD("stockagev2.db")).run(config["Discord"]["token"])
    #run(database_outils.appelsBDD("stockagev2.db"),config["Discord"]["token"])
