import time
import telebot
from telebot import types

TOKEN = '00000000000000000000000000000000000000000000'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    'hood': 'set up a town, brah..',
}




# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "I already know you, no need for me to scan you again!")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page





# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['hood'])
def handle_text(message):
    def weather(town):
        import pyowm as owm
        mgr = owm.OWM('000000000000000000000000000000000000').weather_manager()
        place = town
        try:
            observation = mgr.weather_at_place(place)
            w = observation.weather
            temper  = w.temperature('celsius')['temp']
            temper_max = w.temperature('celsius')['temp_max']
            temper_min = w.temperature('celsius')['temp_min']
            stts = w.status
            dtld_stts = w.detailed_status

            pogoda = [
            'temper in ' + str(place) + ' = ' + str(temper),
            'temper_max in ' + str(place) + ' = ' + str(temper_max),
            'temper_min in ' + str(place) + ' = ' + str(temper_min),
            'status in ' + str(place) + ' = ' + str(stts),
            'detailed_status in ' + str(place) + ' = ' + str(dtld_stts)
            ]

            pogoda_str = str(pogoda)

            file = open('pgd.txt', 'w')
            file.write(pogoda_str)
            file.close()
        except:
            pogoda = 'wrong hood'
            file = open('pgd.txt', 'w')
            file.write(pogoda_str)
            file.close()


    bot.send_message(message.chat.id, "which town? ")
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        txt = message.text
        weather(txt)

        print(txt)
        time.sleep(3)
        try:
            file = open('c:/py/pgd.txt', 'r')
            bot.send_message(message.chat.id, file)
            file.close()
            bot.send_message(message.chat.id, file)
        except:
            pass



# if the user has issued the "/getImage" command, process the answer


# default handler for every other text


bot.polling()
