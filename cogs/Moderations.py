import disnake, config
from disnake.ext import commands
from disnake.ext.commands import slash_command, user_command, message_command


class Moderations(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    #optional permissions remove if you dont want it
    @commands.has_permissions(manage_nicknames=True)
    @slash_command(
      name="nick",
      description="Измените ник пользователя"
    )
    async def nick(self, inter, member: disnake.User, *, nickname: str):
        try:
          await member.edit(nick=nickname)
          embed = disnake.Embed(
            title=":white_check_mark: Сменил Ник!",
            description=f"**{member}** новый ник **{nickname}**!",
            color=config.success
          )
          await inter.send(embed=embed)
        except:
          embed = disnake.Embed(
            title="Ошибка",
            description=f"Произошла ошибка при попытке изменить ник {member}",
            color=config.error
          )
          embed.add_field(
            name="Faq",
            value="Попробуйте убедиться, что ваши роли выше, чем роль пользователя!"
          )
          await inter.send(embed=embed)

    @commands.has_permissions(kick_members=True)
    @slash_command(
      name="kick",
      description="Выгнать участника с сервера"
    )
    async def kick(self, inter, member: disnake.User, *, reason: str = "Не указана"):
      await member.kick(reason=reason)
      embed = disnake.Embed(
        title=f"{member} был выгнан {inter.author}",
        description=reason,
        color=config.success
      )
      await inter.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @slash_command(
      name="ban",
      description="Запретить пользователю доступ к серверу и всем сообщениям через несколько дней"
    )
    async def ban(self, inter, member: disnake.Member, delete_msg_days: int, *, reason: str = None):
      if delete_msg_days > 7: #можно удалять сообщения только менее чем за 7 дней
        delete_msg_days = 7
      await member.ban(delete_message_days=delete_msg_days, reason=reason)
      embed = disnake.Embed(
        title=f"{member} был заблокирован {inter.author}",
        description=f"Причина: {reason}",
        color=config.success
      )
      await inter.send(embed=embed)
    
    @commands.has_permissions(administrator=True)
    @slash_command(
      name="unban",
      description="Разбаньте пользователя, используйте идентификатор пользователя."
    )
    async def unban(self, inter, member_id, *, reason: str):
      member_id = int(member_id)
      member = await self.bot.fetch_user(member_id)
      await inter.guild.unban(member, reason=reason)
      embed = disnake.Embed(
        title=f"{member} был разблокирован {inter.author}",
        description=f"Причина: {reason}",
        color=config.success
      )
      await inter.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @slash_command(
      name="move",
      description="Перекиньте участника на голосовой канал"
    )
    async def move(self, inter, member: disnake.User, channel: disnake.VoiceChannel = None):
      if member.voice:
        await member.edit(voice_channel=channel)
        embed = disnake.Embed(
          title="Переехал на новую базу?!",
          description=f"{member} перекинут в {channel}",
          color=config.success
        )
        await inter.send(embed=embed)
      else:
        embed = disnake.Embed(
          title="Ошибка!",
          description=f"{member} не подключен к голосовому каналу!",
          color=config.error
        )
        await inter.send(embed=embed)


    @commands.has_permissions(manage_channels=True)
    @slash_command(
      name="lock",
      description="Lock a channel"
    )
    async def lock(self, inter, channel: disnake.TextChannel=None):
        channel = channel or inter.channel

        overwrite = channel.overwrites_for(inter.guild.default_role)
        overwrite.send_messages = False
        overwrite.add_reactions = False

        await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
        await channel.send(":lock: Channel Locked.")
    
    @commands.has_permissions(manage_messages=True)
    @slash_command(
      name="unlock",
      description="Unlock a channel"
    )
    async def unlock(self, inter, channel: disnake.TextChannel=None):
        channel = channel or inter.channel

        overwrite = channel.overwrites_for(inter.guild.default_role)
        overwrite.send_messages = True
        overwrite.add_reactions = True

        await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
        await channel.send(":unlock: Channel Unlocked.")

    @commands.has_permissions(manage_channels=True)
    @slash_command(
      name="archive",
      description="Archive a channel, voice channel or stage channel"
    )
    async def archive(self, inter, channel: disnake.TextChannel = None, voice_channel: disnake.VoiceChannel = None, stage_channel: disnake.StageChannel = None):
      channel = channel or voice_channel or stage_channel

      overwrite = channel.overwrites_for(inter.guild.default_role)
      overwrite.send_messages = False
      overwrite.add_reactions = False
      category = disnake.utils.get(inter.guild.channels, id=config.archive_id)

      embed = disnake.Embed(
        title=":white_check_mark: Archived!",
        color=config.success
      )
      await inter.send(embed=embed)
      await channel.edit(category=category)


def setup(bot):
    bot.add_cog(Moderations(bot))
    print(f"> Extension {__name__} is ready")