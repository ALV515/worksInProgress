
#Creates XML Documents from SQLite file
import sqlite3

movie_outfile = open('movies.xml', 'w+')
people_outfile = open('people.xml', 'w+')
oscar_outfile = open('oscars.xml', 'w+')


#Creates outfiles
db = sqlite3.connect('movie.sqlite')

movie_outfile.write('<?xml version="1.0" encoding="iso-8859-1"?>' + "\n")
movie_outfile.write('\n')
movie_outfile.write("<movies>" + "\n")

people_outfile.write('<?xml version="1.0" encoding="iso-8859-1"?>' + "\n")
people_outfile.write('\n')
people_outfile.write("<people>" + "\n")

oscar_outfile.write('<?xml version="1.0" encoding="iso-8859-1"?>' + "\n")
oscar_outfile.write("\n")
oscar_outfile.write("<oscars>" + "\n")

cursor = db.cursor()
cursor2 = db.cursor()
cursor3 = db.cursor()
cursor4 = db.cursor()

#Executes SQL to get IDs
cursor.execute("SELECT DISTINCT id FROM Movie")

for row in cursor:
    #Code to get director and actor IDs
    cursor2.execute("SELECT d.director_id FROM Director d, Movie m WHERE m.id = d.movie_id AND m.id = " + row[0])

    for row2 in cursor2:
        movie_outfile.write("   <movie " +"id = " " \"" + "M" + row[0] + "\"" + "director =" + "\"" + "P" + row2[0] + "\"" "\n" + " ")
        cursor3.execute("SELECT a.actor_id FROM Actor a, Movie m WHERE m.id = a.movie_id AND m.id = " + row[0])
        movie_outfile.write("       actors = " + "\"")

        for row3 in cursor3:
            movie_outfile.write("P" + row3[0] + " ")
        movie_outfile.write("\"" +">" + "\n")

    #Gets everything needed from Movie to add to the XML
    cursor4.execute("SELECT name,year,rating,runtime,genre,earnings_rank FROM MOVIE WHERE id = " + row[0])
    for row4 in cursor4:
        movie_outfile.write("       <name>" + row4[0] +  "</name>" + "\n")
        movie_outfile.write("       <year>" + str(row4[1]) + "</year>" + "\n")
        movie_outfile.write("       <rating>" + row4[2] + "</rating>" + "\n")
        movie_outfile.write("       <runtime>" + str(row4[3]) + "</runtime>" + "\n")
        movie_outfile.write("       <genre>" + row4[4] + "</genre>" + "\n")
        movie_outfile.write("       <earnings_rank>" + str(row4[5])+ "</earnings_rank>" + "\n")
        movie_outfile.write("       </movie>" + "\n")
movie_outfile.write("</movies>")

cursor4.close
cursor3.close()
cursor2.close()
cursor.close()


cursor = db.cursor()
c2 = db.cursor()
c3 = db.cursor()
c4 = db.cursor()
c5 = db.cursor()

cursor.execute("SELECT id FROM Person")

for row in cursor:
    #This code tries to build out the people outfile
    #Doesn't work perfectly, duplicates the acted_in attribute if an actor has appeared in more than one movie
    c2.execute("SELECT a.movie_id FROM Actor a, Person p WHERE p.id = a.actor_id AND p.id =" + row[0])

    actedIn = [ ]
    i = 0

    for aRow in c2:
        people_outfile.write("<person id = " + "\"" + row[0] + "\" ")
        thisMovie = aRow[0]
        actedIn.append(thisMovie)
        i+=1
        people_outfile.write("actedIn = ")
        for movie in actedIn:
            people_outfile.write("\"" + movie + "\"" + ">")
        people_outfile.write("\n")

    c3.execute("SELECT d.movie_id FROM Director d, Person p WHERE p.id = d.director_id AND p.id =" + row[0])

    directedIn = [ ]
    j = 0

    for dRow in c3:
        if not actedIn:
            people_outfile.write("<person id = " + "\"" +  row[0] + "\" ")
        thisDir = dRow[0]
        directedIn.append(thisDir)
        j+=1
        people_outfile.write("directed = ")
        for movie in directedIn:
            people_outfile.write("\"" + movie + "\"" + ">")
        people_outfile.write("\n")


    c4.execute("SELECT o.year, o.type FROM Oscar o, Person p WHERE o.person_id = p.id AND p.id = " + row[0])

    #Builds arays to keep oscars and oscar types
    oscarArray = [ ]
    typeArr = [ ]
    z = 0
    y = 0
    for oRow in c4:
        thisOscar = oRow[0]
        thisType = oRow[1]
        oscarArray.append(thisOscar)
        typeArr.append(thisType)
        z+=1
        people_outfile.write("      oscars = ")
        #Checks to see if the oscar in oscar array is Best Picture in the type array, and prints differently to
        #the XML doc depending
        for oscar in oscarArray:
            for t in typeArr:
                if(t is "BEST-PICTURE"):
                    people_outfile.write("\"" + str(oscar) + "00000" + "\"" + " ")
            people_outfile.write("\"" + str(oscar) + row[0] + "\"" + " ")
        people_outfile.write("\n")

    c5.execute("SELECT name, dob, pob FROM Person WHERE id = " + row[0])

    for x in c5:
        name = x[0]
        dob = x[1]
        pob = x[2]

        people_outfile.write("      <name>" + str(name) + "</name>" + "\n")
        people_outfile.write("      <dob>" + str(dob) + "</dob>" + "\n")
        people_outfile.write("      <pob>" + str(pob) + "</pob>" + "\n")
        people_outfile.write("</person> " + "\n")



cursor.close()
c2.close()
c3.close()
c4.close()
c5.close()


cursor = db.cursor()

#Builds out oscar outfile
cursor.execute("SELECT movie_id, person_id, type, year FROM Oscar")

for row in cursor:
    mID = row[0]
    pID = row[1]
    oType = row[2]
    year = row[3]

    if(pID == None):
        oscar_outfile.write("<oscar = " + "id = " + "\"" + str(year) + "00000" + "\" " + "movie_id = " + "\"" + mID + "\"" + ">" + "\n")
        oscar_outfile.write("   <type = " + "\"" + str(oType) + "\"" + "</type>" + "\n")
        oscar_outfile.write("   <year = " + "\"" + str(year) + "\"" + "</year>" + "\n")
        oscar_outfile.write("</oscar>" + "\n")

    oscar_outfile.write("<oscar = " + "id = " + "\"" + str(year) + str(mID) + "\" "  + "movie_id =" + "\"" + str(mID) + "\" " +  "person_id = " + "\"" + str(pID) + "\"" + ">" + "\n")
    oscar_outfile.write("   <type = " + "\"" + str(oType) + "\"" + "</type>" + "\n")
    oscar_outfile.write("   <year = " + "\"" + str(year) + "\"" + "</year>" + "\n")
    oscar_outfile.write("</oscar>" + "\n")


cursor.close()
movie_outfile.close()
people_outfile.close()
oscar_outfile.close()
