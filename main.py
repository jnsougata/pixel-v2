import os
import traceback
import discohook as dh

app = dh.Client(
    application_id=int(os.getenv("APPLICATION_ID")),
    public_key=os.getenv("PUBLIC_KEY"),
    token=os.getenv("DISCORD_TOKEN"),
    log_channel_id=902228501120290866,
)

@app.on_error
async def on_error(e: Exception, data: dict):
    err = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
    embed = dh.Embed(
        title='Stack Trace', 
        description=f'```py\n{err}\n```\n```py\n{data}\n```', 
        color=0xff0000
    )
    await app.send_message(902228501120290866, {'embeds': [embed.json()]})

cogs = [
    f"cogs.{script[:-3]}" for script in os.listdir("cogs") 
    if script.endswith(".py")
]
for cog in cogs:
    try:
        app.load_cog(cog)
    except:
        pass