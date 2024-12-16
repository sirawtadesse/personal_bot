import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import time

# Replace with your bot's API token
API_TOKEN = "8147630662:AAG1y0mXJP_9a_6RjIgtWfVuZW-YQDM1Qls"
bot = telebot.TeleBot(API_TOKEN)

# Personal information
personal_info = {
    "name": "Siraw Tadesse",
    "birthplace": "Zindib, West Gojjam, Ethiopia",
    "current_address": "Bole, Addis Ababa, Ethiopia",
    "education": "Information Systems Graduate, Addis Ababa University",
    "current_position": "Full-stack Developer at RE Technology Solutions PLC",
}

# Paths to files
cv_file_path = r"C:\Users\dell\Documents\sirawcv\Siraw_CV_19.pdf"
profile_picture_path = r"C:\Users\dell\Documents\sirawcv\profile_picture.jpg"
certificate_paths = [
    r"C:\Users\dell\Documents\sirawcv\certificate_1.pdf",
    r"C:\Users\dell\Documents\sirawcv\certificate_2.pdf",
]
educational_files_paths = [
    r"C:\Users\dell\Documents\sirawcv\Siraw_Documents.pdf",
]
portfolio_image_path = r"C:\Users\dell\Documents\sirawcv\portfolio_screenshot.png"
# project_video_path = r"C:\Users\dell\Documents\sirawcv\project_demo_video.mp4"

# Start Command
@bot.message_handler(commands=["start"])
def start(message):
    welcome_text = f"""👋 *Welcome, {message.from_user.first_name}!* 

I'm Siraw Tadesse, here to share some information about myself.

Use the menu below to explore my details and more:
"""
    # Main Menu with a more attractive layout
    menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu.add(KeyboardButton("📜 Personal Info"), KeyboardButton("📄 Download CV"))
    menu.add(KeyboardButton("🏅 Download Certificates"), KeyboardButton("🎓 Download Educational Files"))
    menu.add(KeyboardButton("📸 Profile Picture"), KeyboardButton("🌐 My Portfolio"))
    menu.add(KeyboardButton("ℹ️ Contact Me"))

    bot.send_message(message.chat.id, welcome_text, reply_markup=menu)

# Handle all menu options
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "📜 Personal Info":
        info_text = f"""👤 *Personal Information:*

📍 **Name**: {personal_info['name']}
🗺️ **Birthplace**: {personal_info['birthplace']}
🏠 **Current Address**: {personal_info['current_address']}
🎓 **Education**: {personal_info['education']}
💼 **Current Position**: {personal_info['current_position']}
"""
        bot.send_message(message.chat.id, info_text, parse_mode="Markdown")
    
    elif message.text == "📄 Download CV":
        send_file(message.chat.id, cv_file_path, "📑 *Here is my CV*. Feel free to download it!")
    
    elif message.text == "🏅 Download Certificates":
        for cert_path in certificate_paths:
            send_file(message.chat.id, cert_path, "🏆 *Here is one of my certificates*. Feel free to download it!")
    
    elif message.text == "🎓 Download Educational Files":
        for edu_file_path in educational_files_paths:
            send_file(message.chat.id, edu_file_path, "🎓 *Here is an educational document*. Feel free to download it!")
    
    elif message.text == "📸 Profile Picture":
        send_file(message.chat.id, profile_picture_path, "📸 *This is my profile picture*.", is_photo=True)
    
    elif message.text == "🌐 My Portfolio":
        portfolio_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        portfolio_menu.add(KeyboardButton("📷 Portfolio Screenshot"), KeyboardButton("🎥 Portfolio Video"))
        portfolio_menu.add(KeyboardButton("🔙 Back to Main Menu"))
        bot.send_message(message.chat.id, "Choose an option for my portfolio:", reply_markup=portfolio_menu)
    
    elif message.text == "📷 Portfolio Screenshot":
        send_file(message.chat.id, portfolio_image_path, "🌐 *Here is my portfolio screenshot*. Check out my work!", is_photo=True)
    
    elif message.text == "🎥 Portfolio Video":
        send_file(message.chat.id, project_video_path, "🎥 *Check out my project demo video*!")

    elif message.text == "ℹ️ Contact Me":
        contact_text = f"""📩 *Contact Information:*

- 📧 **Email**: [sirawbizutadesse21@gmail.com](mailto:sirawbizutadesse21@gmail.com)
- 📱 **Phone**: +251 919 901 362  
- 🐱 **GitHub**: [Siraw's GitHub](http://www.github.com/sirawtadesse/)
- 🔗 **LinkedIn**: [Siraw's LinkedIn](http://www.linkedin.com/in/siraw-tadesse-668088274)
- 🌐 **Portfolio**: [Siraw's Portfolio](https://siraw-website.vercel.app/)
"""
        inline_markup = InlineKeyboardMarkup()
        inline_markup.add(
            InlineKeyboardButton("GitHub", url="http://www.github.com/sirawtadesse/"),
            InlineKeyboardButton("LinkedIn", url="http://www.linkedin.com/in/siraw-tadesse-668088274"),
            InlineKeyboardButton("Portfolio", url="https://siraw-website.vercel.app/")
        )
        bot.send_message(message.chat.id, contact_text, parse_mode="Markdown", reply_markup=inline_markup)
    
    elif message.text == "🔙 Back to Main Menu":
        start(message)
    
    else:
        bot.send_message(message.chat.id, "Please choose a valid option from the menu.")

# Helper function to send files
def send_file(chat_id, file_path, caption, is_photo=False, retries=3):
    try:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"File size: {file_size} bytes")
            if file_size > 0:
                print(f"Attempting to send file: {file_path} (Size: {file_size / 1024:.2f} KB)")
                with open(file_path, "rb") as file:
                    for attempt in range(retries):
                        try:
                            if is_photo:
                                bot.send_photo(chat_id, file, caption=caption, parse_mode="Markdown", timeout=60)
                            else:
                                bot.send_document(chat_id, file, caption=caption, parse_mode="Markdown", timeout=60)
                            print(f"File sent successfully: {file_path}")
                            return  # Exit after successful upload
                        except Exception as e:
                            print(f"Error during file upload attempt {attempt + 1}: {str(e)}")
                            if attempt < retries - 1:
                                time.sleep(5)  # Retry after 5 seconds
                            else:
                                raise e
            else:
                bot.send_message(chat_id, f"❌ Error: File `{file_path}` is empty.", parse_mode="Markdown")
        else:
            bot.send_message(chat_id, f"❌ Error: File `{file_path}` does not exist.", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")

# Run the bot
print("Bot is running...")
bot.polling(timeout=60, long_polling_timeout=60)
