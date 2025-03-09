# telegram_sgcheckpointv2_pytutorial
Updated: 2025 -> https://github.com/tengfone/sgcustoms_telebot 

This is a continuation of the previous tutorial [telegram_sg_checkpoint_pytutorial](https://github.com/tengfone/telegram_sgcheckpoint_pytutorial). In this version, we will use a Conversational style bot and a custom keyboard.

Do check it out if you haven't as this tutorial is heavily dependent on that.

A basic tutorial to write a telegram bot using python written by someone who does not know how to code at all (Learnt on the go). 

This version uses telegram [ConversationHandler](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.conversationhandler.html) for simplicity purposes. We will be using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) as a wrapper.

## Screenshots
![SGCustom Camera](https://user-images.githubusercontent.com/20770447/62672343-e2bcc600-b9cc-11e9-95ab-0645431130d7.gif)

## Pre-Requisite
- Have read and understand [telegram_sg_checkpoint_pytutorial](https://github.com/tengfone/telegram_sgcheckpoint_pytutorial)
- Basic Knowledge On [Python 3.x](https://www.w3schools.com/python/)
- IDE (Personal Recommendation [PyCharm](https://www.jetbrains.com/pycharm/))
- A Telegram Account
- [Heroku Command Line](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
- [Heroku Account - Free](https://signup.heroku.com/)
- [GIT](https://git-scm.com/downloads)

## Getting Started
This tutorial will be using PyCharm as an IDE. 

### Importing files from previous project

We can always install a fresh copy of everything by using ```pip install``` but that will take too long and you do not
know which version you will be using. Therefore, we can use someone's/your own previously done project to use the same 
library version. 

Start off by creating a new project. Ensure it is utilizing ```pipenv``` as an environment.

![newproj](https://user-images.githubusercontent.com/20770447/62672561-d1c08480-b9cd-11e9-81c2-23278d491507.png)


Once created, you will realize that the IDE will auto generate a ```Pipfile``` for you in your 
root directory. Delete that. Instead we will be using ```requirements.txt``` from your previous project to load all the libraries in.

After deleting the auto generated ```Pipfile``` copy and paste/download from my repo, the ```requirements.txt```. Now your project
directory should look like this

![req](https://user-images.githubusercontent.com/20770447/62672729-5f03d900-b9ce-11e9-9256-919907c60cb7.png)

Once that is done. Run the command inside your IDE terminal (ensure directory is your project root directory).
```bash
$ pipenv shell
$ pipenv update
```
![pipenv](https://user-images.githubusercontent.com/20770447/62672792-9a060c80-b9ce-11e9-8855-77092ab9d186.png)

What this does is to load the ```requirements.txt``` file into a ```Pipfile``` and then it will download and install all
the required libraries into your Python Environment.

### Set Environments Variables

Remember to add ```TOKEN, API_KEY, MODE, HEROKU_APP_NAME``` in the console config.

## Code
The difference in V1 and V2 is how the code is being processed. For V1 what we were doing is using commands ```/commands``` to invoke functions. While for V2
we will be using a conversational style bot. A good example of a conversational bot can be found [here](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py) and [here](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot2.py).

#### State Machine
You will need to understand [State Machines](https://python-3-patterns-idioms-test.readthedocs.io/en/latest/StateMachine.html) to be able to fully 
understand the passing of arguments(eg User Information) in a conversation handler.

```MENU``` ```CHOOSING_CAMERA``` ```CHOOSING_RATES``` ```CALCULATE_SG_MY``` ```CALCULATE_MY_SG```
```python
MENU, CHOOSING_CAMERA, CHOOSING_RATES, CALCULATE_SG_MY, CALCULATE_MY_SG = range(5)
```
We will be using these 5 states. States can be anything you labelled it as. In this case I will be calling it in integers form, state 0, state 1 etc.

#### [Custom Keyboard](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#keyboard-menus)

```python
menu_reply_keyboard = [['Camera 📷'], ['Rates 💰'], ['Info ℹ️']]
camera_reply_keyboard = [['Woodlands', 'Tuas'], ['Back']]
rates_reply_keyboard = [['🇸🇬➡️🇲🇾', '🇲🇾➡️🇸🇬'], ['Back']]
```

Let's look at ```menu_reply_keyboard```

###### emoji

Emoji's can be added easily into the string function (Only for Python 3.x) for Python 2.x you will have to include the Unicode function. To add the
emoji in Python 3.0 just launch Telegram, copy and paste the emoji from Telegram into the string.

###### layout
If you noticed, the keyboard is stored as a list. By putting it in ```[['A'],['B'],['C']]```, your keyboard layout will look like this:

![hori](https://user-images.githubusercontent.com/20770447/62673733-2403a480-b9d2-11e9-8319-ecc50b23b916.png)


If you place it as ```[['A','B','C']]``` it will be like this:

![verti](https://user-images.githubusercontent.com/20770447/62673732-236b0e00-b9d2-11e9-8fce-45e3975d19ad.png)

Bear in mind you can mix and match the layout. Eg: ```camera_reply_keyboard = [['Woodlands', 'Tuas'], ['Back']]```

###### Reply Keyboard
To "enable" the keyboard, you will have to attach it to a text message. As such, we use ```update.message.reply_text``` function
to call the keyboard.

An example:
```python
@send_typing_action         # enable typing... when processing
def start(update, context):
    """
    This is  what happens when you type /start. It displays a message with a custom keyboard and returns to the state MENU
    """
    update.message.reply_text(
        "Going to 🇲🇾 or coming back 🇸🇬 \nCome, I let you see if got jam anot. \nOr you want exchange rate also can.",
        reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard, one_time_keyboard=True))
    return MENU
```
When you use the function ```update.message.reply_text```, the User ID and chat ID will automatically be passed in the function. ```reply_markup``` will 
identify what kind of keyboard you would like to pass it to. ```ReplyKeyboardMarkup(YOUR_KEY_BOARD, FUNCTION_TO_EXECUTE)```
Read up [telegram.ReplyKeyboardMarkup](https://python-telegram-bot.readthedocs.io/en/stable/telegram.replykeyboardmarkup.html) for more info.

###### message
This function passes all kinds of messages, from replies to getting input/output. The format can be ```update.message.reply_photo``` or ```update.message.reply_text``` whereby it takes
in the User's input / Chat ID etc.
```python
update.message.reply_photo(woodlands_bke_image, caption=(''...'))
```
The whole list of commands should be read and fully understand [here](https://python-telegram-bot.readthedocs.io/en/stable/telegram.message.html)

### [Send typing action](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#send-a-chat-action)
Adds the ```typing...``` status to the bot while its processing a function. Aesthetic purposes, makes it looks like its a human.
Add a ```@send_typing_action``` on top of any function for it to be called.
```python
def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func
``` 
### [Conversation Handler](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.conversationhandler.html)
This handler will be our primary way of communicating between User and bot
```python
class telegram.ext.ConversationHandler(entry_points, states, fallbacks, allow_reentry=False, run_async_timeout=None, 
timed_out_behavior=None, per_chat=True, per_user=True, per_message=False, conversation_timeout=None)
```
Sample Conversation Handler format:
```python
conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(Filters.regex('^Camera 📷$'), camera, pass_user_data=True),
                   MessageHandler(Filters.regex('^Rates 💰$'), rates, pass_user_data=True),
                   MessageHandler(Filters.regex('^Info ℹ️'), info, pass_chat_data=True)],
            CHOOSING_CAMERA: [MessageHandler(Filters.regex('^Woodlands$'), woodlands, pass_user_data=True),
                              MessageHandler(Filters.regex('^Tuas$'), tuas, pass_user_data=True)],
            CHOOSING_RATES: [MessageHandler(Filters.regex('^🇸🇬➡️🇲🇾$'), ask_rates_sg_my, pass_user_data=True),
                             MessageHandler(Filters.regex('^🇲🇾➡️🇸🇬$'), ask_rates_my_sg, pass_user_data=True)],
            CALCULATE_SG_MY: [MessageHandler(Filters.text, calc_rates_sg_my, pass_user_data=True)],
            CALCULATE_MY_SG: [MessageHandler(Filters.text, calc_rates_my_sg, pass_user_data=True)],
        },
        fallbacks=[MessageHandler(Filters.regex('^Back$'), start, pass_user_data=True)],
        allow_reentry=True  # this line is important as it allows the user to talk to the bot anytime
    )
```
```entry_points``` runs ```/start``` to execute your start function. This is to determine that you are "entering" the loop for a conversation.

```states``` are the different state machines the bot is in when you are executing the script. 

```regex``` stands for [regular expression](https://www.rexegg.com/regex-quickstart.html), which basically strips the text you click and match it with a function. However since we have already
pre-define our User input (Keyboard), we can just use the format ```('^xxx$')``` which basically just matches both input and output.

```pass_user_data``` is to ensure that the bot "remembers" the same User who  is talking to the bot and also pushes the Chat ID and User ID along .

```fallbacks``` you can think of it as a "Cancel" or "Back" function.

```allow_reentry``` this is important as it allows a User to communicate with the bot even if the conversation is cleared. This 
sorts of resets the State of the machine is in for the particular User. This is ***extremely*** important if we deloy it in the FREE Heroku as after
30 minutes of inactivity of the bot, Heroku puts it into sleep. If you resume the bot (sending a command), it will
forget the state you are in and will never enter back into the Conversation Handler.

The rest of the code can be found in ```bot.py```.

## Deployment
Same as [telegram_sg_checkpoint_pytutorial](https://github.com/tengfone/telegram_sgcheckpoint_pytutorial).

### Docker
I will not be doing an in-depth tutorial for Docker. You can Dockerize it to Heroku by creating a extension-less file called ```Dockerfile``` in your root directory

On the inside:
```dockerfile
FROM python:3.7

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD python /app/bot.py

```

On your project folder directory terminal:
```bash
$ heroku container:login
$ heroku container:push --app <HEROKU_NAME> web
$ heroku container:release --app <HEROKU_APP_NAME> web
```
and you're done.
## Further Development
- Deploying to a VPS
- Sending location gives you the nearest checkpoint camera

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Credits
[python-telegram-bot examples](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples)

[Creating Telegram Bot and Deploying it to Heroku](https://medium.com/python4you/creating-telegram-bot-and-deploying-it-on-heroku-471de1d96554)
## License
[MIT](https://choosealicense.com/licenses/mit/)
