import sqlite3

def NewDataBase(database, tablename, datas):
    con =sqlite3.connect(database)
    cur = con.cursor()
    print(f"Es wird eine Tabelle mit dem Namen ['{tablename}'] und den Spalten ['{datas}'] erstellt")
    cur.execute(f"CREATE TABLE {tablename} ({datas})")
    con.commit()
    print(f"Datenbank mit dem Namen [{database}] wurde erfolgreich erstellt!")
    con.close()

def InsertData(database, tablename, value ):
    con = sqlite3.connect(database)
    cur = con.cursor()
    IDs = []
    for a in FetchDataBase(database, f"SELECT id FROM {tablename} ORDER BY id ASC"):
        IDs.append(a)
        print(a)
    #print(IDs.pop()[0])
    if len(IDs) != 0:
        cur.execute(f"INSERT INTO {tablename} VALUES({IDs.pop()[0]+1}, {value})") #
    else:
        cur.execute(f"INSERT OR REPLACE INTO {tablename} VALUES({0}, {value})") #
    con.commit()
    print(f"Die Datenbank {database}, wurde mit den Daten [{value}] erweitert")
    con.close()

def FetchDataBase(database, fetchcommand):
    con = sqlite3.connect(database)
    cur = con.cursor()
    result = cur.execute(f"{fetchcommand}")
    print(f"Daten wurden aus der Datenbank geladen: {result}")
    return result

def UpdateDatabase(database, tablename, value1, value2 ):
    con = sqlite3.connect(database)
    cur = con.cursor()
    insert = f"UPDATE {tablename} SET {value1} WHERE {value2}"
    cur.execute(insert)
    print(f"In {tablename} wurde Menge {value1} erweitert! Mit der ID {value2}")
    con.commit()
    con.close()

def DeleteFromDatabase(database, tablename, value):
    con = sqlite3.connect(database)
    cur = con.cursor()
    delete =  f"DELETE FROM {tablename} WHERE id={value}"
    cur.execute(delete)
    con.commit()
    print(f"In {tablename} wurde Menge {value} gelöscht!")
    con.close()

def FreeSqlOrder(database, tablename, comand):
    con = sqlite3.connect(database)
    cur = con.cursor()
    com = comand
    cur.execute(com)
    con.commit()
    print(f"Der Befehl {comand} wurde ausgeführt")
    con.close()