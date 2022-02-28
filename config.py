import os

config={"Coc":{"mail":os.environ.get("mail"),
              "password":os.environ.get("password")},
        "Discord":{"token":os.environ.get("Token"),
                  "prefix":os.environ.get("prefix")},
        "bddlink":os.environ.get("DATABASE_URL"),
        "liste_clans":[
                       "#2PU29PYPR",#Yoda
                       "#29Q29PRY9",#Yoda Academy
                       "#29U9YR0QP",#Tatooine
                       "#2LL0UCY89",#Endor
                       "#2LR9RP20J",#Ylesia
                       "#2YL9PLJR2",#Coruscant
                       "#2Y2UVR99P",#Kamino
                       "#2L0JQYUPU",#FeeNiX
                       "#2LLCPYV9P",#Naboo
                       "#2YU08J8UU",#E-Yoda
                       "#2LVCU2QQ8",#Hoth
                       "#2LVCUJLU0"#E-Yoda 2
                      ],
        "liste_id_administratifs":[
                                  611927869429645333,#yoh
                                  447117251477241857,#claire
                                  
                                  397116327887896576#av
                                   
                                      ],
        "liste_sous_admins":[
                                  611927869429645333,#yoh
                                  447117251477241857,#claire
                                  
                                  568527448677810208,#Thorn
                                  707204926849417357,#Xebec
                                  397116327887896576#av
                                   
                                      ],
        "dico_roles_clans":{"#2PU29PYPR":777258978157264906
                            },
        "liste_clan_empire":[],#contient des Clans_empire
        "id_serveur_discord":729401132643909684
       }
