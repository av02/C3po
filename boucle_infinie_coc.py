import coc
import database_outils

def boucle_infinie_coc(config,connection_bdd,discordClient,cocClient):
    clan_tags=["#2PU29PYPR","#29Q29PRY9","#29U9YR0QP","#2LL0UCY89","#2LR9RP20J","#2PYR2V202","#2Y2UVR99P","#2L0JQYUPU","#2LLCPYV9P","#2YU08J8UU"]# mettre ça dans une bdd
    tagsJoueurs=connection_bdd.get_all_tag()
    # connection client coc, non bloquant
    
    @cocClient.event# quand une attaque de guerre survient
    @coc.WarEvents.war_attack(tags=clan_tags)
    async def current_war_stats(attack, war):
        print("un attaque survint:",attack.attacker.name,"de",attack.attacker.clan.name,"a fait:",attack.stars,"étoiles")
        if attack.attacker.clan.tag in clan_tags and attack.attacker.town_hall>=attack.defender.town_hall:# on controle qu'il est dans un de nos clans
            print("tag:",attack.attacker_tag,"etoiles:",attack.stars,"th",attack.attacker.town_hall,attack.defender.town_hall,sep="\n\n")
            if attack.attacker.town_hall != attack.defender.town_hall and  attack.attacker.town_hall != attack.defender.town_hall+1: # ce n'est un un x vs x , ni un x vs x-1
                return   
            connection_bdd.add_score_gdc(attack.attacker_tag,
                                        attack.stars,
                                        attack.attacker.town_hall,
                                        attack.attacker.name,
                                        attack.attacker.clan.tag,
                                        attack.attacker.town_hall != attack.defender.town_hall)
            return
        else:
            if attack.attacker.town_hall != attack.defender.town_hall:
                return
            connection_bdd.add_def_gdc(attack.defender_tag,
                                       attack.stars==3
                                        )




    @cocClient.event  
    @coc.ClanEvents.member_donations(tags=clan_tags)
    async def on_clan_member_donation(old,new):#TODO controller les odns négatifs
        print("on a ", old," qui a donné ",new.donations-old.donations,"troupes dans ",old.clan)
        if new.donations<old.donations:# si donné negatifs, alors c'est que debut saison ou quitté le clan
            return
        profil=await cocClient.get_player(old.tag)# on recupere le profil
        connection_bdd.add_don(old.tag,new.donations-old.donations,profil.town_hall,profil.name,old.clan.tag)
    

    @cocClient.event#mise a jour de la bdd quand un membre reçoit
    @coc.ClanEvents.member_received(tags=clan_tags)
    async def on_clan_member_received(old,new):
        print("on a ", old," qui a reçu ",new.received-old.received,"troupes dans ",old.clan)# pour les logs, aucun interet
        if new.received<old.received:# si le joueur a des reçus negatifs, soit quitté le clan, soit debut de saison
            return
        profil = await cocClient.get_player(old.tag)# on recupere le profil 
        connection_bdd.add_recu(old.tag,new.received-old.received,profil.town_hall,profil.name,old.clan.tag)
        


    @cocClient.event#mise a jour de la bdd quand un membre change de pseudo
    @coc.PlayerEvents.name(tags= tagsJoueurs)
    async def on_name_change(old,new):
        print("chnagement de nom",old.name,new.name)
        connection_bdd.edit_pseudo(old.tag,new.name)
    @cocClient.event# mise a jour de la bdd quand un membre change d'hdv
    @coc.PlayerEvents.town_hall(tags= tagsJoueurs)
    async def on_th_change(old,new):
        print("th change", old.th)
        connection_bdd.up_hdv(old.tag,new.town_hall)
    
    
    
    @cocClient.event  
    @coc.PlayerEvents.clan(tags=tagsJoueurs)
    async def on_clan_status_change(old,new):
        print("il y a {} qui a quitté {} ou rejoint {}".format(old.name,old.clan,new.clan))
        pass
