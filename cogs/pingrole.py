import deta
import aiohttp
import discohook as dh
from utils.db import db


async def fetch_channel(channel_id: str) -> dict:
    url = f"https://aiotube.deta.dev/channel/{channel_id}/info"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
    

class Pingrole(dh.Cog):
    
    @dh.Cog.command(
        name="pingrole",
        description="set the role to ping with youtube feeds",
        options=[dh.RoleOption("role", "the role to ping", required=True)],
        permissions=[dh.Permissions.manage_guild],
        dm_access=False,
    )
    async def subscribe(self, i: dh.Interaction, role: dh.Role):
        updater = deta.Updater()
        updater.set("pingrole", role.id)
        await db.update(i.guild_id, updater)
        emd = dh.Embed(description=f'✅ Pingrole {role.mention} added Successfully', color=0xc4302b)
        return await i.command.response(embed=emd, ephemeral=True)
        

def setup(app: dh.Client):
    app.add_cog(Pingrole())
