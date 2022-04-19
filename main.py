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

#=========Functions=========

#This function returns a nice looking Time-String
def ConvertStringToTime(strPar):
    parFloat = float(strPar)
    rest = round(parFloat % 60, 2)
    minutes = int(round((parFloat - rest) / 60, 0))
    returnString1 = ""
    returnString2 = ""
    if minutes < 10:
        returnString1 = "0" + str(minutes)
    else:
        returnString1 = "" + str(minutes)
    
    if rest < 10:
        returnString2 = ":0" + str(rest)
    else:
        returnString2 = ":" + str(rest)
        
    if rest * 100 % 10 == 0:
        return (returnString1 + returnString2 + "00")
    else:
        return (returnString1 + returnString2 + "0")

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
    letterArray2 = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
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

watchListChannelId = 963122498273157150  

bannedWords = ["nigga", "nigger"]
warningWords = ["retard", "retarded", "penis", "vagina"]

nicePeopleArray = ["FlippyDolphin#1651", "Meister Möhre#1623", "dash#8750", "JonasTyroller#7200", "OrangeChef#4553", "TheOrangeWhale#8667", "Zetas2#6270"]


categoryChoices = ["Any% NMG", "Any%", "Alt Ending", "All Collectibles", "No Shortcuts"]
bossChoices = ["Splitty", "Mr D.A.N.C.E", "Mama Squid", "Helpy", "Bartender", "Squid 1", "Squid 2"]
difficultyChoices = ["IE", "EE", "VE", "Easy"]
typingCategoryChoices = ["Any%NMG", "Any%", "AltEnding", "AllCollectibles", "NoShortcuts"]
typingBossChoices = ["Splitty", "MrDance", "MamaSquid", "Helpy", "Bartender", "Squid1", "Squid2"]
typingChapterChoices = ["ChapterA", "ChapterB", "ChapterC", "ChapterD", "ChapterE"]
typingOtherExtChoices = ["ChapterRelay", "Iaf", "DoubleTime", "Death%", "BlockMassacre", "MinimumKills"]

listOfSpeedyTicketWriter = [None] * 2

#=========Discord Client=========


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.Change_Values.start()
    #This is a loop which update every 300 seconds the values from the array
    @tasks.loop(seconds=300.0)
    async def Change_Values(self):      
        listOfSpeedyTicketWriter.clear()
        
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
            
                
        global maxLeaderboardIndex
        eventOutputString[a2] = eventOutputString[a2] + '```'
        maxLeaderboardIndex = a - 1
        print("Loop restarted...")
  
    async def on_message(self, message):
        #Creating a string from the message-Object
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
            if str(message.author) not in nicePeopleArray: return 
            async for m in message.channel.history(limit=1 + int(messageStr.replace(str(prefix + 'clear '), ''))):
                await m.delete()
            return



        #===Reaction Command (m!reaction)===


      
        #If a m!Reaction is in the message, then he has to delete the emoji and react with it on the last message
        if str(prefix + 'reaction') in messageStr.lower():
            if str(message.author) not in nicePeopleArray: return #when the author isn't included in the Array nothing happens
            a = 0
            tempData = [''] * 2
            async for data in message.channel.history(limit=2):
                tempData[a] = str(data.content)
                if a == 1:
                    await data.delete()
                a += 1

            try:
                await message.add_reaction(str(tempData[1]))
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
            



        #===Help Command (m!Help)==




        if TestForAdvancedSpeedrunCommand(messageStr, str(prefix + 'help')): 
            embed = discord.Embed(
            title = 'Help',
            description = 'This is a list of the commands: \n ',
            colour = discord.Colour.blue()
            )
            #embed.add_field(name='m!src X', value='Shows top X runs.', inline=True)
            #embed.add_field(name='m!src X-Y', value='Shows runs X through Y.\n', inline=True)
            embed.add_field(name='m!eventruns', value='Shows a list of all runs submitted during the event. \n', inline=True)
            embed.add_field(name='m!lb category difficulty X', value='Shows top X runs from \n the category in the difficulty.', inline=False)
            embed.add_field(name='m!lb category difficulty X-Y', value='Shows runs X through Y from \n the category in the difficulty.', inline=True)
            embed.add_field(name='m!ticket', value='Creates a ticket.', inline=False)
            embed.add_field(name='m!removeticket ID', value='Removes a ticket.', inline=True)
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
                txtw3.write("------------------------------------------------------------------------------------\n")

                txtw.close()
                txtw2.close()
                txtw3.close()

                listOfSpeedyTicketWriter.append(str(message.author))

                await message.channel.send(str(message.author.mention) + " Thank you for creating a ticket! :)  (ID: " + theCurrentId + ")")
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

                activeTicketStatus = txtFileStatusRl[(intId) * 2].split('~')[1]

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
            except:
                await message.channel.send("This ticket doesn't exist!")

    #===Reaction Add===


          
    async def on_raw_reaction_add(self, payload): #We need to use the "raw"-Method, otherwise it only checks the messages in the bot-cache
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if str(prefix + 'reaction') not in str(message.content) or str(message.author) not in nicePeopleArray: return 
        user = payload.member
        #Here he gets the role: Currently it's locked on "Event Announcements"
        eventAnnouncements = discord.utils.get(user.guild.roles, name='Event Announcements') 
        if user.bot: return
        await user.add_roles(eventAnnouncements)


      
    #===Reaction Remove===  


      
    async def on_raw_reaction_remove(self, payload): 
        #At the Reaction-Remove-Function he returns "payload.member = None", that's why the program needs to fetch the member
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)  
        if str(prefix + 'reaction') not in str(message.content) or str(message.author) not in nicePeopleArray: return
        guild = client.get_guild(payload.guild_id) #916534358943342653 <-- That's the ID from "Will You Speedrun?"-Dc
        user = await(guild.fetch_member(payload.user_id)) # Here is the fetch-Function
        eventAnnouncements = discord.utils.get(guild.roles, name='Event Announcements') 
        if user.bot: return
        await user.remove_roles(eventAnnouncements)    

      
#Start the Discord Bot -->

client = MyClient()
keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)
