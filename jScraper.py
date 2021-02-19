########################################################################
########################################################################
####                                                                ####
####                            jTrain!                             ####
####                                                                ####
####                        Author: Paul Rich                       ####
####                                                                ####
####                                                                ####
####        Description: Scrapes the jArchive.com website           ####
####                    using beautifulSoup4, cleans the            ####
####                    scraped clues/answers/info and              ####
####                    stores the data in a MySQL database.        ####
####                                                                ####
####        Note: Inspirational credit goes to Jeopardy!            ####
####              champ Roger Craig, who spoke on the show          ####
####              about his own program he created to study         ####
####              for the show, and to trivia-trainer.com           ####
####              who seem to have beaten me to the punch. ;)       ####
####              Also a special thanks to the volunteers at        ####
####              jArchive, as well as the writers of Jeopardy!     ####
####              and of course, thank you Alex.                    ####   
####                                                                ####
########################################################################                                        ####
########################################################################                                  

import requests
from bs4 import BeautifulSoup
import mysql.connector



def pad_clues(clues, answers):
    if (len(clues) == 30 ):
        return
    else:
        index = 0
        while (index < 30):
            if (answers[index] == None):
                add_blank(clues, index)
            index += 1
        return


def add_blank(clues, index):
    end_index = len(clues)
    clues.append("")
    while (end_index > index):
        clues[end_index] = clues[end_index - 1]
        end_index -= 1
    clues[index] = "BLANK"

def clean_clues(clues):
    cleaned_array = []

    for tag in soup.find_all("span"):
        tag.replaceWith(' -- ')

    #print("After Padding: " + str(len(clues)))
    for clue in clues:
        if (clue != "BLANK"):
            split_j = str(clue).split('">')
            split_j = split_j[1].split('</td')
            split_j = str(split_j[0])
            split_j = split_j.replace("<br/>", " ")
            split_j = split_j.replace("&amp;", "&")
            split_j = split_j.replace("<br/>", "\n")
            if ("<a href" in split_j):
                cleaned_array.append("BLANK")
            else:
                cleaned_array.append(split_j)
        else:
            cleaned_array.append("BLANK")
    return cleaned_array



mydb = mysql.connector.connect(
    host="localhost",
    user="USER",
    password="PASSWORD",
    database="DB"
)

print(mydb)


URL_Start = "https://www.j-archive.com/showgame.php?game_id="

# First show to scrape - Note: represents the URL show number, not taping number.
showNumber = 6905           

# stop at this show number
lastShowNumber = 6948       

# main loop to connect to jArchive, scrape show information and write to DB.
while(showNumber < lastShowNumber):

    # Used to hold the Jeopardy/Double Jeopardy round categories
    j_round_cat_array = []
    dj_round_cat_array = []

    # used to hold the Jeopardy/Double Jeopardy round clues
    j_clue_array = []
    dj_clue_array = []

    # Used to hold the Jeopardy/Double Jeopardy round answers
    j_answer_array = []
    dj_answer_array = []

    # Combine URL prefix with show ID number
    URL = URL_Start + str(showNumber)

    # Send page request to URL
    page = requests.get(URL)

    # Return the content of the page as a parseable soup object
    soup = BeautifulSoup(page.content, 'html.parser')

    ### --- Jeopardy Round Parsing --- ###
    jeopardy_round = soup.find(id='jeopardy_round')

    if (jeopardy_round == None):
        print("ABORTED: Missing round in show number: " + str(showNumber))
        showNumber += 1
        continue

    # Find all category name blocks
    jcategories = jeopardy_round.find_all(class_='category_name')

    # Check that there are no missing categories, which often indicate missing
    # clues and/or misformatted shows
    if (len(jcategories) < 6):
        print("ABORTED: Missing Categories in show number: " + str(showNumber))
        showNumber += 1
        continue

    # Find all clue text blocks
    j_clue_text = jeopardy_round.find_all(class_='clue_text')
    
    # Append all clues to the clue array
    for j_clue in j_clue_text:
        j_clue_array.append(j_clue)

    # Find the show information, located in the H1 header tag
    h1Tag = soup.find("h1")
    showInfo = h1Tag.text
    print(showInfo)
    

    # Find all J! clue classes
    j_divs = (jeopardy_round.find_all(class_='clue'))

    	# Each jdiv (30) holds a clue's html block, parse for answer in loop
    for jdiv in j_divs:
		
		# split the html block on correct response code
        jdiv2 = str(jdiv).split('correct_response&quot;&gt;')
        if (len(jdiv2) > 1):

            # Remove the formatting for the <i> tags
            jans = jdiv2[1].replace("&lt;i&gt;", "").replace("&lt;//i&gt;", "")
            
            # split the correct response on the back half to rid of extra html code
            jans = jans.split('&lt;')[0].replace("&amp;", "&").replace("&quot;", "")

            
			# add the cleaned answer to the answer array
            j_answer_array.append(jans)
        else:
            j_answer_array.append(None)


    

	### --- Double Jeopardy Round Parsing --- ###
    double_jeopardy_round = soup.find(id='double_jeopardy_round')

    if (double_jeopardy_round == None):
        print("ABORTED: Missing round in show number: " + str(showNumber))
        showNumber += 1
        continue

	# Find all category name blocks
    djcategories = double_jeopardy_round.find_all(class_='category_name')

    # Check that there are no missing categories, which often indicate missing
    # clues and/or misformatted shows
    if (len(djcategories) < 6):
        print("ABORTED: Missing Categories in show number: " + str(showNumber))
        showNumber += 1
        continue

	# Find all clue text blocks
    dj_clue_text = double_jeopardy_round.find_all(class_='clue_text')
	
    # Append all clues to the clue array
    for dj_clue in dj_clue_text:
        dj_clue_array.append(dj_clue)
    

	# Find all DJ! clue classes and convert them to strings
    dj_divs = (double_jeopardy_round.find_all(class_='clue'))

	# Each djdiv (30) holds a clue's html block, parse for answer in loop
    for djdiv in dj_divs:

		# split the html block on correct response code
        djdiv2 = str(djdiv).split('correct_response&quot;&gt;')
        if (len(djdiv2) > 1):
			# split the correct response on the back half to rid of extra html code

            # Remove the formatting for the <i> tags
            djans = djdiv2[1].replace("&lt;i&gt;", "").replace("&lt;//i&gt;", "")
            
            # split the correct response on the back half to rid of extra html code
            djans = djans.split('&lt;')[0].replace("&amp;", "&").replace("&quot;", "")

			# add the cleaned answer to the answer array
            dj_answer_array.append(djans)
        else:
            dj_answer_array.append(None)
    
    ### --- Final Jeopardy Round Parsing --- ###
    final_j = soup.find(id='final_jeopardy_round')

    final_found = True
    if (final_j == None):
        final_found = False

    if (final_found):
	    # Find the final jeopardy category name block
        final_j_cat = final_j.find(class_='category_name')
	    # Find the final jeopardy clue text block
        fjquestion = final_j.find(class_='clue_text')
	    # Find the final jeopardy correct resopnse block and convert to str
        fj_div = (str) (final_j.find(class_='final_round'))

        # Split on correct respnse, including quote and > symbols
        if ('correct_response\\&quot;&gt;' in fj_div) :
            fjdiv2 = fj_div.split('correct_response\\&quot;&gt;')[1]
            fjans = fjdiv2.split('/em&gt;')[0]
        # Split on correct respnse, without quote and > symbols
        else:
	    # split the html block on correct response code
            fjdiv2 = fj_div.split('correct_response')[1]
	    # split the correct response on the back half to rid of extra html code
            fjans = fjdiv2.split('&lt;')[0]

        # Remove extra html in final jeopardy answer
        if ('i&gt;' in fjans):
            fjans = fjans.replace('i&gt;','')
        if ('&quot;' in fjans):
            fjans = fjans.replace('&quot;', '')
        if ('&lt;' in fjans):
            fjans = fjans.replace('&lt;','')
        if ('&amp;' in fjans):
            fjans = fjans.replace('&amp;', '&')
        if ('/' in fjans):
            fjans = fjans.replace('/', '')
        if ('\\' in fjans):
            fjans = fjans.replace('\\', '')
	

	#### --- END OF PARSING --- ###

	# Add the category names to the category name array for J!/DJ!
    for category in jcategories:
        j_round_cat_array.append(category.text)
    for category in djcategories:
        dj_round_cat_array.append(category.text)

    # used to determine the current category, and dollar amount
    clue_index = 0

    # Used for debugging missing clues and clue padding function
    #print("CLUES FOUND: " + str(len(j_clue_array)))
    #print("ANSWERS FOUND: " + str(len(j_answer_array)))
    
    # Call the clue padding functions for each round.
    pad_clues(j_clue_array, j_answer_array)
    pad_clues(dj_clue_array, dj_answer_array)

    # Call the clue cleaning functions for each round.
    j_clue_array = clean_clues(j_clue_array)
    dj_clue_array = clean_clues(dj_clue_array)

    # Initial clue value set to 200 for the first row of clues in round 1
    clue_value = 200

    # Prepared the 30 Clues in the first round to be written to the DB
    while (clue_index < 30):
        
        # If this is true, the end of the row was reached, increment value
        if (clue_index % 6 == 0 and clue_index != 0):
            clue_value += 200
        
        # Gather the current clue, answer and category
        current_clue = j_clue_array[clue_index]
        current_answer = j_answer_array[clue_index]
        current_cat = j_round_cat_array[clue_index % 6]
        
        # If clue information is not missing, insert the record into the DB
        if (current_clue != "BLANK" and current_answer != "BLANK"):
            mycursor = mydb.cursor()
            sql = "INSERT INTO clues (clue_category, clue_text, clue_answer, clue_show, clue_round, clue_value) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (current_cat, current_clue, current_answer, showInfo, "1", clue_value)
            mycursor.execute(sql, val)
            mydb.commit()
        clue_index += 1
    # End of writing first round clues

    # begin clue value at 400 for double jeopardy round
    clue_value = 400
    # reset clue index, as DJ has a separate array from first round
    clue_index = 0

    # Prepared the 30 Clues in the first round to be written to the DB
    while (clue_index < 30):

        # If this is true, the end of the row was reached, increment value
        if (clue_index % 6 == 0 and clue_index != 0):
            clue_value += 400

        # Gather the current clue, answer and category    
        current_clue = dj_clue_array[clue_index]
        current_answer = dj_answer_array[clue_index]
        current_cat = dj_round_cat_array[clue_index % 6]
        
        # If clue information is not missing, insert the record into the DB
        if (current_clue != "BLANK" and current_answer != "BLANK"):
            mycursor = mydb.cursor()
            sql = "INSERT INTO clues (clue_category, clue_text, clue_answer, clue_show, clue_round, clue_value) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (current_cat, current_clue, current_answer, showInfo, "2", clue_value)
            mycursor.execute(sql, val)
            mydb.commit()
        clue_index += 1
    # End of writing second round clues


    # open a new cursor for final jeopardy
    mycursor = mydb.cursor()
    if (final_found):
        sql = "INSERT INTO clues (clue_category, clue_text, clue_answer, clue_show, clue_round, clue_value) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (final_j_cat.text, fjquestion.text, fjans, showInfo, "0", "0")
        mycursor.execute(sql, val)
        mydb.commit()

    print("Show #" + str(showNumber) + " successfully inserted")
    showNumber += 1

mycursor = mydb.cursor()
sql = 'DELETE FROM clues where clue_text like "%="'
mycursor.execute(sql)
mydb.commit()
