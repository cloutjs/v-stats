import discord
import requests
import json

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith(".info"):
    name = message.content.split(".info")[1].strip()
    r = requests.get(f"https://api.projectv.gg/api/v1/frontend/users/{name}?expand=user,profile.preferred_platform,profile.preferred_game,settings,files,integrations,gameaccounts,teamfinder")
    if r.status_code == 200:
      r = r.json()
      country = requests.get("https://api.projectv.gg/api/v1/frontend/countries?page_size=200").json()["data"]
      for item in country:
        if item["id"] == r["profile"]["country"]:
          coun = item["name"]["en"]
      teams = requests.get(f"https://api.projectv.gg/api/v1/frontend/users/{name}/teams?expand=team,team.platforms,team.files")
      if not "description" in teams.text:
        team = "Not in a team"
      else:
        team = teams.json()["data"][0]["team"]["name"]
      link = "https://projectv.gg/teams/" + teams.json()["data"][0]["team"]["slug"]
      try:
        embed = discord.Embed(title=name, description=f"[Profile Link](https://projectv.gg/profile/{name})")
        embed.set_thumbnail(url=r["files"][0]["file"])
        embed.add_field(name="Valorant Tag", value=r["gameaccounts"][0]["value"])
        embed.add_field(name="Created at", value=r["profile"]["created_at"].split("T")[0])
        embed.add_field(name="Account verified?", value=r["verified"])
        embed.add_field(name="Country", value=coun)
        embed.add_field(name="Team", value=f"[{team}]({link})")
        await message.channel.send(embed=embed)
      except:
        await message.channel.send("Sorry, an error occured!")
    elif r.status_code == 404:
      await message.channel.send("User doesn't exist.")
    else:
      await message.channel.send("Sorry, an error occured!")   

  if message.content.startswith(".teaminfo"):
      name = message.content.split(".teaminfo")[1].strip()
      r = requests.get(f"https://api.projectv.gg/api/v1/frontend/teams/{name}?expand=files,settings,teamfinder,vrc_ranking.season,vrc_ranking.history")
      if r.status_code == 200:
        r = r.json()
        try:
          embed = discord.Embed(title=r["name"], description=f"[Team Link](https://projectv.gg/teams/{name})")
          embed.set_thumbnail(url=r["files"][0]["file"])
          embed.add_field(name="Member Count", value=r["members_count"])
          embed.add_field(name="Created at", value=r["settings"]["created_at"].split("T")[0])
          embed.add_field(name="Join requests open?", value=r["settings"]["allow_join_request"])
          await message.channel.send(embed=embed)
        except:
          await message.channel.send("Sorry, an error occured!")
      elif r.status_code == 404:
        await message.channel.send("Team doesn't exist.")
      else:
        await message.channel.send("Sorry, an error occured!")



client.run("")