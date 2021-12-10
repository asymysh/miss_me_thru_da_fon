import discord
import os
import csv
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
from discord.ext.commands import Bot

import twilio
from twilio.rest import Client

#^ basic imports for other features of discord.py and python ^

account_sid = os.environ['twilsid']
auth_token = os.environ['twiltoken']


client = discord.Client()
twilio = Client(account_sid, auth_token)
client = commands.Bot(command_prefix = '!') #put your own prefix here

####################################################################
#--------------------STATUS CHECK----------------------------------#
####################################################################
@client.event
async def on_ready():
    print("bot online") #will print "bot online" in the console when the bot is online

@client.command()
async def ping(ctx):
  await ctx.send("pong!")


####################################################################
#-------------------MISS ME THRU DA PHONE--------------------------#
####################################################################
@client.command()
async def gottacallemall(ctx):
  await ctx.send("calling everyone! good lord it might take me a second for every 3 people on the list")

  with open('database.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
      print(row[1])
      try:
        call = twilio.calls.create(url='https://replit.com/@AsoomYesh/MemorableUniqueHarddrives#Response.xml',from_='+15158541872',to=row[1])
      except Exception:
        pass


@client.command()
async def callme(ctx, arg):
    await ctx.send("calling")
    print(arg)
    call = twilio.calls.create(url='https://replit.com/@AsoomYesh/MemorableUniqueHarddrives#Response.xml',from_='+15158541872',to=arg)

@client.command()
async def addme(ctx, arg):

  if len(arg)<10:
    await ctx.send("Thats either an invalid number or an international number. If youre trying to add international numbers you should try adding it with the country code")

  else:
    if len(arg)==10:
      arg='91'+ str(arg) 

    if len(arg)>13:
      await ctx.send("Hey! We added your number but the number of digits was a little suspicious. If you're certain that youve put in the correct number then theres nothing to worry about :) ")

    print(ctx.message.author,"added",arg)
    string= str(ctx.message.author)
    await ctx.send("We shall miss you thru da phone henceforth Monsieur/Madame"+" "+string+" "+ "having da phone number " + arg)
    data = [[string,arg]]

    with open('database.csv', 'a') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerows(data)


@client.command()
async def amiinit(ctx, arg=None):
  string=str(ctx.message.author)
  flag=0
  with open('database.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
      if string in row:
        flag=1
      if arg:
        print("There is an argument",arg)
        if arg in row:
          flag=2
  if flag==2:
    await ctx.send("Hey! I just found you, and this is crazy. But here's an idea; let me call you maybe ;)")
  if flag==1 and arg!=None:
    await ctx.send("Umm this is a little embarrasing. We have your Discord username listed but your number doesnt seem to match our database. Huh! Are you sure youre not being notty and trying to check someone else's number? ;) Try entering YOUR number next time.")
  if flag==1 and arg==None:
    await ctx.send("I mean we do have your Username listed on here. We'd recommend checking with a phone number just to confirm if you're REALLY on the list, yk?")
  if flag==0:
    await ctx.send("Pfffft. Your a loser. We don't have you're number L-O-S-E-R")
  


####################################################################
#--------------------IN-QUIZ COMMANDS------------------------------#
####################################################################
@client.command()
async def verify(ctx):
    channame = str(ctx.message.channel) + "-verified☑"
    await ctx.message.channel.edit(name=channame)
    
@client.command()
async def reset(ctx):
    channame = str(ctx.message.channel)
    string = "-verified☑"
    print("read the name as",channame)
    if string in channame:
      channame = channame.replace("-verified☑","")
      print("changed the name to",channame)
      await ctx.message.channel.edit(name=channame)
      await ctx.channel.purge()
    
    else:
      await ctx.send("Are you sure this is a Verified Question? I can only clear Verified Questions. Try using !verify before using !reset if you're still having troubles. Contact catcat for everything else ig")

@client.command()
async def rename(ctx, arg):
      await ctx.message.channel.edit(name=arg)


####################################################################
#---------------------CLIENT RUN COMMAND---------------------------#
####################################################################

client.run(os.getenv("TOKEN")) #get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value. 
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!