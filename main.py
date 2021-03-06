# ----------------------------------------------------
# Created by Möhrchen [Thilo] and OrangeChef [Kameron]
#     and the help of Acute with the Http-Requests    
#           ©2022 - All Rights Reserved
# ----------------------------------------------------

import srcomapi, srcomapi.datatypes as dt
import discord
from discord.ext import tasks, commands
from discord.utils import get
from webserver import keep_alive
import os
import random
from datetime import datetime
import calendar

#=========Functions=========

#This function returns a nice looking Time-String
def ConvertStringToTime(strPar):
    parFloat = float(strPar)
    rest = round(parFloat % 60, 2)
    minutes = int(round((parFloat - rest) / 60, 0))
    hours = 0
    returnString0 = ""
    returnString1 = ""
    returnString2 = ""
    if minutes > 59:
        while minutes > 59:
            minutes -= 60
            hours += 1
        returnString0 = str(hours) + ":"

    if minutes < 10: returnString1 = "0" + str(minutes)
    else: returnString1 = "" + str(minutes)
    
    if rest < 10: returnString2 = ":0" + str(rest)
    else: returnString2 = ":" + str(rest)
        
    if rest * 100 % 10 == 0: return (returnString0 + returnString1 + returnString2 + "00")
    else: return (returnString0 + returnString1 + returnString2 + "0")

api = srcomapi.SpeedrunCom(); api.debug = 1

#CreateCustomID
def CreateTicketID(totalTickets):

    letterArray = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O',
    'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '8', '9', '0']
    letterArray2 = ['!', '@', '#', '$', '%', '?', '&', '*', '(', ')']
    numberArray = str(totalTickets)

    randomFactor = random.randint(0, 62)
    idReturn = letterArray[randomFactor]

    for n in numberArray:
        idReturn = idReturn + letterArray2[int(n)]

    randomFactor = random.randint(0, 62)
    idReturn = idReturn + letterArray[randomFactor]


    return idReturn

#ReverseCustomID
def ReverseTicketID(strID):
    forCount = 0
    letterArray2 = ['!', '@', '#', '$', '%', '?', '&', '*', '(', ')']
    returnStr = ''
    for char in strID:
        if forCount != 0 and forCount != len(strID) - 1:
            returnStr = returnStr + str(letterArray2.index(char))
        forCount += 1
    
    return int(returnStr)
    

def TestForAdvancedSpeedrunCommand(messagePar, checkPar):
    #if checkPar in messagePar: return True
    if checkPar.lower() in messagePar.lower(): return True
    
    return False
    


#=========Important Variables=========



listLimit = 30

timeArray = [None] * 1000 #When the Leaderboard gets over 1000 entrys we need to edit this value
webLinkArray = [None] * 1000 
nameArray = [None] * 1000

howMuchData = 2
dcData = [None] * howMuchData
dcData[1] = 'bot-commands'

prefix = "m!"
client = commands.Bot(command_prefix = 'm!')

watchListChannelId = 963122498273157150     #TestDC=964456821182070784   RealDC=963122498273157150

ticketChannelId = 966279655344701449         #TestDC=966237739223760906   RealDC=966279655344701449

birthdayChannelId = 980054278272090112      #TestDC=980015311199813683   RealDC=980054278272090112
                            
activeGuildId = 916534358943342653           #TestDC=964450998452125697   RealDC=916534358943342653

bannedWords = ["nigga", "nigger"]
warningWords = ["retard", "retarded", "penis", "vagina"]

nicePeopleArray = ["FlippyDolphin#1651", "Meister Möhre#1623", "JonasTyroller#7200", "OrangeChef#4553", "TheOrangeWhale#8667", "Zetas2#6270", "Ezra3#0928", "Doginator#5868", "enmy#0745", "Martinuz_64#7736"]
godDamnNicePeopleArray = ["FlippyDolphin#1651", "Meister Möhre#1623", "JonasTyroller#7200", "OrangeChef#4553"]


categoryChoices = ["Any% NMG", "Any%", "Alt Ending", "All Collectibles", "No Shortcuts"]
bossChoices = ["Splitty", "Mr D.A.N.C.E", "Mama Squid", "Helpy", "Bartender", "Squid 1", "Squid 2"]
difficultyChoices = ["IE", "EE", "VE", "Easy"]
typingCategoryChoices = ["Any%NMG", "Any%", "AltEnding", "AllCollectibles", "NoShortcuts"]
typingBossChoices = ["Splitty", "MrDance", "MamaSquid", "Helpy", "Bartender", "Squid1", "Squid2"]
typingChapterChoices = ["ChapterA", "ChapterB", "ChapterC", "ChapterD", "ChapterE"]
typingOtherExtChoices = ["ChapterRelay", "Iaf", "DoubleTime", "Death%", "BlockMassacre", "MinimumKills"]

listOfSpeedyTicketWriter = [None] * 2

listOfBotStatus = ['Will You Snail?', 'm!help', 'm!leaderboard', 'm!ticket']
activeBotStatus = 0

#=========Discord Client=========



class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.Change_Values.start()
        self.Change_Status.start()
    #This is a loop which update every 300 seconds the values from the array
    @tasks.loop(seconds=30.0)
    async def Change_Status(self):
        global activeBotStatus
        await self.change_presence(activity=discord.Game(name=listOfBotStatus[activeBotStatus]))
        if activeBotStatus < len(listOfBotStatus) - 1: activeBotStatus += 1
        else: activeBotStatus = 0
            

    @tasks.loop(seconds=300.0)
    async def Change_Values(self):      
        listOfSpeedyTicketWriter.clear()
        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        print(unixtime)
        bdays = open("Birthdays.txt", "r")
        bDaysRL = bdays.readlines()
        bdays.close()
        for ln in bDaysRL:
            lnSplit = ln.split('~')
            if int(unixtime) > (int(lnSplit[2]) + (int(lnSplit[3]) * 31556926)):
                bDayChannel = client.get_channel(birthdayChannelId)
                tu = await client.fetch_user(int(lnSplit[0]))
                embed = discord.Embed(
                title = 'Happy Birthday!',
                description = str('Today is ' + tu.name + '\'s birthday! Everybody wish ' + lnSplit[1].split('<')[1] + ' a great day, and good luck with future speedruns! :)'),
                colour = discord.Colour.red()
                )
                embed.set_image(url='https://thumbs.dreamstime.com/b/happy-birthday-candles-against-black-background-50258013.jpg')
                theGuild = client.get_guild(activeGuildId)
                theRole = discord.utils.get(theGuild.roles,name="Birthday Announcements")
                await bDayChannel.send(tu.mention + " " + theRole.mention, embed=embed)

                bdaysW = open("Birthdays.txt", "w")
                for ln2 in bDaysRL:
                    if ln2 != ln:
                        bdaysW.write(ln2)
                    else:
                        bdaysW.write(lnSplit[0] + "~" + lnSplit[1] + "~" + lnSplit[2] + "~" + str((int(lnSplit[3]) + 1)) + "\n")

                bdaysW.close()
                return
        print('300s over!')
        return
        #Getting the Leaderboard -->
        searchApi = api.search(srcomapi.datatypes.Game, {"name": "Will You Snail?"})
        game = searchApi[0]
        cates = game.categories
        #runs = game.categories[0].records[0].runs #Currently not used
        sms_runs = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(game.id, game.categories[0].id)))
        
        #Write every score and name into the arrays --> 
        a = 0
        a2 = 0
        global eventOutputString
        eventOutputString = ['```'] * 10
        for r in sms_runs.runs:
            try:
                run = r["run"]
                webLinkArray[a] = run.weblink
                time = ConvertStringToTime(float(run.times["primary_t"]))
                playerTag = str(run.players[0])
                playerString = str(playerTag.replace('<User "', '')).replace('">', '')
                timeArray[a] = time
                dateString = str(run.submitted)
                year = dateString[0] + dateString[1] + dateString[2] + dateString[3]
                month = dateString[5] + dateString[6]
                day = dateString[8] + dateString[9]
                if year == '2022' and month == '04':
                    if int(day) <= 19 and int(day) >= 9:
                        if len(eventOutputString[a2]) > 1800:
                            eventOutputString[a2] = eventOutputString[a2] + '```'
                            a2 += 1 
                        eventOutputString[a2] = eventOutputString[a2] + playerString + ": " + str(year) + "-" + str(month) + "-" + str(day) + "\n" #+ "```" + " --> " + str(run.weblink) + "\n"
              
                nameArray[a] = playerString
                a += 1
            except:
                print('An error with a http-request!')
                
        global maxLeaderboardIndex
        eventOutputString[a2] = eventOutputString[a2] + '```'
        maxLeaderboardIndex = a - 1
        print("Loop restarted...")
  
    async def on_message(self, message):
        prefix = 'm!'
        messageStr = '{0.content}'.format(message)

        if len(messageStr) < 2: return
        


        #===Check for banned Words===

        for bw in bannedWords:
            if bw.lower() in messageStr.lower():
                if message.author.bot: return
                watchListChannel = client.get_channel(watchListChannelId)
                await message.delete()
                await message.author.send("You have been banned from Will You Speedrun? for using a banned word.")
                await message.channel.send("The previous message was deleted because a banned word was used!")
                await watchListChannel.send("The banned word '" + bw + "' was used by " + str(message.author) + " in the channel #" + str(message.channel.name) + ".\nMessage: " + messageStr)
                try: await message.guild.get_member(message.author.id).ban() 
                except: await message.author.ban() 
                await watchListChannel.send("Succesfully banned " + str(message.author) + ".")
                return
            
        for ww in warningWords:    
            if ww.lower() in messageStr.lower():
                if message.author.bot: return
                watchListChannel = client.get_channel(watchListChannelId)
                await message.delete()
                await message.author.send("You used the banned word '" + ww + "'. Please don't use it again!'")
                await message.channel.send("The previous message was deleted because a banned word was used!")
                await watchListChannel.send("The banned word '" + ww + "' was used by " + str(message.author) + " in the channel #" + str(message.channel.name) + ".\nMessage: " + messageStr)
                await watchListChannel.send("Succesfully warned " + str(message.author) + ".")
                return



        #===Clear Command (m!clear X)===



        if str(prefix + 'clear') in messageStr.lower():
            if str(message.author) not in godDamnNicePeopleArray: return 
            try:
                async for m in message.channel.history(limit=1 + int(messageStr.replace(str(prefix + 'clear '), ''))):
                    await m.delete()
                return
            except:
                print('m!clear Error!')



        #===Reaction Command (m!reaction)===


        
        if str(prefix + 'reaction') in messageStr.lower(): #If a m!Reaction is in the message, then he has to delete the emoji and react with it on the last message
            if str(message.author) not in godDamnNicePeopleArray: return #when the author isn't included in the Array nothing happens
            a = 0
            tempData = [''] * 3
            async for data in message.channel.history(limit=3):
                tempData[a] = str(data.content)
                await data.delete()
                a += 1

            roleFile = open("Roles.txt", "r")
            roleFileRL = roleFile.readlines()
            roleFile.close()

            theNewMessage = await message.channel.send(tempData[0].replace(prefix + 'reaction', ''))

            roleFileW = open("Roles.txt", "w")
            for ln in roleFileRL:
                roleFileW.write(ln)
            roleFileW.write(str(tempData[2]) + "~" + str(theNewMessage.id) + "\n")

            try:
                await theNewMessage.add_reaction(str(tempData[1]))
            except:
                print("Entered a false Reaction")




      
        if messageStr[0] != 'm' or messageStr[1] != '!' :
            if messageStr[0] == 'M' and messageStr[1] == '!':
                prefix = 'M!'
            else:
                return #when no prefix in a message is detected nothing should happen
        
        if str(message.author) not in nicePeopleArray and not str(message.channel) == str(dcData[1]): return #when the author isn't included in the Array nothing happens


          
        #===Speedrunning Command (m!src)===


      
        if str(prefix + 'src') in messageStr: 

            await message.channel.send("This command is outdated: use m!lb instead!")    
            return

            try: 
                if '-' in messageStr.replace(str(prefix + 'src '), ''):                    # First Command starts here - m!src X-Y
                    numberArray = messageStr.replace(str(prefix + 'src '), '').split('-')
                    
                    #Check if the Leaderboard has that much entrys
                    if int(numberArray[1]) > maxLeaderboardIndex:
                        await message.channel.send("The numbers are too large for the leaderboard!")
                        return
                    
                    #Check if that what the Bot displays is only "Leaderboard:"                  
                    if int(numberArray[1]) + 1 - int(numberArray[0]) <= 0:
                        await message.channel.send("Leaderboard index should be 1 or higher!")
                        return
                    
                    if int(numberArray[1]) + 1 - int(numberArray[0]) <= listLimit: #Check if the value is too large 
                        #Combine them into one message -->
                        completeString = "__Leaderboard:__ \n"
                        for p in range(int(numberArray[0]), int(numberArray[1]) + 1):
                            sentenceString =  str(p) + ". **" + str(timeArray[p - 1]) + "** by **" + str(nameArray[p - 1] + "**")
                            completeString = completeString + sentenceString + "\n"
                        await message.channel.send(completeString)
                    else:
                        await message.channel.send("Leaderboard index should be 30 or lower!")
                    
                else:                                                                    # Second Command starts here - m!src X
                    arrayCount = int(messageStr.replace(str(prefix + 'src '), ''))
                    
                    if arrayCount <= listLimit: #Check if the value is too large 
                        completeString = "__Leaderboard:__ \n"
                        
                        if arrayCount == 0: #EASTER EGG 1 (A request from FlippyDolphin)
                            await message.channel.send("The Leaderboard doesn't exist anymore! :(")
                            return
                        #Combine them into one message -->    
                        for p in range(1, arrayCount + 1):
                            sentenceString =  str(p) + ". **" + str(timeArray[p - 1]) + "** by **" + str(nameArray[p - 1] + "**")
                            completeString = completeString + sentenceString + "\n"
                        await message.channel.send(completeString)
                    else:
                        await message.channel.send("Leaderboard index should be 30 or lower!")
            except:
                await message.channel.send("Leaderboard index should be a valid number!")


              
        #===Event Command (m!eventruns)===



        if str(prefix + 'eventruns') in messageStr or str(prefix + 'Eventruns') in messageStr: 
            await message.channel.send("This event is over, so this command has been removed!")    
            return

            for m in eventOutputString:
                if m != '```':
                    await message.channel.send(m)


          
        #===Moderator Command (m!GetData)===


              
        if str(prefix + 'GetData') in messageStr: 
            a = 0
            async for data in message.channel.history(limit=howMuchData):
                dcData[a] = str(data.content)
                a += 1
                
            await message.channel.send("Command channel is assigned as: #" + str(dcData[1]))
            


        #===Zetas Command (m!Zetas)===

        #if str(prefix + 'zetas') in messageStr.lower(): 
        #    theGuild = message.guild 
        #    theRole = discord.utils.get(theGuild.roles,name=messageStr.replace(prefix + 'zetas', ''))
        #    message.channel.send("That should be the mention... " + theRole.mention)
        #    return

        #===Help Command (m!Help)==



        if TestForAdvancedSpeedrunCommand(messageStr, str(prefix + 'help')): 
            embed = discord.Embed(
            title = 'Help',
            description = 'This is a list of the commands: \n ',
            colour = discord.Colour.blue()
            )
            #embed.add_field(name='m!src X', value='Shows top X runs.', inline=True)
            #embed.add_field(name='m!src X-Y', value='Shows runs X through Y.\n', inline=True)
            #embed.add_field(name='m!eventruns', value='Shows a list of all runs submitted during the event. \n', inline=True)
            embed.add_field(name='m!lb category difficulty X', value='Shows top X runs from \n the category in the difficulty.', inline=False)
            embed.add_field(name='m!lb category difficulty X-Y', value='Shows runs X through Y from \n the category in the difficulty.', inline=True)
            embed.add_field(name='m!ticket', value='Creates a ticket.', inline=False)
            embed.add_field(name='m!removeticket ID', value='Removes a ticket.', inline=True)
            embed.add_field(name='m!getticket ID', value='Shows the status, the author and the message from a ticket.', inline=False)
            embed.set_thumbnail(url='https://www.speedrun.com/themeasset/2woqj208/logo?v=ae9623c')
            await message.channel.send(embed=embed)



        #===Speedrun Command Advanced (m!category difficulty X) / (m!catgory difficulty X-Y)



        if TestForAdvancedSpeedrunCommand(messageStr, prefix + 'lb') or TestForAdvancedSpeedrunCommand(messageStr, prefix + 'leaderboard'):

                                                                  #Try to get the Category and the Difficulty -->

            tempCategory = None #Is a string
        
            for cateCommand in typingCategoryChoices:
                if TestForAdvancedSpeedrunCommand(messageStr, cateCommand) and tempCategory == None:
                    tempCategory = categoryChoices[typingCategoryChoices.index(cateCommand)]
        
            typeOfCategory = 'Category' #Default Value = Category
            minusCommandSplitter = 0


            if tempCategory == None: #Test for ILs (Chapters)
                for chapterCommand in typingChapterChoices:
                    if TestForAdvancedSpeedrunCommand(messageStr, chapterCommand) and tempCategory == None:
                        tempCategory = chapterCommand
                        typeOfCategory = 'Chapter'

            if tempCategory == None: #Test for Other Extensions
                for otherExtCommand in typingOtherExtChoices:
                    if TestForAdvancedSpeedrunCommand(messageStr, otherExtCommand) and tempCategory == None:
                        tempCategory = otherExtCommand
                        typeOfCategory = 'OtherExtension'
                     
            if tempCategory == None: #It should be a Boss, 100% or a typo
                if '100%' in messageStr:  #It's 100%
                    tempCategory = '100%'
                    typeOfCategory = '100%'
                    minusCommandSplitter = 1
                else:
                    for bossCommand in typingBossChoices:
                        if TestForAdvancedSpeedrunCommand(messageStr, bossCommand) and tempCategory == None:
                            tempCategory = bossChoices[typingBossChoices.index(bossCommand)]
                            typeOfCategory = 'Boss'
                
                
            tempDifficulty = None #Is an integer
        
            if typeOfCategory != '100%':
                for diffCommand in difficultyChoices:
                    if TestForAdvancedSpeedrunCommand(messageStr, diffCommand) and tempDifficulty == None:
                        tempDifficulty = difficultyChoices.index(diffCommand)
          
            if tempCategory == None: 
                await message.channel.send("Please specify the catagory!")
                return

            await message.channel.send("Loading...")
            theLeaderboard = None
            cateString = ""
            searchApi = api.search(srcomapi.datatypes.Game, {"name": "Will You Snail?"})
            game = searchApi[0]
            cates = game.categories  
            levels = game.levels
            try:                                                    #Now try to get the Leaderboard from the right category -->
                if typeOfCategory == 'Category':
                    categoryInt = categoryChoices.index(tempCategory)
                    if categoryInt == 4: categoryInt = 10
                    cate = cates[categoryInt]
                    difficultyVar = cate.variables[0] 
                    cateString = "leaderboards/{}/category/{}?var-{}={}".format(game.id, cate.id, difficultyVar.id, list(difficultyVar.data["values"]["choices"].keys())[tempDifficulty])
                elif typeOfCategory == 'Boss':
                    cate = cates[9]
                    bossVar = cate.variables[1]
                    difficultyVar = cate.variables[0]
                    cateString = "leaderboards/{}/category/{}?var-{}={}&var-{}={}".format(game.id, cate.id, difficultyVar.id, list(difficultyVar.data["values"]["choices"].keys())[tempDifficulty], bossVar.id, list(bossVar.data["values"]["choices"].keys())[bossChoices.index(tempCategory)])
                elif typeOfCategory == '100%':
                    cate = cates[8]
                    cateString = "leaderboards/{}/category/{}".format(game.id, cate.id)
                elif typeOfCategory == 'Chapter':
                    difficultyVar = cates[tempDifficulty+4]
                    level = levels[typingChapterChoices.index(tempCategory)]  
                    cateVar = difficultyVar.variables[0]
                    cateString = "leaderboards/{}/level/{}/{}?var-{}={}".format(game.id, level.id, difficultyVar.id, cateVar.id, list(cateVar.data["values"]["choices"].keys())[0]) #This number at the end controls Any% or AllPuzzles
                elif typeOfCategory == 'OtherExtension':
                    game3 = searchApi[3]
                    cates3 = game3.categories
                    if typingOtherExtChoices.index(tempCategory) == 1:
                        iafArray = ["2", "25", "50", "75", "100", "1000"]
                        iafIndex = ""
                        for iafValue in iafArray:
                            if typingOtherExtChoices[1].lower() + iafValue in messageStr.lower():
                                iafIndex = iafValue
                        cate = cates3[1]
                        levelVar = cate.variables[0]
                        cateString = "leaderboards/{}/category/{}?var-{}={}".format(game3.id, cate.id, levelVar.id, list(levelVar.data["values"]["choices"].keys())[iafArray.index(iafIndex)])
                        minusCommandSplitter = 1
                    elif typingOtherExtChoices.index(tempCategory) == 3:
                        cate = cates3[3]
                        cateString = "leaderboards/{}/category/{}".format(game3.id, cate.id)
                        minusCommandSplitter = 1
                    else: 
                        cate = cates3[typingOtherExtChoices.index(tempCategory)]
                        difficultyVar = cate.variables[0]
                        cateString = "leaderboards/{}/category/{}?var-{}={}".format(game3.id, cate.id, difficultyVar.id, list(difficultyVar.data["values"]["choices"].keys())[tempDifficulty])

                theLeaderboard = dt.Leaderboard(api, data=api.get(cateString))

                                                                    #Try to display the Leaderboard --> 

                if minusCommandSplitter == 1 and tempDifficulty != None:
                    await message.channel.send("This category hasn't a difficulty!")
                    return

                try:
                    tempNumbers = messageStr.replace(prefix, '').split(' ')[3 - minusCommandSplitter] 
                    if '-' in messageStr: #Command option 1: X-Y
                        try:
                            tempNumber1 = int(tempNumbers.split('-')[0])
                            tempNumber2 = int(tempNumbers.split('-')[1])
                        except Exception as e:
                            await message.channel.send("Please enter a valid number!")
                            return

                        if tempNumber2 > len(theLeaderboard.runs):
                            if len(theLeaderboard.runs) == 1:
                                await message.channel.send("This Leaderboard has only " + str(len(theLeaderboard.runs)) +  " entry!")
                            else:
                                await message.channel.send("This Leaderboard has only " + str(len(theLeaderboard.runs)) +  " entries!")
                            return
                    
                        if tempNumber2 - tempNumber1 >= 30:
                            await message.channel.send("Leaderboard index should be 30 or lower!")
                            return
                        elif tempNumber2 - tempNumber1 < 0:
                            await message.channel.send("Leaderboard index should be 1 or higher!")
                            return
                    
                        _complString = "The " + str(tempCategory) + " Leaderboard: \n"
                        for i in range(tempNumber1, tempNumber2 + 1):
                            _names = theLeaderboard.runs[i - 1]['run'].players
                            _time = ConvertStringToTime(float(theLeaderboard.runs[i - 1]['run'].times["primary_t"]))
                            _complString = _complString + str(i) + ". **" + str(_time) + "** by **" + str(_names[0].name) + "**"
                            arrayCount = 0
                            if len(_names) > 1:
                                for pla in _names:
                                    if arrayCount > 0:
                                        _complString = _complString + " and **" + pla.name + "**"
                                    arrayCount += 1

                            _complString = _complString + "\n"

                        
                        await message.channel.send(_complString)   
                        
                    else:               #Command option 2: X
                        try:
                            tempNumber1 = int(tempNumbers)
                        except Exception as e:
                            await message.channel.send("Please enter a valid number!")
                            return

                        if tempNumber1 > len(theLeaderboard.runs):
                            if len(theLeaderboard.runs) == 1:
                                await message.channel.send("This Leaderboard has only " + str(len(theLeaderboard.runs)) +  " entry!")
                            else:
                                await message.channel.send("This Leaderboard has only " + str(len(theLeaderboard.runs)) +  " entries!")
                            return
                
                        if tempNumber1 > 30:
                            await message.channel.send("Leaderboard index should be 30 or lower!")
                            return
                        elif tempNumber1 == 0:
                            await message.channel.send("The Leaderboard doesn't exist anymore! :(") #FlippyDolphin's Easter Egg
                            return 
                    
                        _complString = "The " + str(tempCategory) + " Leaderboard: \n"
                        for i in range(1, tempNumber1 + 1):
                            _names = theLeaderboard.runs[i - 1]['run'].players
                            _time = ConvertStringToTime(float(theLeaderboard.runs[i - 1]['run'].times["primary_t"]))
                            _complString = _complString + str(i) + ". **" + str(_time) + "** by **" + str(_names[0].name) + "**"
                            arrayCount = 0
                            if len(_names) > 1:
                                for pla in _names:
                                    if arrayCount > 0:
                                        _complString = _complString + " and **" + pla.name + "**"
                                    arrayCount += 1

                            _complString = _complString + "\n"
                    
                        await message.channel.send(_complString)   
                except Exception as e:
                    await message.channel.send("Please enter the number of runs you'd like display!")
            except Exception as e:
                await message.channel.send("Please specify the difficulty!")
            a = 0
            async for data in message.channel.history(limit=2):
                if a == 1:
                    await data.delete()
                a += 1
           


    #===Mod Command (m!setstatus)===



        if TestForAdvancedSpeedrunCommand(messageStr, prefix + 'setstatus'):
            if str(message.author) in nicePeopleArray:
                try:
                    arguments = messageStr.replace(prefix + 'setstatus ', '').split()
                    newStatus = ''
                    whichId = arguments[0]
                    for argu in arguments:
                        if argu != whichId: 
                            newStatus = newStatus + argu + " "

                    txtFile = open("TicketStatus.txt","r")
                    txtFileRl = txtFile.readlines()
                    txtFile.close()

                    rvrsedId = ReverseTicketID(whichId)

                    newTxtString = ''
                    for line in txtFileRl:
                        if whichId == line.split(':')[0]:
                            newTxtString = newTxtString + str(whichId) + ": ~" + str(newStatus) + "\n"
                        else:
                            newTxtString = newTxtString + line
                       

                    txtWriteFile = open("TicketStatus.txt","w")
                    txtWriteFile.write(newTxtString)
                    txtWriteFile.close()

                    await message.channel.send("The Status of ticket '" + str(whichId) + "' has been changed to '" + str(newStatus) + "'.") #should i start it now? sure
                except:
                    await message.channel.send("Something went wrong! :(")



    #===Ticket Create===



        if TestForAdvancedSpeedrunCommand(messageStr, prefix + 'ticket'):
            if str(message.author) not in listOfSpeedyTicketWriter:
                currentTickets = ""
                currentIdCount = 0
                shouldChangeIdCount = True
                try:
                    txtr = open("Tickets.txt","r")
                    rl = txtr.readlines()
                    for line in rl:
                        currentTickets = currentTickets + line
                    txtr.close()
                except:
                    print("Currently there isn't a txt-file, so I create a file for you :)")
                txtw = open("Tickets.txt","w")
                txtr2 = open("TicketsHistory.txt","r")
                txt2rl = txtr2.readlines()
                currentIdCount = round(len(txt2rl) / 2)
                ticketHistory = ''
                for line in txt2rl:
                    ticketHistory = ticketHistory + line
                txtr2.close()
                txtr3 = open("TicketStatus.txt","r")
                txt3rl = txtr3.readlines()
                ticketStatusHistory = ''
                for line in txt3rl:
                    ticketStatusHistory = ticketStatusHistory + line
                txtr3.close()
                txtw2 = open("TicketsHistory.txt","w")
                txtw3 = open("TicketStatus.txt","w")
                txtw.write(currentTickets)
                txtw2.write(ticketHistory)
                txtw3.write(ticketStatusHistory)            
                theCurrentId = CreateTicketID(currentIdCount)
                try:
                    txtw.write(str(message.author) + ": " + messageStr.replace(prefix + 'ticket', '') + "\n")
                    txtw2.write(str(message.author) + ": " + messageStr.replace(prefix + 'ticket', '') + "\n")
                    txtw3.write(str(theCurrentId) + ": ~Unseen \n") #Statuses are Unseen, Seen, In Progress and Implemented
                except:
                    await message.channel.send("Your message contains characters that could not be processed!")
                    return
                txtw.write("------------------------------------------------------------------------------------\n")
                txtw2.write("------------------------------------------------------------------------------------\n")
                #txtw3.write("------------------------------------------------------------------------------------\n")
                txtw.close()
                txtw2.close()
                txtw3.close()
                listOfSpeedyTicketWriter.append(str(message.author)) #await message.channel.send(str(message.author.mention) + " Thank you for creating a ticket! :)  (ID: " + theCurrentId + ")")              
                embed = discord.Embed(
                    title = 'Ticket from ' + str(message.author.name),
                    description = '',
                    colour = discord.Colour.blue()
                )
                embed.add_field(name='ID: ', value=theCurrentId, inline=True)
                embed.add_field(name='Message: ', value=messageStr.replace(prefix + 'ticket', ''), inline=False)
                embed.set_thumbnail(url='https://www.speedrun.com/themeasset/2woqj208/logo?v=ae9623c')
                theTicketChannel = client.get_channel(ticketChannelId)
                await theTicketChannel.send(message.author.mention, embed=embed)

                lm = theTicketChannel.last_message

                await lm.add_reaction(get(message.guild.emojis, name='Sr_5InfEasy'))
                await lm.add_reaction(get(message.guild.emojis, name='Sr_1Down'))

                txtMessageIDs = open("TicketMessageIds.txt","r")
                txtMessageIDsRl = txtMessageIDs.readlines()
                txtMessageIDs.close()
                allIds = ''
                for ln in txtMessageIDsRl:
                    allIds = allIds + ln
                allIds = allIds + str(theTicketChannel.last_message_id) + "\n"
                txtMessageIdsW = open("TicketMessageIds.txt","w")
                txtMessageIdsW.write(allIds)
                txtMessageIdsW.close()
                await message.author.send("Thank you for creating a ticket! :)  (ID: " + theCurrentId + ")", embed=embed)
                await message.delete()
                return
            else:
                await message.channel.send("Please slow down with writing tickets! Try again in a few minutes!")


            return

        if TestForAdvancedSpeedrunCommand(messageStr, prefix + 'removeticket'):
            theRemoveId = messageStr.replace(prefix + 'removeticket ', '')
            rti = 0
            try:
                rti = ReverseTicketID(theRemoveId)
            except:
                await message.channel.send("This ID doesn't exist!")
                return
            ticketHistoryStr = ''
            notChangedTxt = ''
            nameFromTicketWriter = ''
            searchedLine = ''
            try:
                txtr = open("TicketsHistory.txt","r")
                rl = txtr.readlines()
                a = 0
                changeV = True
                for line in rl:
                    ticketHistoryStr = ticketHistoryStr + line
                    if changeV: 
                        changeV = False
                        if a == rti:
                            nameFromTicketWriter = line.split(':')[0]
                            searchedLine = line
                        a += 1
                    else: changeV = True
                txtr.close()
            except:
                await message.channel.send("This ID doesn't exist!")
                return

            if str(message.author) != nameFromTicketWriter and str(message.author) not in nicePeopleArray:
                await message.channel.send("You haven't the permission to remove tickets from the others!")
                return

            txtr = open("Tickets.txt","r")
            txtrrl = txtr.readlines()
            txtr.close()

            txtw = open("Tickets.txt","w")
            currentTickets = ''
            deleteNextLine = False
            for line in txtrrl:
                notChangedTxt = notChangedTxt + line
                if deleteNextLine:
                    deleteNextLine = False
                elif line != searchedLine:
                    currentTickets = currentTickets + line
                else: deleteNextLine = True

            txtw.write(currentTickets)
            txtw.close()
                
            if notChangedTxt == currentTickets:
                await message.channel.send("This ID doesn't exist!")
            else:
                txtStatusR = open("TicketStatus.txt", "r")
                txtStatusRl = txtStatusR.readlines()
                txtStatusR.close()
                txtStatusW = open("TicketStatus.txt", "w")
                theTicketHistory = ''
                for st in txtStatusRl:
                    if st.split(':')[0] == theRemoveId: theTicketHistory = theTicketHistory + st.split(':')[0] + ": ~Removed \n"
                    else: theTicketHistory = theTicketHistory + st
                txtStatusW.write(theTicketHistory)
                txtStatusW.close()

                txtMessageIDs = open("TicketMessageIds.txt","r")
                txtMessageIDsRl = txtMessageIDs.readlines()
                txtMessageIDs.close()
                theTicketChannel = client.get_channel(ticketChannelId)

                theMessageInTheTicketChannel = await theTicketChannel.fetch_message(int(txtMessageIDsRl[rti]))
                await theMessageInTheTicketChannel.delete()
                await message.channel.send("Your ticket has been successfully removed!")

            return



    #===Get Ticket Command===



        if TestForAdvancedSpeedrunCommand(messageStr, prefix + 'getticket'):
            try:
                strId = messageStr.replace(prefix + 'getticket ', '')
                intId = ReverseTicketID(strId)

                txtFile = open("TicketsHistory.txt","r")
                txtFileRl = txtFile.readlines()
                txtFile.close()

                activeTicket = txtFileRl[(intId) * 2] 

                txtFileStatus = open("TicketStatus.txt", "r")
                txtFileStatusRl = txtFileStatus.readlines()
                txtFileStatus.close()

                activeTicketStatus = txtFileStatusRl[(intId)].split('~')[1]

                if 'Removed' not in activeTicketStatus or str(message.author) in nicePeopleArray:
                    embed = discord.Embed(
                        title = 'Get Ticket',
                        description = '',
                        colour = discord.Colour.blue()
                    )
                    embed.add_field(name='ID: ', value=strId, inline=True)
                    embed.add_field(name='Status: ', value=activeTicketStatus, inline=True)
                    embed.add_field(name='Message: ', value=activeTicket, inline=False)
                    embed.set_thumbnail(url='https://www.speedrun.com/themeasset/2woqj208/logo?v=ae9623c')
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("This ticket doesn't exist!")
            except Exception as e:
                await message.channel.send("This ticket doesn't exist!" + str(e))



    #===Reaction Add===


          
    async def on_raw_reaction_add(self, payload): #We need to use the "raw"-Method, otherwise it only checks the messages in the bot-cache
        print("Reaction recognized")
        ctids = open("TicketMessageIds.txt", "r")
        ctidsRl = ctids.readlines()
        ctids.close()
        for ln in ctidsRl:
            if payload.message_id == int(ln):
                channel = client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)  
                if message.reactions[0].count > message.reactions[1].count:
                    ts = open("TicketStatus.txt", "r")
                    tsRl = ts.readlines()
                    ts.close()
                    newTxtString = ''
                    for line in tsRl:
                        if '~' in line:
                            if ctidsRl.index(ln) == tsRl.index(line) and "seen" in line.split('~')[1].lower(): newTxtString = newTxtString + line.split('~')[0] + "~Under consideration \n"
                            else: newTxtString = newTxtString + line
                    tsw = open("TicketStatus.txt", "w")
                    tsw.write(newTxtString)
                    tsw.close()
                    return
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if not message.author.bot: return 
        user = payload.member
        #Here he gets the role: Currently it's locked on "Event Announcements"
        tempRole = None
        roleTxt = open("Roles.txt", "r")
        roleTxtRl = roleTxt.readlines()
        roleTxt.close()
        for ln in roleTxtRl:
            if "~" in ln:
                if int(ln.split('~')[1]) == int(payload.message_id):  
                    tempRole = discord.utils.get(user.guild.roles, name=str(ln.split('~')[0])) 

        if user.bot: return
        await user.add_roles(tempRole)


      
    #===Reaction Remove===  


      
    async def on_raw_reaction_remove(self, payload): 
        #At the Reaction-Remove-Function he returns "payload.member = None", that's why the program needs to fetch the member
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)  
        if not message.author.bot: return 
        guild = client.get_guild(payload.guild_id) #916534358943342653 <-- That's the ID from "Will You Speedrun?"-Dc
        user = await(guild.fetch_member(payload.user_id)) # Here is the fetch-Function
        if user.bot: return
        tempRole = None
        roleTxt = open("Roles.txt", "r")
        roleTxtRl = roleTxt.readlines()
        roleTxt.close()
        for ln in roleTxtRl:
            if "~" in ln:
                if int(ln.split('~')[1]) == int(payload.message_id):  
                    tempRole = discord.utils.get(user.guild.roles, name=str(ln.split('~')[0])) 
        if user.bot: return
        await user.remove_roles(tempRole)
        

      
#Start the Discord Bot -->

client = MyClient()
keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)
