from .sql import FetchDataBase, InsertData, UpdateDatabase




def orderStatus(orderNr, jobNr, partNr, amountsNr, databaseName, tableName, dateNow):
    if orderNr != None:
        table = [a if a == orderNr else a for a in
                 FetchDataBase(databaseName, f"SELECT * FROM {tableName} WHERE orders={orderNr} ORDER BY job ASC")]
    stateControl = False
    if (orderNr and jobNr and partNr and amountsNr) != None:
        if len(orderNr) >= 7 and len(jobNr) >= 1 and len(partNr) >= 6 and len(amountsNr) >= 1:
            print("Es ist nicht NONE")
            value = f"{orderNr}, {jobNr}, '{partNr}', {amountsNr.replace(',', '.')}, '{dateNow}'"
            print(value)
            for a in table:
                if partNr == a[3] and int(jobNr) == a[2]:
                    print(f"Job: {int(jobNr)} bereits vorhanden: {a[2]}, Auftragsnummer: {partNr} bereits vorhanden {a[3]}, ID: {a[0]}")
                    value1 = f"amounts='{a[4] + float(amountsNr.replace(',', '.'))}'"
                    value2 = f"id={a[0]}"
                    print(value)
                    UpdateDatabase(databaseName, tableName, value1, value2)
                    stateControl = True
            if stateControl == False:
                print(f"Folgende Daten werden ergänzt {databaseName}, {tableName}, {value}")
                InsertData(databaseName, tableName, value)