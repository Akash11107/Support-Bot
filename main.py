import discord
from discord.ext import commands, tasks
import config
import os
import sys
import random
import discord.utils as utils
import asyncio
import random
import datetime
from datetime import datetime, timedelta
import pytz
from discord.ui import View, Button

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)



@bot.event
async def on_ready():
    print('Online For 24 x 7')
    await bot.tree.sync()








# help cmd
@bot.tree.command(name="help", description="Get Help")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help", description="Here are the commands you can use", color=discord.Color.blue())
    embed.add_field(name="Moderation", value="/ban, /kick, /timeout, /clear, /dm, /mute, /unmute, /autorole_add", inline=False)
    embed.add_field(name="Public", value="/store, /report_player", inline=False)
    embed.add_field(name="Store And Giveaways", value="/store, /giveaway_create(BETA), /giveaway_reroll(BETA), /giveaway_end(BETA)", inline=False)
    await interaction.response.send_message(embed=embed)

# Clear Cmd
@bot.tree.command(description="Delete Messages As Specified In The Channel Where The Command Was Ran")
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
async def clear_all(interaction: discord.Interaction, amount: int,):
    await interaction.response.defer(thinking=True, ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Deleted {amount} messages", ephemeral=True)

@clear_all.error
async def on_error(interaction: discord.Interaction, error:commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
                    

# Silk Pro Cmd
@bot.tree.command(name="silk_pro", description="Updated Store Prices According To Your Currency!")       
async def store(interaction: discord.Interaction):
    embed = discord.Embed(title="🛒 Store Information (Mostly Used Currency)", color=0x00ffb3)
    embed.description = "All of prices are monthly prices."
    embed.set_author(name="🛒 Official Store", url="")
    embed.add_field(name="USD", value="**Ranks**\nSilk Pro(Monthly): $5\nSilk Pro(3 Months): $12\nSilk Pro(6 Month): $25\nSilk Pro(Yearly): $50", inline=True)
    embed.add_field(name="INR", value="**Ranks**\nSilk Pro(Monthly): ₹399\nSilk Pro(3 Months): ₹999\nSilk Pro+(6 Month): ₹1999\nSilk Pro(Yearly): ₹4099", inline=True)
    embed.add_field(name="EUR", value="**Ranks**\nSilk Pro(Monthly): €4\nSilk Pro(3 Months): €10.99\nSilk Pro(6 Month): €22\nSilk Pro(Yearly): €44.99", inline=True)
    embed.add_field(name="GBP", value="**Ranks**\nSilk Pro(Monthly): £3\nSilk Pro(3 Months): £8.99\nSilk Pro(6 Month): £18.99\nSilk Pro(Yearly): €38.99", inline=True)
    embed.set_footer(text="Silk Client Store Latest Update || Official Store Updates")
    await interaction.response.send_message(embed=embed)




# staff cmd
@bot.tree.command(name="staff", description="Show the list of staff and their online status")
async def staff_online(interaction: discord.Interaction):
    staff_role = interaction.guild.get_role(1214815241469173800)  # Replace with the ID of the staff role
    online_staff = [member for member in staff_role.members if member.status != discord.Status.offline]
    offline_staff = [member for member in staff_role.members if member.status == discord.Status.offline]

    embed = discord.Embed(title="Staff Online Status", color=discord.Color.blue())
    embed.add_field(name="All Staff:", value="\n".join([f"{i+1}. {member.mention} {'🟢' if member in online_staff else '🔴'}" for i, member in enumerate(staff_role.members)]), inline=False)
    embed.add_field(name="Online Staff:", value="\n".join([f"{i+1}. {member.mention} 🟢" for i, member in enumerate(online_staff)]), inline=False)
    embed.add_field(name="Offline Staff:", value="\n".join([f"{i+1}. {member.mention} 🔴" for i, member in enumerate(offline_staff)]), inline=False)

    await interaction.response.send_message(embed=embed)




# ticket cmd - open a ticket from a dropdown menu
category_id = 1230415640079110236  # Replace with the ID of the category where tickets should be created
log_channel_id = 1249321995473125436  # Replace with the ID of the log channel

class ConfirmCloseButton(discord.ui.Button):
    def __init__(self, ticket_channel):
        super().__init__(style=discord.ButtonStyle.danger, label="Close Ticket")
        self.ticket_channel = ticket_channel

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Confirm Close", description="Are you sure you want to close this ticket?")
        view = discord.ui.View()
        yes_button = discord.ui.Button(style=discord.ButtonStyle.green, label="Yes")
        no_button = discord.ui.Button(style=discord.ButtonStyle.red, label="No")
        view.add_item(yes_button)
        view.add_item(no_button)

        async def yes_callback(interaction):
            await interaction.response.defer()
            reason_message = await bot.wait_for('message', check=lambda message: message.author == interaction.user)
            reason = reason_message.content
            await self.ticket_channel.delete()
            log_channel = bot.get_channel(log_channel_id)
            log_embed = discord.Embed(title="Ticket Closed", description=f"Ticket closed by {interaction.user.mention} for reason: {reason}")
            await log_channel.send(embed=log_embed)
            await interaction.followup.send("Ticket closed!")

        async def no_callback(interaction):
            await interaction.response.defer()
            await interaction.followup.send("Ticket not closed.")

        yes_button.callback = yes_callback
        no_button.callback = no_callback

        await interaction.response.send_message(embed=embed, view=view)

class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="General Issue", description="To Claim Rewards or Any General Issue Related To Client"),
            discord.SelectOption(label="Reporting", description="Report A Person or A Client Bug"),
            discord.SelectOption(label="Partnership", description="To Partner With Silk Client"),
            discord.SelectOption(label="Punishment Appeal", description="To Appeal For The Punishment You Have Recieved"),
            discord.SelectOption(label="Store Issue", description="To Check Your Order or Issue Related To Store"),
            discord.SelectOption(label="Other", description="Anything that we haven't mention then open this ticket"),
        ]
        super().__init__(placeholder="Choose An Option From Below.", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        ticket_type = self.values[0]
        category = bot.get_channel(category_id)
        ticket_channel = await category.create_text_channel(f"ticket-{ticket_type.lower()}-{interaction.user.name}")
        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)  # Add the user to the channel
        embed = discord.Embed(title="Ticket Created", description=f"Hello {interaction.user.mention}, please describe your issue below")
        view = discord.ui.View()
        view.add_item(ConfirmCloseButton(ticket_channel))
        
        await ticket_channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"Your ticket has been created! Please check {ticket_channel.mention} to describe your issue.", ephemeral=True)

@bot.command(name="tic")
async def ticket(ctx):
    view = discord.ui.View()
    view.add_item(TicketDropdown())
    embed = discord.Embed(title="Support Has Arrived", description="Please Choose Your Support-Type By Clicking On The Drop-Down Menu!")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1241814565856084068/1246730963527012452/discord-icon.png?ex=667680b0&is=66752f30&hm=fca70f6cf6d5943ccae532553a3dce471c457a89ac4124ca5667b7b6567c3bf3&")
    embed.set_footer(text="Silk Client Official Support.")
    await ctx.send(embed=embed, view=view)

# If the user does not have permisson then,
async def ticket(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You don't have permission to run this command.")
        return

# If the user has the permisson then,
    view = discord.ui.View()
    view.add_item(TicketDropdown())
    embed = discord.Embed(title="Create a Ticket", description="Select a ticket type below")
    await ctx.send(embed=embed, view=view)




# Giveaway_create

giveaway_participants = {}  # dictionary to store giveaway participants

@bot.command(name="gibe")
async def giveaway(ctx, prize: str, *, duration: str):
    # Parse the duration string into seconds
    duration_seconds = 0
    for part in duration.split():
        if part.endswith('s'):
            duration_seconds += int(part[:-1])
        elif part.endswith('m'):
            duration_seconds += int(part[:-1]) * 60
        elif part.endswith('h'):
            duration_seconds += int(part[:-1]) * 3600
        elif part.endswith('d'):
            duration_seconds += int(part[:-1]) * 86400

    # Calculate the end time of the giveaway
    end_time = datetime.now() + timedelta(seconds=duration_seconds)
    
    embed = discord.Embed(title="Giveaway!", description=f"**{prize}**", color=discord.Color.gold())
    embed.set_footer(text=f"Hosted by {ctx.author.name}")
    embed.add_field(name="Duration", value=f"{duration} (ends at {end_time.strftime('%Y-%m-%d %H:%M:%S')})", inline=False)

    class GiveawayButton(Button):
        def __init__(self):
            super().__init__(style=discord.ButtonStyle.green, label="Enter Giveaway")

        async def callback(self, interaction: discord.Interaction):
            if interaction.user.id in giveaway_participants.get(ctx.channel.id, []):
                class QuitButton(Button):
                    def __init__(self):
                        super().__init__(style=discord.ButtonStyle.red, label="Quit Giveaway")

                    async def callback(self, interaction: discord.Interaction):
                        giveaway_participants.setdefault(ctx.channel.id, []).remove(interaction.user.id)
                        await interaction.response.send_message("You have quit the giveaway!", ephemeral=True)

                view = View()
                view.add_item(QuitButton())
                await interaction.response.send_message("Do you want to quit the giveaway?", view=view, ephemeral=True)
            else:
                giveaway_participants.setdefault(ctx.channel.id, []).append(interaction.user.id)
                await interaction.response.send_message("You have entered the giveaway!", ephemeral=True)

    view = View()
    view.add_item(GiveawayButton())

    giveaway_msg = await ctx.send(embed=embed, view=view)



    # rps 

def determine_winner(player_choice, bot_choice):
    if player_choice == bot_choice:
        return "tie"
    elif (player_choice == "Rock" and bot_choice == "Scissors") or (player_choice == "Scissors" and bot_choice == "Paper") or (player_choice == "Paper" and bot_choice == "Rock"):
        return "win"
    else:
        return "lose"

@bot.command(name="rps_game", description="Play Rock, Paper, Scissors!")
async def rock_paper_scissors(ctx: commands.Context):
    embed = discord.Embed(title="Rock, Paper, Scissors!", description="Choose your move:", color=0x00ff00)
    embed.set_image(url="https://media1.tenor.com/m/6OLOBD89g1QAAAAC/smile-precure-cure-peace.gif")  # Add your banner URL here
    view = RockPaperScissorsView()
    await ctx.send(embed=embed, view=view)

class RockPaperScissorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.primary)
    async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "Rock"
        await interaction.response.defer()
        await self.play_game(interaction)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.primary)
    async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "Paper"
        await interaction.response.defer()
        await self.play_game(interaction)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.primary)
    async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "Scissors"
        await interaction.response.defer()
        await self.play_game(interaction)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

    async def play_game(self, interaction: discord.Interaction):
        choices = ["Rock", "Paper", "Scissors"]
        bot_choice = random.choice(choices)
        result = determine_winner(self.value, bot_choice)
        embed = discord.Embed(title="Result!", description=f"You chose {self.value} and I chose {bot_choice}.", color=0x00ff00)
        if result == "win":
            embed.description += " You win!"
        elif result == "lose":
            embed.description += " I win!"
        else:
            embed.description += " It's a tie!"
        view = PlayAgainView()
        await interaction.followup.send(embed=embed, view=view)

class PlayAgainView(discord.ui.View):
    @discord.ui.button(label="Play Again", style=discord.ButtonStyle.primary)
    async def play_again_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Rock, Paper, Scissors!", description="Choose your move:", color=0x00ff00)
        embed.set_image(url="https://media1.tenor.com/m/6OLOBD89g1QAAAAC/smile-precure-cure-peace.gif")  # Add your banner URL here
        view = RockPaperScissorsView()
        await interaction.response.send_message(embed=embed, view=view)


# FAQs 
@bot.command(name="faqs", description="Get FAQs")
async def faqs(interaction: discord.Interaction):
    embed = discord.Embed(title="FAQs", description="Frequently Asked Questions", color=0)
    embed.add_field(name="Q: What is Silk Client?", value="A: Silk Client is a Minecraft Client for Cracked as well as for Premium users.It is mostly used for PVP and Skyblock. It Provides Tons Of Features like free cosmetics, fps boost, Supports Pojav.", inline=False)
    embed.add_field(name="Q: How do I use this bot?", value="A: You can use this bot by typing `/` and then the command you want to use", inline=False)
    embed.add_field(name="Q: How do I report a bug?", value="A: You can report a bug by using the `/report_bug` command", inline=False)
    embed.add_field(name="Q: What is Silk Pro?,", value="A: Silk Pro is a subscription with extra features and benefits, it increases your Silk Client experience and also your minecraft gameplay experience.", inline=False)
    embed.add_field(name="Q: How Do I Report A Player?", value="A: You can report a player by using the `/report_player` command", inline=False)
    embed.add_field(name="Q: What Features Does The Silk Pro Offers Me?", value="A: Silk Pro offers many features to the Silk Client Users as well as for Better Minecraft Journey. It provides features like:\n"
                    "* Access To All Pvp and Skyblock Mods\n"
                    "* Early Access Of Silk Client Special Cape And Cosmetics\n"
                    "* Other features include:\n"
                    "* 10% Discount On Every Orders\n"
                    "* @Silk Pro Discord Role\n"
                    "* Special Giveaways Alongside with free users giveaway\n"
                    "* Custom Cape And Much More But we may still add some more and interesting features to it.", inline=False)
    embed.add_field(name="Q: How Can I Check Prices Of Silk Pro", value="You Can Check Prices By using `/silk_pro` cmd")
    await interaction.response.send_message(embed=embed)


    # Announcement 
channel_id = 1241818041617088563  # Replace with the channel ID where you want to send the message
embed_message = discord.Embed(description="If you're facing any kind of problem then please try to open a ticket in support channel. We appreatiate You", color=0x00ff00)

@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
    if channel:
        while True:
            try:
                await channel.send(embed=embed_message)
                await asyncio.sleep(300)  # Sec mai hai
            except discord.Forbidden:
                print("I don't have permission to send messages in that channel.")
                break
            except discord.HTTPException as e:
                print(f"An error occurred: {e.text}")
                break
    else:
        print(f"Channel with ID {channel_id} not found or inaccessible.")



@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="Silk Client")
    await bot.change_presence(status=discord.Status.online, activity=activity)


        # Trigger Thing

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if 'discord.com/invite/' in message.content or 'discord.gg/' in message.content:
        await message.delete()
        embed = discord.Embed(description=f"{message.author.mention} You're not allowed to send other Discord server links. It's Bannable Offence", color=0xFF0000)
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


# Ban
# Kick
# Timeout




bot.run(config.DISCORD_TOKEN)