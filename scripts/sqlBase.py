import mysql.connector

conn = mysql.connector.connect(host="95.213.155.74",
                               port=3306,
                               user="ttproduct_read",
                               password="7IIIQQxCWKbipA==",
                               database="tattooport")

def getDictByAttribute(sql_query,keyAttribute):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql_query)

    res_dict = {}
    for res in cursor:
        res_dict[res[keyAttribute]] = res
        del res_dict[res[keyAttribute]][keyAttribute]
    cursor.close()
    conn.commit()

    return res_dict

def getDict(sql_query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql_query)

    result = []
    for res in cursor:
        result.append(res)
    cursor.close()
    conn.commit()

    return result

def getOne(sql_query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql_query)

    result = None
    for res in cursor:
        result=res

    cursor.close()
    conn.commit()

    return result


