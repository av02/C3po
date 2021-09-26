import os
import psycopg2


connectionBDD = psycopg2.connect(os.environ.get("DATABASE_URL"))#,sslmode='require')
Curseur = connectionBDD.cursor()
Curseur.execute("""CREATE TABLE "new" ( tagIG TEXT, discordID INTEGER, pseudoIG TEXT, thIG INTEGER, donne INTEGER DEFAULT 0, recu INTEGER DEFAULT 0,nbattaqueshdv INTEGER DEFAULT 0, perfhdv INTEGER DEFAULT 0, bihdv INTEGER DEFAULT 0, onehdv INTEGER DEFAULT 0, blackhdv INTEGER DEFAULT 0,"nbattaqueshdv-1" INTEGER DEFAULT 0, "perfhdv-1" INTEGER DEFAULT 0, "bihdv-1" INTEGER DEFAULT 0, "onehdv-1" INTEGER DEFAULT 0, "blackhdv-1" INTEGER DEFAULT 0, perfdefhdv INTEGER DEFAULT 0, nbdefhdv INTEGER DEFAULT 0, clan TEXT, attaqueshdvante INTEGER, perfhdvante INTEGER, bihdvante INTEGER, onehdvante INTEGER, blackhdvante INTEGER, PRIMARY KEY(tagIG) )""",)
Curseur.execute("""INSERT INTO new  (tagIG,thIG,pseudoIG,discordID,donne,recu,nbattaqueshdv,perfhdv,bihdv,onehdv,blackhdv,"nbattaqueshdv-1","perfhdv-1","bihdv-1","onehdv-1","blackhdv-1") SELECT scores.tag,MAX(scores.th),MIN(pseudoIG),IdDiscord,SUM(donne),SUM(recu),AVG(perf+bi+one+black),AVG(perf),AVG(bi),AVG(one),AVG(black),AVG(perfdips+bidips+onedips+blackdips),AVG(perfdips),AVG(bidips),AVG(onedips),AVG(blackdips) FROM scores LEFT JOIN nommage ON  scores.tag=nommage.tagIG AND scores.th=nommage.th GROUP BY scores.tag,IDdiscord""")
connectionBDD.close()
