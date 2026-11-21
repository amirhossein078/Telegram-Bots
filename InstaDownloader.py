import telebot
import instaloader
import os
import shutil

TELEGRAM_TOKEN = 'YOUR BOT TOKEN'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

loader = instaloader.Instaloader()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Please Send post URL")

@bot.message_handler(func=lambda message: True)
def download(message):
    url = message.text
    try:
        
        shortcode = url.split("/")[-2]
        
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        if post:
            loader.download_post(post, target='downloads')
            
            cap = post.caption
            
        if post.is_video:
            for filename in os.listdir('downloads'):
                if filename.endswith('.mp4'): 
                    with open(f'downloads/{filename}', 'rb') as file:
                        message_id = bot.send_message(message.chat.id,"Downloading... 📥").message_id
                        bot.send_video(message.chat.id,file,caption=cap)
                        bot.delete_message(message.chat.id,message_id)
        else:
            for filename in os.listdir('downloads'):
                if filename.endswith('.jpg'): 
                    with open(f'downloads/{filename}', 'rb') as file:
                        message_id = bot.send_message(message.chat.id,"Downloading... 📥").message_id
                        bot.send_photo(message.chat.id,file,caption=cap)
                        bot.delete_message(message.chat.id,message_id)
                        
        shutil.rmtree("downloads")
    except Exception as e:
        bot.reply_to(message, f'Error: {e}')
        bot.delete_message(message.chat.id,message_id)
if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    
bot.infinity_polling()