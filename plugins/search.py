import asyncio
from info import *
from utils import *
from time import time 
from client import User
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    f_sub = await force_sub(bot, message)
    if f_sub==False:
       return     
    channels = (await get_group(message.chat.id))["channels"]
    if bool(channels)==False:
       return     
    if message.text.startswith("/"):
       return    
    query   = message.text 
    head    = "<b>👀 𝐎𝐧𝐥𝐢𝐧𝐞 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠 𝐋𝐢𝐧𝐤 👀</b>\n\n"
    results = ""
    try:
       for channel in channels:
           async for msg in User.search_messages(chat_id=channel, query=query):
               name = (msg.text or msg.caption).split("\n")[0]
               if name in results:
                  continue 
               results += f"<b>👉 {name}\n🔎 {msg.link}</b>\n\n"                                                      
       if bool(results)==False:
          movies = await search_imdb(query)
          buttons = []
          for movie in movies: 
              buttons.append([InlineKeyboardButton(movie['title'], callback_data=f"recheck_{movie['id']}")])
          msg = await message.reply("<b>𝐌𝐫 #𝐦𝐞𝐧𝐭𝐢𝐨𝐧 𝐔𝐫 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐌𝐨𝐯𝐢𝐞 👀 𝐎𝐧𝐥𝐢𝐧𝐞 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠 𝐋𝐢𝐧𝐤 𝐍𝐨𝐭 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐫𝐞𝐢𝐠𝐡𝐭 𝐤𝐧𝐨𝐰🥺\n\n𝐆𝐞𝐭 𝐃𝐢𝐫𝐞𝐜𝐭 𝐌𝐨𝐯𝐢𝐞 𝐅𝐢𝐥𝐞📁 𝐈𝐧 𝐁𝐞𝐥𝐨𝐰 𝐆𝐫𝐨𝐮𝐩</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎Ur Movie File Here 🔍", url=f"https://t.me/+5TJUbOMCqD05ZmQ1")]]))
       else:
          msg = await message.reply_text(text=head+results, disable_web_page_preview=True)
       _time = (int(time()) + (15*60))
       await save_dlt_message(msg, _time)
       await save_dlt_message.delete(10)
    except:
       pass
       


@Client.on_callback_query(filters.regex(r"^recheck"))
async def recheck(bot, update):
    clicked = update.from_user.id
    try:      
       typed = update.message.reply_to_message.from_user.id
    except:
       return await update.message.delete(2)       
    if clicked != typed:
       return await update.answer("That's not for you! 👀", show_alert=True)

    m=await update.message.edit("Searching..💥")
    id      = update.data.split("_")[-1]
    query   = await search_imdb(id)
    channels = (await get_group(update.message.chat.id))["channels"]
    head    = "<u>I Have Searched Movie With Wrong Spelling But Take care next time 👇\n\nPowered By </u> <b><I>@CyniteBackup</I></b>\n\n"
    results = ""
    try:
       for channel in channels:
           async for msg in User.search_messages(chat_id=channel, query=query):
               name = (msg.text or msg.caption).split("\n")[0]
               if name in results:
                  continue 
               results += f"<b>🔎 {name}</b>\n👉 {msg.link}</b>\n\n"
       if bool(results)==False:          
          return await update.message.edit("Still no results found! Please Request To Group Admin", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 Request To Admin 🎯", callback_data=f"request_{id}")]]))
       await update.message.edit(text=head+results, disable_web_page_preview=True)
    except Exception as e:
       await update.message.edit(f"❌ Error: `{e}`")


@Client.on_callback_query(filters.regex(r"^request"))
async def request(bot, update):
    clicked = update.from_user.id
    try:      
       typed = update.message.reply_to_message.from_user.id
    except:
       return await update.message.delete()       
    if clicked != typed:
       return await update.answer("That's not for you! 👀", show_alert=True)

    admin = (await get_group(update.message.chat.id))["user_id"]
    id    = update.data.split("_")[1]
    name  = await search_imdb(id)
    url   = "https://www.imdb.com/title/tt"+id
    text  = f"#RequestFromYourGroup\n\nName: {name}\nIMDb: {url}"
    await bot.send_message(chat_id=admin, text=text, disable_web_page_preview=True)
    await update.answer("✅ Request Sent To Admin", show_alert=True)
    await update.message.delete(60)
