import mysql.connector as cn

dbHost = "192.168.18.4"
dbPort = "3306"
dbUsername = "areeba"
dbPassword = "areebafyp"
dbDatabase = "db_classroom_management"

mydb = cn.connect(host=dbHost, user=dbUsername, passwd=dbPassword, database=dbDatabase)
myCursor = mydb.cursor()

#myCursor.execute("select * from wp_minas;")
#print (myCursor.fetchall())

myCursor.execute("select * from tbl_relays")
print(myCursor.fetchall())

#myCursor.execute("select * from wp_minas;")
#print (myCursor.fetchall())

mydb.close()