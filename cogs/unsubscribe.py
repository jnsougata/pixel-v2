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
        id="1047213737930657802",
        name="unsubscribe",
        description="unsubscribe from a youtube feed",
        permissions=[dh.Permissions.manage_guild],
        dm_access=False,
    )
    async def unsubscribe(self, i: dh.CommandInteraction):
        record = (await db.get(i.guild_id))[0]
        if not record.get("channels"):
            return await i.response("No channels subscribed", ephemeral=True)
        await i.defer(ephemeral=True)
        channel_ids = list(record["channels"].keys())
        tasks = [fetch_channel(channel_id) for channel_id in channel_ids]
        channels = await asyncio.gather(*tasks)
        valids = [channel for channel in channels if channel]
        channel_menu = dh.SelectMenu(
            options=[dh.SelectOption(channel["name"], channel["id"]) for channel in valids],
            max_values=len(valids),
            placeholder="select channel(s) from list",
        )
        @channel_menu.onselection
        async def channel_menu_selection(i: dh.ComponentInteraction, values: list):
            updater = deta.Updater()
            for value in values:
                updater.delete(f"channels.{value}")
            await db.update(i.guild_id, updater)
            await i.edit_original("✅ Unsubscribed from selected channels", view=None, embed=None)
        
        view = dh.View()
        view.add_select_menu(channel_menu)
        await i.follow_up(view=view)


def setup(app: dh.Client):
    app.add_cog(Unsubscribe())
