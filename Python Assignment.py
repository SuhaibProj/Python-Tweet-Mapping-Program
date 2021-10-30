import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import folium, json
import webbrowser, os
import re

win = tk.Tk()   # Create instance of tkinter
win.title("Suhaib's Tweet Search & Mapper")   # Add a title
win.configure(bg='mint cream')
# Disable resizing the GUI at specific limits
win.minsize(width=350,height=250)
win.maxsize(width=700,height=700)
win.resizable(0,0)

# Modify adding a Label for simple searching
searchLbl = ttk.Label(win, text="Enter a broad case sensitive search:")
searchLbl.grid(column=0, row=0)

# Adding a Textbox for simple searching 
searchName = tk.StringVar()
nameEntered = ttk.Entry(win, width=30, textvariable=searchName)
nameEntered.grid(column=0, row=1, pady=10) 

# Modify adding a Label for template searching
blacklistLbl = ttk.Label(win, text="Choose a search for blacklisted words:")
blacklistLbl.grid(column=0,row=3) 

# Modify adding a Label for CREATOR
credentialLbl = ttk.Label(win, text="Software Created By\n" + "Muhammad Suhaib",)
credentialLbl.grid(column=2, row=1)#specifiy exaclty out of grid where to place button
credentialLbl.place(x=430,y=1,height=35,width=113)

# Using a scrolled Text control for tweets
scrolW = 65
scrolH = 30
tweetBox = scrolledtext.ScrolledText(win, width=scrolW, height=scrolH, wrap=tk.WORD)
tweetBox.grid(column=0, columnspan=3)

counter = 0
tweetFile = '50-tweets_inc_swears.json'    #declared variable for tweet file

#performing a seach of what is in the tweets.
def search():
    userSearch = searchName.get() 
    searchBtn.configure(text="Searching..." + userSearch)
    with open(tweetFile) as data_file:
        for row in data_file:
           data = json.loads(row)
           tweet = data['text']
           if (userSearch == ""):
               counter = 1
           elif str(userSearch).lower() or str(userSearch).upper() in tweet:
               outputScroll = ("\n"+".................Searching................." +"\n" + tweet + "\n...........................................")
               tweetBox.insert(tk.INSERT, outputScroll)
           elif not str(userSearch).lower() or not str(userSearch).upper() or not str(userSearch) in tweet:
               counter = 2   
#           elif str(userSearch) not in tweet:
#               counter = 2
        counters(counter)
        
def regularExpressionSearch():
    regex = re.compile(searchName.get())
    with open(tweetFile, 'r') as data_file:
        for l in data_file: #every line in data file
            data = json.loads(l)
            tweet = data['text']
            result = regex.findall(tweet)
            if (result):  
                tweetBox.insert(tk.INSERT, "\n-----------------------------------------------------------"+"\nData Found:" +"\n"+ tweet)
                for r in result:
                    tweetBox.insert(tk.INSERT, "\nKeyword was: " + r +"\n-----------------------------------------------------------" )
    
#Mapping ComboBox to blacklisted words for template searching
def templateSearch():
    tempSearchBtn.configure(text="Searching "+ bListComboBox.get())
    vC = ["kill","bomb","die","shoot","shot","violence","stab","knife","attack", "punched", "assualt", "robbery", "homocide", "wounding", "domestic violence", "mugging", "murder", "murdered", "manslaughter", "infanticide", "sexual assault", "rape", "drink" + "driving", "drug" + "driving", "GBH", "possession"+ "weapon", "harassment","firearm", "stalking", "vandalism","vandalised","vandal","arson","graffiti","deliberate damage","malicious","set fire","criminal damage","destroyed","damaged","keying"+"car","reckless"]
    aC = ["theft", "burglary", "vehicle"+"stolen", "nicked", "robbery", "breaking"+"entering","bike"+"stolen"]
    fF = ["fraud","forgery","identity theft","bank card"+"stolen","false accounting","bankruptcy","credit card","debit card","bank details"+"stolen","fraudulent"]
    rR = ["racial","racial"+"abuse","racist","hate crime","religion","hatred","religious","aggravated"]
    dO = ["drugs","drug","possession","intent to supply","cannabis","class a","class b","class c","drug trafficking","heroin","cocaine","LSD","amphetamine","ketamine"]
    with open (tweetFile) as data_file:
        for row in data_file:
            data = json.loads(row)
            tweet = data["text"]
            if bListComboBox.get() == ("Violence & Criminal"):
                for v in range(len(vC)):
                        if vC[v] in tweet:
                            outputScroll = ("\n"+".................Search Results.................\n" + tweet + "\n")
                            tweetBox.insert(tk.INSERT, outputScroll)
            elif bListComboBox.get() == ("Acquisitive Crime"):                
                for a in range(len(aC)):
                        if aC[a] in tweet:
                            outputScroll = ("\n"+".................Search Results.................\n" + tweet + "\n")
                            tweetBox.insert(tk.INSERT, outputScroll)
            elif bListComboBox.get() == ("Fraud & Forgery"):
                for f in range(len(fF)):
                        if fF[f] in tweet:
                            outputScroll = ("\n"+".................Search Results.................\n" + tweet + "\n")
                            tweetBox.insert(tk.INSERT, outputScroll)
            elif bListComboBox.get() == ("Racial & Religious"):
                for r in range(len(rR)):
                        if rR[r] in tweet:
                            outputScroll = ("\n"+".................Search Results.................\n" + tweet + "\n")
                            tweetBox.insert(tk.INSERT, outputScroll)
            elif bListComboBox.get() == ("Drug Offences"):
                for d in range(len(dO)):
                        if dO[d] in tweet:
                            outputScroll = ("\n"+".................Search Results.................\n" + tweet + "\n")
                            tweetBox.insert(tk.INSERT, outputScroll)
    if bListComboBox.get() == ("**Please Select**"):
                tweetBox.insert(tk.INSERT, "\nPlease choose an option")
    
#loading json as string text button function
def loadTweetJson():
    map_osm = folium.Map(location=[53.472328361821766,-2.23959064483645], zoom_start=13)
    with open(tweetFile) as data_file:    #with statement handles exceptions and cleans up code.
        for row in data_file: 
            data = json.loads(row)
            tweet = data["text"].replace("'","\\'")
            longitude = data['geoLocation']['longitude']
            latitude = data['geoLocation']['latitude']
            stringToScroll = "\n........................................." + "\nDate: " + data['createdAt']['$date'] + " \nlatitude: " + str(data['geoLocation']['latitude']) + " \nlongitude: " + str(data['geoLocation']['longitude']) + "\nTweet Text: " + tweet + "\nPlace Full Name: "+data['place']['fullName'] + "\n .............. Next Record .............."
            folium.Marker([latitude,longitude], popup=data['text'], icon=folium.Icon(color='green')).add_to(map_osm)
            tweetBox.insert(tk.INSERT, stringToScroll)
            map_osm.save('Regular Map.html')
    
def openMap():
    map_osm = folium.Map(location=[53.472328361821766,-2.23959064483645], zoom_start=13)
    with open(tweetFile) as data_file:
        for row in data_file: 
            data = json.loads(row)
            tweet = data["text"].replace("'","\\'")
            longitude = data['geoLocation']['longitude']
            latitude = data['geoLocation']['latitude']
            folium.Marker([latitude,longitude], popup=tweet, icon=folium.Icon(color='green')).add_to(map_osm)
    map_osm.save('Regular Map.html')
    filename = 'file://'+os.getcwd()+'/' + 'Regular Map.html'
    webbrowser.open_new_tab(filename)    

#method for clearing text form the scrollable textbox, adding convenience to user to search and load tweets     
def clearText():
    tweetBox.delete("1.0", "end")
    
#Used in conjunction with global variable counter for events on types of ways userSearch does not match.             
def counters(counter):     
        #get out of loop to stop repeated statements for every tweet
     if (counter == 1): 
         tweetBox.insert(tk.INSERT, "\nYou must input in the search bar to see results\n")
         counter = 0
     if (counter == 2):
         tweetBox.insert(tk.INSERT, "\nSorry no matching search results!\nNOTE: Results are Case Sensitive\n")
         counter = 0        
 
# Adding search Button
searchBtn = ttk.Button(win, text="Search", command=search) #creating and linking button to search function
searchBtn.place(x=225,y=27,height=25,width=90) #specifiy exaclty out of grid where to place button

# Adding regular expression search Button
regexSearchBtn = ttk.Button(win, text="RegEx Search", command=regularExpressionSearch) #creating and linking button to regularExpressionSearch function
regexSearchBtn.place(x=325,y=27,height=25,width=90) #specifiy exaclty out of grid where to place button

# Adding template search Button
tempSearchBtn = ttk.Button(win, text="Template Search", command=templateSearch) #creating and linking button to templateSearch function
tempSearchBtn.grid(column=2, row=3) #alligns button to grid 

#creating the combobox widget for drop down menu
bListBox = tk.StringVar()
bListComboBox = ttk.Combobox(win, width=20, textvariable=bListBox)
bListComboBox['values'] = ("**Please Select**","Violence & Criminal", "Acquisitive Crime", "Fraud & Forgery", "Racial & Religious","Drug Offences")
bListComboBox.grid(column=1, row=3) #alligns combobox to grid
bListComboBox.current(0) #specifies to start with the first data set in the comboBox

# Adding JSON details Button
loadingJsonBtn = ttk.Button(win, text=" Load Tweets from JSON", command=loadTweetJson) #creating and linking button to loadTweetJson function
loadingJsonBtn.place(x=200,y=569,height=25,width=150) #specifiy exaclty out of grid where to place button

# Adding clear Button
clearBtn = ttk.Button(win, text="Clear", command=clearText) #creating and linking button to clearText function
clearBtn.place(x=380,y=569,height=25,width=90) #specifiy exaclty out of grid where to place button

#Adding opening map button
mapOpen = ttk.Button(win, text="Show Map of tweets", command=openMap) #creating and linking button to openMap function
mapOpen.grid(column=0, row=8) #alligns button to grid
#tempSearchBtn.place(x=180,y=562,height=25,width=90)

#enabling button state after textbox is not empty
#searchBtn.configure(state='disabled')

nameEntered.focus() # Place cursor into name Entry
win.mainloop() # Start GUI
