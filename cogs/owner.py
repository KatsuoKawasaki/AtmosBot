import disnake, config
from disnake.ext import commands
from disnake.ext.commands import slash_command, user_command, message_command


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.is_owner() #a simple owner check for owner commands
    @slash_command(
      name="shutdown",
      description="Сделайте так, чтобы бот отключился."
    )
    async def shutdown(self, inter):
        embed = disnake.Embed(
          title="Выход из системы",
          description=":wave: Пока!",
          color=config.success
        )
        await inter.send(embed=embed)
        await self.bot.close()

    @commands.is_owner()
    @slash_command(
      name="echo",
      description="Заставьте бота повторить что-нибудь"
    )
    async def echo(self, inter, *, message):
        await inter.response.send_message(f"Sent: `{message}`!", ephemeral=True)
        await inter.channel.send(message)

    @commands.is_owner()
    @slash_command(
      name="embed",
      description="Создайте пользовательское встраивание"
    )
    async def embed(self, inter, title, *, description):
        embed = disnake.Embed(
          title=title,
          description=description
        )
        await inter.send(embed=embed)

    @commands.is_owner()
    @slash_command(
      name="direct_message",
      description="Прямое сообщение пользователю"
    )
    async def dm(self, inter, user: disnake.Member, message):
        await user.send(message)
        print(f"Отправлено {message} к {user}")
        await inter.send("Зарегистрировал пользователя")


def setup(bot):
    bot.add_cog(Owner(bot))
    print(f"> Extension {__name__} is ready")