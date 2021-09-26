import os

config={"Coc":{"mail":os.environ.get("mail"),
              "password":os.environ.get("password")},
        "Discord":{"token":os.environ.get("Token"),
                  "prefix":os.environ.get("prefix")},
        "bddlink":os.environ.get("DATABASE_URL")
       }
