import os
import discohook as dh

app = dh.Client(
    application_id=int(os.getenv("APPLICATION_ID")),
    public_key=os.getenv("PUBLIC_KEY"),
    token=os.getenv("DISCORD_TOKEN"),
    express_debug=True,
)

cogs = [
    f"cogs.{script[:-3]}" for script in os.listdir("cogs") 
    if script.endswith(".py")
]
for cog in cogs:
    app.load_cog(cog)