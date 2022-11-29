import deta
import asyncio
import aiohttp
import discohook as dh
from utils.db import db


async def fetch_channel(channel_id: str) -> dict:
    url = f"https://aiotube.deta.dev/channel/{channel_id}/info"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()


class Unsubscribe(dh.Cog):
    
    @dh.Cog.command(
        name="unsubscribe",
        description="unsubscribe from a youtube feed",
        permissions=[dh.Permissions.manage_guild],
        dm_access=False,
    )
    async def unsubscribe(self, i: dh.Interaction):
        record = (await db.get(i.guild_id))[0]
        if not record.get("channels"):
            return await i.command.response("No channels subscribed", ephemeral=True)
        channel_ids = list(record["channels"].keys())
        tasks = [fetch_channel(channel_id) for channel_id in channel_ids]
        channels = await asyncio.gather(*tasks)

        channel_menu = dh.SelectMenu(
            dh.SelectMenuType.text, 
            placeholder="select channel(s) from list",
            options=[dh.SelectOption(channel["name"], channel["id"]) for channel in channels],
            max_values=len(channels),
        )
        @channel_menu.on_selection
        async def channel_menu_selection(i: dh.Interaction, values: list):
            updater = deta.Updater()
            for value in values:
                updater.delete(f"channels.{value}")
            await db.update(i.guild_id, updater)
            return await i.command.response("✅ Unsubscribed from selected channels", ephemeral=True)
        
        view = dh.View()
        view.add_select_menu(channel_menu)
        return await i.command.response(components=view, ephemeral=True)


def setup(app: dh.Client):
    app.add_cog(Unsubscribe())
