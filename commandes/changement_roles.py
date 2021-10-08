async def maj_role(discordClient,discord_id,*clan_rejoints):
    """ajouter les roles de clan

    Args:
        discordClient ([discordClient]): [le client discord]
        discord_id ([int]): [l'identifiant du joueur]
        clan_rejoint ([list]):[liste des tags des differents clans de l'empire du joueur]
    """    
    #get les roles de l'user 
    #comparer avec les roles
    #maj des roles
    LISTE_CLANS=["#2PU29PYPR"]
    LISTE_ID_ROLES_CLANS=[777258978157264906]
    guild = discordClient.get_guild(729401132643909684)
    discord_user = await guild.fetch_member(discord_id)
    liste_roles_clans_discord = list(set(map(lambda role:role.id,discord_user.roles))&set(LISTE_ID_ROLES_CLANS)) #on prend une liste qui contient les roles associés aux clans que le joueur a 
    #TODO DONE:il faut sup les roles de liste_role qui sont pas dans clan_rejoint, et ajouter les reciproques
    liste_clans_rejoints = [LISTE_ID_ROLES_CLANS[LISTE_CLANS.index(x)] for x in clan_rejoints]
    liste_clans_en_trop=list(set(liste_roles_clans_discord)-set(liste_clans_rejoints))
    liste_clans_a_ajouter=list(set(liste_clans_rejoints)-set(liste_roles_clans_discord))
    #TODO: ajouter/retirer les roles
    if liste_clans_en_trop==[]:
        roles = [role for role in guild.role if role.id in liste_clans_en_trop]
        await discord_user.remove_roles(roles,reason="bot: clan quitté")
    if liste_clans_a_ajouter==[]:
        roles = [role for role in guild.role if role.id in liste_clans_a_ajouter]
        await discord_user.add_roles(roles,reason="bot: clan rejoint")
    
