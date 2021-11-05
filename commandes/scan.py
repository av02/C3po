import discord
import database_outils as dB
import config

async def scan(DiscordClient,message,args):
    if not message.author.id in [611927869429645333,447117251477241857,397116327887896576]:#YOH,CLAIRE ou av
        return
    for member in message.guild.members:
        comptes = dB.get_compte_coc(member.id)
        if len(L)==0:
            await message.channel.send(f"```{member.id}```{member.display_name} n'a pas de comptes ajoutés")
            break
        present_dans_l_empire= False
        for c in comptes:
            pass
            #check presence comptes dans l'empire via l'api, ma bdd est  insufusante.
            #1 compte=> present_dans_l_empire=True;break
            
        if not present_dans_l_empire:
            await message.channel.send(f"```{member.id}```{member.display_name} n'a pas de comptes dans l'empire")
            #GC du joueur pour voir ses comptes enregistrés
            
        
    await message.channel.send("scan terminé")
            
