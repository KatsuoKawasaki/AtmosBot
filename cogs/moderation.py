import disnake
from disnake.ext import commands
import asyncio

# @commands.command() - команды

prefix = '%'

class moderation(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot



    #Command help
    @commands.command(pass_context = True)
    async def help(self, ctx):
        emb = disnake.Embed( title = 'Список команд' )
        emb.add_field( name = '{}ban' .format(prefix), value= 'Ограничение доступа пользователю.' )
        emb.add_field( name = '{}unban' .format(prefix), value= 'Разблокировка доступа пользователя.' )
        emb.add_field( name = '{}kick' .format(prefix), value= 'Выгнать пользователя.' )
        await ctx.send( embed = emb )

    #ban/unban
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: disnake.Member = None, time = None, *, reason: str = None):
        async def unb(self, member):
            users = await ctx.guild.bans()
            for ban_user in users:
                if ban_user.user == member:
                    await ctx.guild.unban(ban_user.user)       
        if member:
            if time: 
                time_letter = time[-1:] 
                time_numbers = int(time[:-1]) 
                
                def t(time_letter): 
                    if time_letter == 's':
                        return 1
                    if time_letter == 'm':
                        return 60
                    if time_letter == 'h':
                        return 60*60
                    if time_letter == 'd':
                        return 60*60*24
                if reason:
                    await member.ban(reason=reason)
                    await ctx.send(embed=disnake.Embed(description=f'Пользователь {member.mention} был забанен \nВремя: {time} \nПричина: {reason}' ))
                    
                    await asyncio.sleep(time_numbers*t(time_letter))
                    
                    await unb(member)
                    await ctx.send(f'Пользователь {member.mention} разбанен.')
                else:
                    await member.ban()
                    await ctx.send(embed=disnake.Embed(description=f'Пользователь {member.mention} был забанен. \nВремя: {time}'))
                    
                    await asyncio.sleep(time_numbers*t(time_letter))
                    
                    await unb(member)
                    await ctx.send(f'Пользователь {member.mention} разбанен.')
            else:
                await member.ban()
                await ctx.send(embed=disnake.Embed(description=f'Пользователь {member.mention} был забанен.'))
        else: 
            await ctx.send('Введите имя пользователя.')
        
    #unban
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, id_: int = None):
        if id_:
            banned_users = await ctx.guild.bans()
            member_full = commands.get_user(id=id_)
            for ban in banned_users:
                if ban.user == member_full:
                    await ctx.guild.unban(ban.user)
            await ctx.send('Пользователь разбанен')
        else:
            await ctx.send('Введите айди')

    #kick
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: disnake.Member = None, *, reason:str = None):
        if member:
            if reason:
                await member.kick(reason=reason)
                await ctx.send(embed=disnake.Embed(description=f'Пользователь {member.mention} был выгнан. \nПричина: {reason}' ))
            else:
                await member.kick()
                await ctx.send(embed=disnake.Embed(description=f'Пользователь {member.mention} был выгнан.'))
        else: 
            await ctx.send('Введите имя пользователя.')


    # Очистка чата
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit=count+1)
        await ctx.send(f"Было удаленно {count} сообщений")


def setup(bot:commands.Bot):
    bot.add_cog(moderation(bot))
    print(f">Extension {__name__} is ready")