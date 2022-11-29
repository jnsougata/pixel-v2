import deta
import discohook as dh
from utils.db import db


class Pingrole(dh.Cog):
    
    @dh.Cog.command(
        name="pingrole",
        description="set the role to ping with youtube feeds",
        options=[dh.RoleOption("role", "the role to ping", required=True)],
        permissions=[dh.Permissions.manage_guild],
        dm_access=False,
    )
    async def pingrole(self, i: dh.Interaction, role: dh.Role):
        updater = deta.Updater()
        updater.set("pingrole", role.id)
        await db.update(i.guild_id, updater)
        emd = dh.Embed(description=f'✅ Pingrole {role.mention} added Successfully', color=0xc4302b)
        return await i.command.response(embed=emd, ephemeral=True)
        

def setup(app: dh.Client):
    app.add_cog(Pingrole())
