import requests
import re
from datetime import datetime
import mysql.connector
import pandas as pd
from send_mail import *


"""
Getting the id's from the database in order to generate the request
"""
try:

    mydb = mysql.connector.connect(
        host='ussitemanager.iviscloud.net',
        user='opdb_rw',
        password='testdbpw',
        database='ivigil_crm')

    cursor = mydb.cursor()

    sql = "SELECT \
     a.accountId, \
     p.potentialId, \
     p.unitId, \
     a.accountName \
     FROM account a \
     JOIN  potential p ON a.`accountId`=p.`accountId` \
     WHERE a.`active`='T' AND  a.accountId  NOT IN (1000,1009,1012,1013,1015) AND p.potentialId NOT IN(1014,1019) "

    cursor.execute(sql)
    myresult = cursor.fetchall()
    df = pd.DataFrame(myresult,
                      columns=['accountId', 'potentialId', 'unitId', 'accountName'])
    # print(df)

    """
      Id's which are collected from the db are stored in the Id lists
    """

    accountId = list(df['accountId'])
    potentialId = list(df['potentialId'])
    unitId = list(df['unitId'])
    accountName = list(df['accountName'])

    print("accountId", accountId)
    print("potentialId", potentialId)
    print("unitId", unitId)
    print("accountName", accountName)

    for p, q, r, s in zip(accountId, potentialId, unitId, accountName):

        req = 'http://kernel.iviscloud.net:8182/ivis-kernel-server/devicesList.jsp?s_deviceId='+r+'&siteName=&deviceIp=&project=all&status=all&version=all&uptime=true'
        response_API = requests.get(req)
        # print(response_API.status_code)
        data = response_API.text
        print("data",data)
        # print(type(data))
        word = '"status":true'
        # print("word:", word)

        if word in data:
            print("connected")
            pass


        else:
            print("Disconnected")

            a = re.search(r'"lastConnected":', data)
            temp = data[a.end():a.end() + 30]
            print("temp", temp)

            hour = temp[12:14]
            minute = temp[15:17]

            hour0 = datetime.now()
            hour1 = str(hour0)[11: 13]
            min1 = str(hour0)[14:16]

            final_hour = abs(int(hour1)-int(hour))
            final_min = int(min1)-int(minute)

            time_difference = (final_hour*60)+final_min
            if time_difference > 30:
                mail = ShutterEmail(r, s, last_conn=temp)
                mail.email()

    if mydb.is_connected():
        cursor.close()
        mydb.close()

except mysql.connector.Error as error:
    print("Failed to SELECT Data from MySQL table {}".format(error))

finally:
    print("MySQL connection is closed")



