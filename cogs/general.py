import disnake, config, random, aiohttp
from disnake.ext import commands
from disnake.ext.commands import slash_command, user_command, message_command


class General(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @slash_command(
      name="ping",
      description="Проверьте, жив ли бот"
    )
    async def ping(self, inter):
        embed = disnake.Embed(
          title=":ping_pong: Pong!",
          description=f"{round(self.bot.latency * 1000)}ms.",
          color=disnake.Color.green()
        )
        await inter.response.send_message(embed=embed)
    
    @slash_command(
      name="poll",
      description="Создайте опрос, на который пользователи могут реагировать!"
    )
    async def poll(self, inter, emoji_1: disnake.Emoji, emoji_2: disnake.Emoji, emoji_3: disnake.Emoji, title):
        embed = disnake.Embed(
          title=title,
          description="Создан новый опрос!",
          color=disnake.Color.green()
        )
        embed.set_footer(
          text=f"Опрос создан: {inter.author} • Реагировать на голосование!"
        )
        embed_message = await inter.send(embed=embed)
        await embed_message.add_reaction(emoji_1)
        await embed_message.add_reaction(emoji_2)
        await embed_message.add_reaction(emoji_3)

    @slash_command(
      name="BotInfo",
      description="Получите некоторую информацию о боте"
    )
    async def BotInfo(self, inter):
        embed = disnake.Embed(
          title=f"Name: {self.bot.user}",
          description=f"ID: {self.bot.user.id}",
          color=disnake.Color.green()
        )
        embed.add_field(
          name="Информация о владельце",
          value="Katsuo Kawasaki#9991"
        )
        embed.add_field(
          name="Disnake Version",
          value=f"{disnake.__version__}"
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await inter.send(embed=embed)


    @slash_command(
      name="serverinfo",
      description="Получите некоторую информацию о сервере."
    )
    async def serverinfo(self, inter):
        server = inter.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = disnake.Embed(
            title="**Имя сервера:**",
            description=f"{server}",
            color=0x42F56C
        )
        try:
          embed.set_thumbnail(
              url=server.icon_url
          )
        except:
          print(f"Не найден значок сервера для {server.name}")
        embed.add_field(
            name="Сервер ID",
            value=server.id
        )
        embed.add_field(
            name="Количество участников",
            value=server.member_count
        )
        embed.add_field(
          name="Boosts",
          value=f"{str(inter.guild.premium_subscription_count)}"
        )
        embed.add_field(
            name="Text/Voice каналов",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Ролей ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Создан: {time}"
        )
        await inter.send(embed=embed)

    @slash_command(
      name="random",
      description="Сгенерируйте случайное число"
    )
    async def rng(self, inter, lower_number: int, upper_number: int):
        embed = disnake.Embed(
          title=":game_die: :",
          description=f"{random.randint(lower_number, upper_number)}",
          color=disnake.Color.green()
        )
        await inter.send(embed=embed)
    
    @slash_command(
      name="combo",
      description="Генерировать комбинации из строки"
    )
    async def combo(self, inter, string: str):
        complete_list = []
        for current in range(len(string)):
          a = [i for i in string]
          for y in range(current):
            a = [x+i for i in string for x in a]
          complete_list += a
          with open("combos.txt", "w") as f:
            for item in complete_list:
              f.write(item+"\n")
        await inter.send(file=disnake.File("combos.txt") )

def setup(bot):
    bot.add_cog(General(bot))
    print(f"> Extension {__name__} is ready")