import discord
import database_outils as dB
import config as config
import commandes.dispatch
async def scan(DiscordClient,message,args):
    if not message.author.id in [611927869429645333,447117251477241857,397116327887896576]:#YOH,CLAIRE ou av
        return
    for member in message.guild.members:
        liste_comptes = dB.get_compte_coc(member.id)
        if len(L)==0:
            await message.channel.send(f"```{member.id}```{member.display_name} n'a pas de comptes ajoutés")
            break
        present_dans_l_empire= False
        tags = map(lambda tupple_data:tupple_data[0],liste_comptes)
        async for player in DiscordClient.cocClient.get_players(tags):
            if player.clan is not None:
                if player.clan.tag in config["liste_clans"]:
                    present_dans_l_empire=True
                    break
            
        if not present_dans_l_empire:
            await message.channel.send(f"```{member.id}```{member.display_name} n'a pas de comptes dans l'empire")
            idDiscord=member.id
            pseudo=member.display_name
            rep=discord.Embed(colour=0xf6c471)
            rep.set_author(name="Profil de "+str(pseudo))
            liste_profils=[]
            async for player in DiscordClient.cocClient.get_players(tags):
                liste_profils.append(player)
            liste_profils.sort(reverse= True,key=lambda p:p.town_hall*1000+p.exp_level)   
            for player in liste_profils:    
                rep.add_field(name=player.name,value="<:HdvBot:884202091793506324> Hdv : {} \n<:ExpBot:884202964896608266> Niveau : {} \n<:TagBot:884204003070705754> Tag : {}\n🛡️ Clan : {}".format(player.town_hall,player.exp_level,player.tag,player.clan.name if player.clan is not None else "Pas de clan"))#,ligne_BDD[7]/(ligne_BDD[6]+0.000000000001)*100))
            rep.set_image(url="https://media.discordapp.net/attachments/859386512129654794/884100318936330261/comptes_lie.png")
            rep.set_thumbnail(url=message.mentions[0].avatar_url)
            rep.set_footer(text="Développement av#2616 | Design YohKun#7447 | Empire Galactique",icon_url="https://cdn.discordapp.com/avatars/397116327887896576/93f6ce8dde153200b213ba4ec531dd8f.webp?size=128")
            await message.channel.send(embed=rep)

        
    await message.channel.send("scan terminé")
            
