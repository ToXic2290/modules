# Докажи всем что ты - настоящий гуль.

from .. import loader

class gylMod(loader.Module):
	strings = {"name": "IamGhole"}
	
	async def watcher(self, message):
		me = (await message.client.get_me())
		if message.sender_id == me.id:
			if message.text.lower() == "я гуль":
				a = 1000				
				while a != 6:
					c = str(a)
					a = a - 7
					b = str(a)
					d = c + " - 7 = " + b
					await message.respond(d)
				await message.respond("Теперь понял кто тут гуль?\nby @HACKER_PHONE_ELITE")
