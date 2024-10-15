# from app import db

# db.create_all()

import sqlite3

#Open database
conn = sqlite3.connect('app.db')



# Create cursor object
c= conn.cursor()
  
# Query for INNER JOIN
# c.execute('''SELECT facility.name FROM facility
# INNER JOIN activity.name, activity.price FROM activity
# ON facility.facilityId = activity.facilityId''')



c.execute('''
 SELECT  facility.name, activityEvent.name, activityEvent.day, activityEvent.startTime, activityEvent.endTime FROM activityEvent
        INNER JOIN facility ON activityEvent.facilityId = facility.facilityId

''')
  
# Fetching rows from the result table
result = c.fetchall()
for row in result:
    print(row)








conn.close()



# from app import db

# db.create_all()
