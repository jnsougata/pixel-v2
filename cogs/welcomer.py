import deta
import discohook as dh
from utils.db import db, drive


class Welcomer(dh.Cog):
    
    @dh.Cog.command(
        id="1047186185010806844",
        name="welcomer",
        description="setup the welcomer",
        options=[
            dh.ChannelOption("channel", "the channel to send the welcome message to", required=True, channel_types=[dh.ChannelType.guild_text]),
            dh.AttachmentOption("image", "the image to send with the welcome message"),
        ],
        permissions=[dh.Permissions.manage_guild],
        dm_access=False,
    )
    async def welcomer(self, i: dh.Interaction, channel: dh.Channel, image: dh.Attachment = None):
        updater = deta.Updater()
        updater.set("welcomer", channel.id)
        await db.update(i.guild_id, updater)
        if image:
            await drive.put(await image.read(), f"{i.guild_id}_welcomer.png", folder="welcomer")
            await i.command.response(f'✅ Welcomer bound to {channel.mention} with following [Image]({image.url})', ephemeral=True)
        else:
            await i.command.response(f'✅ Welcomer bound to {channel.mention}', ephemeral=True)

def setup(app: dh.Client):
    app.add_cog(Welcomer())
