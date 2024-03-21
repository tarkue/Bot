from vkwave.bots import SimpleLongPollBot, SimpleBotEvent
from keyboard import KSTART, KS
from vkwave.bots.fsm import FiniteStateMachine, StateFilter, ForWhat, State, ANY_STATE
from os import getenv

bot = SimpleLongPollBot(tokens=getenv("TOKEN"), group_id=getenv("GROUP_ID"))
fsm = FiniteStateMachine()

class Question:
    wait = State("wait")

@bot.message_handler(bot.text_filter("/"))
async def start(event: SimpleBotEvent) -> str:
    return await event.answer("П", keyboard=KS.get_keyboard())

@bot.message_handler(bot.payload_filter(payload={"command":"start"}))
async def start(event: SimpleBotEvent) -> str:
    return await event.answer("Привет! Это текст начать!", keyboard=KSTART.get_keyboard())

@bot.message_handler(bot.payload_filter(payload={"command":"help"}))
async def help(event: SimpleBotEvent) -> str:
    await fsm.set_state(event=event, state=Question.wait, for_what=ForWhat.FOR_USER)
    await fsm.add_data(
        event=event,
        for_what=ForWhat.FOR_USER,
        state_data={"wait": True},
    )
    await event.answer("Опишите вашу проблему в деталях, мы обработаем ваше обращение в ближайший обход!\n\nУкажите проблему и комнату")

@bot.message_handler(StateFilter(fsm=fsm, state=Question.wait, for_what=ForWhat.FOR_USER))
async def handler_waiting(event: SimpleBotEvent) -> str:
    data = await fsm.get_data(event, for_what=ForWhat.FOR_USER)
    if data and data['wait'] == True:
        await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
        await bot.api_context.messages.send(user_id=284389677, message="Новая заявка:\n\n" + event.object.object.message.text, random_id=0)

    return "Ваша заявка была доставлена!"

bot.run_forever()