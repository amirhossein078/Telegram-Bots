import os
import shutil
import telebot
from telebot.types import ReplyKeyboardMarkup
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from PIL import Image

bot = telebot.TeleBot("YOUR BOT TOKEN")

main_key = ReplyKeyboardMarkup(resize_keyboard = True , one_time_keyboard = False)
convert_key = ReplyKeyboardMarkup(resize_keyboard = True , one_time_keyboard = False)

main_key.add ('JPG to PDF♻️')
convert_key.add('Convert🖨','Back🔙')

admin_key = InlineKeyboardMarkup(row_width=2)
#inline
msg_key = InlineKeyboardButton(text = 'msg to all✉️',callback_data = "msg")
sub_key = InlineKeyboardButton(text = 'subscribes📇',callback_data = "sub")
admin_key.add(msg_key,sub_key)
@bot.message_handler(commands=['start'])
def start(message):
    with open('python/data.txt', 'a+') as file:
        with open('python/data.txt', 'r+') as file:
            content = file.read()
            if str(message.chat.id) not in content:
                file.write(str(f"{message.chat.id}\n"))
                file.seek(0)
            else:
                pass
    bot.send_message(message.chat.id,'Welcom to JPG Convertor Bot🖨\n\nHow can I help you?🧐',reply_markup = main_key)

@bot.message_handler(func = lambda message: True)
def jpg_to_pdf(message):
    if message.text == 'JPG to PDF♻️':
        bot.send_animation(message.chat.id,'https://t.me/hsusysgtgs/15',caption="For Convert see this Gif:☝️☝️🖨 \n1- Select your pictures from Gallery and Send me with Sort and without groping.🗂\n\n2-After upload pictures press on Convert🖨️\n⬇️⬇️⬇️⬇️⬇️⬇️",reply_markup = convert_key)

    elif message.text == "Convert🖨":
        message_id = bot.send_message(message.chat.id, "Converting...🖨\nPlease wait...⏳").message_id
        convert(message.chat.id)
        bot.delete_message(message.chat.id,message_id)
    elif message.text == "Back🔙" :
        bot.send_message(message.chat.id,"You are Back to Main Menu, Choose your Request.🤖" , reply_markup = main_key)
    elif message.text == "admin" and message.chat.id == int("232382564"):
        bot.reply_to(message,"hello admin",reply_markup = admin_key)
    else:
       bot.reply_to(message,"your message not define to me.🫤\nplease use keys.🎹")


# دانلود عکس
@bot.message_handler(content_types=["photo"])
def download(message):
    file_id = message.photo[-1].file_id  
    file_info = bot.get_file(file_id)
    folder_path = f"python/{message.chat.id}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"{file_info.file_path.split('/')[-1]}")

    downloaded_file = bot.download_file(file_info.file_path)

    new_file = open(file_path, 'wb')
    new_file.write(downloaded_file)
    new_file.close()


def convert(chat_id):
    folder_path = f"python/{chat_id}"
    if not os.path.exists(folder_path):
        bot.send_message(chat_id, "No images found to convert.")
    else:

        images = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.jpg') or file_name.endswith('.png'):
                image_path = os.path.join(folder_path, file_name)
                images.append(Image.open(image_path))
                images.sort(key=lambda img: img.filename)
        if folder_path:

            pdf_path = os.path.join(folder_path, 'converted_images.pdf')
            images[0].save(pdf_path, save_all=True, append_images=images[1:])

        
            with open(pdf_path, 'rb') as pdf_file:
                bot.send_document(chat_id, pdf_file,caption = "Your images have been converted to PDF.✅", reply_markup = main_key)
        shutil.rmtree(folder_path)

bot.infinity_polling()