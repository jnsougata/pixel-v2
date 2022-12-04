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
async def on_error(e: Exception, _: dict):
    err = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
    embed = dh.Embed(
        title='Stack Trace', 
        description=f'```py\n{err}\n```', 
        color=0xff0000
    )
    await app.send_message(app.log_channel_id, {'embeds': [embed.json()]})

cogs = [
    f"cogs.{script[:-3]}" for script in os.listdir("cogs") 
    if script.endswith(".py")
]
app.load_cogs(*cogs)
