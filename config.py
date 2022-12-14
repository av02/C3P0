import os

config={"Coc":{"mail":os.environ.get("mail"),
              "password":os.environ.get("password")},
        "Discord":{"token":os.environ.get("Token"),
                  "prefix":os.environ.get("prefix")},
        "bddlink":os.environ.get("DATABASE_URL"),
        "liste_clans":[               #a déprecier=>liste_clans_empire[i].tag
                       "#2PU29PYPR",#Yoda
                       "#29Q29PRY9",#Yoda Academy
                       "#29U9YR0QP",#Tatooine
                       "#2LR9RP20J",#Ylesia
                       "#2YL9PLJR2",#Coruscant
                       "#2Y2UVR99P",#Kamino
                       "#2L0JQYUPU",#FeeNiX
                       "#2LLCPYV9P",#Naboo
                       "#2YU08J8UU",#E-Yoda
                       "#2LVCU2QQ8",#Hoth
                       "#2YRRJGJUY",#L’étoile noire 
                       "#2LVCUJLU0"#E-Yoda 2
                      ],
        "liste_id_administratifs":[
                                  611927869429645333,#yoh
                                  447117251477241857,#claire
                                  464188868716134431,#Nanoo
                                  397116327887896576#av
                                   
                                      ],
        "liste_sous_admins":[
                                  611927869429645333,#yoh
                                  447117251477241857,#claire
                                  464188868716134431,#Nanoo
                                  568527448677810208,#Thorn

                                  397116327887896576#av
                                   
                                      ],
        "dico_roles_clans":{"#2PU29PYPR":777258978157264906#a déprecier=>liste_clans_empire[i].tag:liste_clans_empire[i].id_role_associe
                            },
        "liste_clan_empire":[],#contient des Clans_empire
        "id_serveur_discord":729401132643909684,
        "roles_hdv":{"10":741754614369484801,
                    "11":741754668929122427,
                    "12":741754862076821625,
                    "13":741754912236372060,
                    "14":830882079109152809,
                    "15":1024774361858711562}
       }
