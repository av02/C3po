import coc
import coc.errors
import database_outils





async def demarage(config,connection_bdd,cocClient):
    
    tagsJoueurs=connection_bdd.get_all_tag()
    async for player in coc_client.get_players(tagsJoueurs):
        connection_bdd.maj_info(player.tag,player.clan.tag if player.clan is not None else None,player.town_hall)

def boucle_infinie_coc(config,connection_bdd,discordClient,cocClient):
    clan_tags = config["liste_clans"]
    tagsJoueurs = connection_bdd.get_all_tag()
    # connection client coc, non bloquant
    
    
    
    
    
    # quand une attaque de guerre survient
    @cocClient.event
    @coc.WarEvents.war_attack(tags=clan_tags)
    async def current_war_stats(attack, war):
        if attack.attacker.clan.tag in clan_tags and attack.attacker.town_hall>=attack.defender.town_hall:# on controle qu'il est dans un de nos clans
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
            connection_bdd.add_def_gdc(
                                        attack.defender_tag,
                                        attack.stars==3,
                                        attack.defender.town_hall,
                                        attack.defender.name,
                                        attack.defender.clan.tag
                                       )




    @cocClient.event  
    @coc.ClanEvents.member_donations(tags=clan_tags)
    async def on_clan_member_donation(old,new):#TODO controller les odns négatifs
        if new.donations<old.donations:# si donné negatifs, alors c'est que debut saison ou quitté le clan
            return
        profil=await cocClient.get_player(old.tag)# on recupere le profil
        connection_bdd.add_don(old.tag,new.donations-old.donations,profil.town_hall,profil.name,old.clan.tag)
    

    @cocClient.event#mise a jour de la bdd quand un membre reçoit
    @coc.ClanEvents.member_received(tags=clan_tags)
    async def on_clan_member_received(old,new):
        if new.received<old.received:# si le joueur a des reçus negatifs, soit quitté le clan, soit debut de saison
            return
        profil = await cocClient.get_player(old.tag)# on recupere le profil 
        connection_bdd.add_recu(old.tag,new.received-old.received,profil.town_hall,profil.name,old.clan.tag)
        


    @cocClient.event#mise a jour de la bdd quand un membre change de pseudo
    @coc.PlayerEvents.name(tags= tagsJoueurs)
    async def on_name_change(old,new):
        print("\033[96mchnagement de nom",old.name,new.name)
        connection_bdd.edit_pseudo(old.tag,new.name)
    @cocClient.event# mise a jour de la bdd quand un membre change d'hdv
    @coc.PlayerEvents.town_hall(tags= tagsJoueurs)
    async def on_th_change(old,new):
        print("\033[96mth change", old.town_hall)
        connection_bdd.up_hdv(old.tag,new.town_hall)
    
    
    
    @cocClient.event  
    @coc.PlayerEvents.clan(tags=tagsJoueurs)
    async def on_clan_status_change(old,new):
        new_clan_tag = new.clan.tag if new.clan is not None else None
        connection_bdd.edit_clan(old.tag,new_clan_tag)
