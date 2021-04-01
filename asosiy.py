import telebot
from PIL import Image
from telebot.types import KeyboardButton,ReplyKeyboardMarkup
import db
token='1784956442:AAGOQU9yTFjIAnZyI-ZZa76RYLpvApUsF-0'
bot=telebot.TeleBot(token=token)
tasdiq_btn=["Ha","Yo'q"]
middile_1_Main_buttons=['Sotib olish','Sotish','Asosiy menyuga qaytish']
middile_2_Main_buttons=['Ish joyi kerak','Ishchi kerak','Shogirt Kerak','Sherik kerak','Ustoz kerak','Asosiy menyuga qaytish']
main_btn=['Savdo','Ish']
DB=db.PostgresDB()
def mid1_maker(markup):
    _list = []
    for i in range(0, len(middile_1_Main_buttons)):
        _list.append(KeyboardButton(middile_1_Main_buttons[i]))
    markup.add(*_list)
    markup.resize_keyboard = True
    return markup

def mid2_maker(markup):
    _list = []
    for i in range(0, len(middile_2_Main_buttons)):
        _list.append(KeyboardButton(middile_2_Main_buttons[i]))
    markup.add(*_list)
    markup.resize_keyboard = True
    return markup
def TasdiqMaker(markup):
    _list=[]
    for i in range(len(tasdiq_btn)):
	    _list.append(KeyboardButton(tasdiq_btn[i]))
    markup.add(*_list)
    markup.resize_keyboard=True
    return markup
def mainmaker(markup):
    _list=[]
    for i in range(len(main_btn)):
        _list.append(KeyboardButton(main_btn[i]))
    markup.add(*_list)
    markup.resize_keyboard=True
    return markup
@bot.message_handler(commands=['start'])
def StartTing(message):
	user=DB.getuser(message.chat.id)
	m=ReplyKeyboardMarkup(row_width=2)
	m=mainmaker(m)
	if user!=None:
		bot.send_message(message.chat.id,text='Assalomu alaykum hurmatli foydalanuvchi qaytganizdan mamnunmiz !',reply_markup=m)
	else:
		DB.addUser(message.chat.id)
		bot.send_message(message.chat.id,"Assalomu alaykum hurmatli foydalanuvchi xush kelibsiz",reply_markup=m)
@bot.message_handler(func=lambda message:message.text in main_btn)
def mainhandler(message):
    if message.text=='Ish':
        markup=ReplyKeyboardMarkup(row_width=2)
        markup=mid2_maker(markup)
        bot.send_message(message.chat.id,text="Ish to'g'risida e'lon berish uchun tanlang",reply_markup=markup)
    if message.text=='Savdo':
        markup=ReplyKeyboardMarkup(row_width=2)
        markup=mid1_maker(markup)
        bot.send_message(message.chat.id,text="Savdo to'g'risida e'lon berish uchun tanlang",reply_markup=markup)
@bot.message_handler(func=lambda message:message.text=='Asosiy menyuga qaytish')
def backmain(message):
    markup=ReplyKeyboardMarkup(row_width=2)
    markup=mainmaker(markup)
    bot.send_message(message.chat.id,text='Asosiy menyu',reply_markup=markup)
@bot.message_handler(func=lambda message:message.text in middile_2_Main_buttons)
def midd_main_2_handler(message):
	DB.vqdbishCLear(tg_id=message.chat.id)
	DB.vqdbishadd(message.chat.id)
	DB.vqdbSotuvCLear(message.chat.id)
	DB.vqdbIshSetLastMessage(message.chat.id,'full_name')
	DB.EnterTypeIsh(tg_id=message.chat.id,text=message.text)
	DB.EnterUserNameIsh(message.chat.id,text=message.from_user.username)
	bot.send_message(message.chat.id,text='Ish Sharifingizni kiriting  👇')
@bot.message_handler(func=lambda message:message.text in middile_1_Main_buttons)
def midd_main_1_handler(message):
	DB.vqdbSotuvCLear(tg_id=message.chat.id)
	DB.vqdbsotuvadd(message.chat.id)
	DB.vqdbishCLear(message.chat.id)
	DB.vqdbSotuvSetLastMessage(message.chat.id,'full_name')
	DB.EnterTypeSotuv(tg_id=message.chat.id,text=message.text)
	DB.EnterUserNameSotuv(message.chat.id,text=message.from_user.username)
	bot.send_message(message.chat.id,text='Ish Sharifingizni kiriting  👇')
@bot.message_handler(func=lambda message:DB.GetLastMessageSotuv(message.chat.id)[0]=='full_name')
def SaveFull_name(message):
	DB.altertablesotuv(message.chat.id,message.text)
	if DB.GetTypeSotuv(message.chat.id)=='Sotish':
		bot.send_message(message.chat.id,"Sotiladigan narsa nomini kiriting 👇")
	else:
		bot.send_message(message.chat.id,"Sotib olinadigan narsa nomini kiriting 👇")
	DB.vqdbSotuvSetLastMessage(message.chat.id,'tovar')
@bot.message_handler(func=lambda message:DB.GetLastMessageSotuv(message.chat.id)[0]=='tovar')
def SaveTovar(message):
	markup=ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
	m=KeyboardButton('Keyingi')
	markup.add(m)
	DB.altertablesotuv(message.chat.id,message.text)
	typ=DB.GetTypeSotuv(message.chat.id)[0]
	if typ=='Sotish':
		bot.send_message(message.chat.id,"Sotiladigan narsa haqida rasm bo'lsa jo'nating yoki Keyingi tugmasini bosing 👇",reply_markup=markup)
	else:
		bot.send_message(message.chat.id,"Sotib olinadigan narsa haqida rasm bo'lsa jo'nating yoki Keyingi tugmasini bosing 👇",reply_markup=markup)
	DB.vqdbSotuvSetLastMessage(message.chat.id,'photo_path')
@bot.message_handler(func=lambda message:DB.GetLastMessageSotuv(message.chat.id)[0]=='photo_path',content_types=['photo'])		
def SavePhotoPath(message):
	markup=ReplyKeyboardMarkup(row_width=2)
	markup=mid1_maker(markup)
	file_ID=message.photo[-1].file_id
	file_path=bot.get_file(file_ID).file_path
	DB.altertablesotuv(message.chat.id,file_path)
	bot.send_message(message.chat.id,'Aloqa uchun tel raqamingizni kiriting 👇',reply_markup=markup)
	DB.vqdbSotuvSetLastMessage(message.chat.id,'tel')
@bot.message_handler(func=lambda message:DB.GetLastMessageSotuv(message.chat.id)[0]=='photo_path' and message.text=='Keyingi')
def SaveKeyingi(message):
	markup=ReplyKeyboardMarkup(row_width=2)
	markup=mid1_maker(markup)
	DB.altertablesotuv(message.chat.id,'None')
	bot.send_message(message.chat.id,'Aloqa uchun tel raqamingizni kiriting 👇',reply_markup=markup)
	DB.vqdbSotuvSetLastMessage(message.chat.id,'tel')
@bot.message_handler(func=lambda message:DB.GetLastMessageSotuv(message.chat.id)[0]=='tel')
def SaveTelToSotuv(message):
	DB.altertablesotuv(message.chat.id,message.text)
	bot.send_message(message.chat.id,'Manzilingizni kiriting 👇')
	DB.vqdbSotuvSetLastMessage(message.chat.id,'manzil')
@bot.message_handler(func=lambda message:DB.GetLastMessageSotuv(message.chat.id)[0]=='manzil')
def SaveManzil(message):
	DB.altertablesotuv(message.chat.id,message.text)
	bot.send_message(message.chat.id,'Narxini kiriting 👇')
	DB.vqdbSotuvSetLastMessage(message.chat.id,'narx')
@bot.message_handler(func=lambda message:DB.GetLastMessageSotuv(message.chat.id)[0]=='narx')
def SaveNarxToSotuv(message):
	DB.altertablesotuv(message.chat.id,message.text)
	bot.send_message(message.chat.id,"Qo'shimcha ma'lumotlar bo'lsa kiriting 👇")
	DB.vqdbSotuvSetLastMessage(message.chat.id,'qoshimcha')
@bot.message_handler(func=lambda message:DB.GetLastMessageSotuv(message.chat.id)[0]=='qoshimcha')
def SaveQoshimchaToSotuv(message):
	markup=ReplyKeyboardMarkup(row_width=2)
	markup=TasdiqMaker(markup)
	DB.altertablesotuv(message.chat.id,message.text)
	res=DB.ReadySotuvPost(message.chat.id)
	DB.vqdbSotuvSetLastMessage(message.chat.id,'send')
	for i in res:
		try:
			res[i]=res[i].replace("@!","'")
		except Exception as e:
			e
	if res['type']=='Sotish':
		Posts=f"""
		Sotiladi

		🙎‍♂️ Sotuvchi  :  {res['full_name']}
		📦 Sotiladi  :  {res['tovar']}"""
		if res['username']!='None':
			Posts=Posts+f"""
		📡 Username : @{res['username']}"""
		Posts=Posts+f"""
		☎️ Tel :  {res['tel']}
		🌐 Manzil : {res['manzil']}
		💰 Narx : {res['narx']}
		📌Qo'shimcha ma'lumotlar : {res['qoshimcha']} 
		
		Kanal : @Elon_bor1
		"""
		filepath=res['photo_path']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		bot.send_photo(message.chat.id,img,Posts)
		bot.send_message(message.chat.id,text="Hamma ma'lumotlar to'g'ri bo'lsa Ha tugmasini bosing va Post Adminga yuboriladi",reply_markup=markup)
	else:
		Posts=f"""
		Sotib olinadi

		🙎‍♂️ Xaridor :  {res['full_name']}
		📦 Sotib olinadi  :  {res['tovar']}"""
		if res['username']!='None':
			Posts=Posts+f"""
		📡 Username : @{res['username']}"""
		Posts=Posts+f"""
		☎️ Tel :  {res['tel']}
		🌐 Manzil : {res['manzil']}
		💰 Narx : {res['narx']}
		📌Qo'shimcha ma'lumotlar : {res['qoshimcha']} 
		
		Kanal : @Elon_bor1
		"""
		filepath=res['photo_path']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		bot.send_photo(message.chat.id,img,Posts)
		bot.send_message(message.chat.id,text="Hamma ma'lumotlar to'g'ri bo'lsa Ha tugmasini bosing va Post Adminga yuboriladi",reply_markup=markup)
@bot.message_handler(func=lambda message:DB.GetLastMessageSotuv(message.chat.id)[0]=='send' and message.text in tasdiq_btn)
def Savearchieve(message):
	markup=ReplyKeyboardMarkup(row_width=2)
	markup=mainmaker(markup)
	if message.text=="Yo'q":
		DB.vqdbSotuvCLear(message.chat.id)
		bot.send_message(message.chat.id,'Qabul qilinmadi',reply_markup=markup)
	else:
		res=DB.ReadySotuvPost(message.chat.id)
		DB.SaveArchieveSotuv(message.chat.id,res['full_name'],res['tovar'],res['tel'],res['manzil'],res['narx'],res['qoshimcha'],res['type'],res['username'])
		if res['type']=='Sotish':
			Posts=f"""
		Sotiladi

		🙎‍♂️ Sotuvchi  :  {res['full_name']}
		📦 Sotiladi  :  {res['tovar']}"""
			if res['username']!='None':
				Posts=Posts+f"""
		📡 Username : @{res['username']}"""
			Posts=Posts+f"""
		☎️ Tel :  {res['tel']}
		🌐 Manzil : {res['manzil']}
		💰 Narx : {res['narx']}
		📌Qo'shimcha ma'lumotlar : {res['qoshimcha']} 
		
		Kanal : @Elon_bor1
		"""
			filepath=res['photo_path']
			if filepath=='None':
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
			else:
				try:
					img=bot.download_file(file_path=filepath)
				except Exception as e:
					img=Image.open('img/elon.jpg')
					img=img.resize((270,200),Image.ANTIALIAS)
			bot.send_photo(-537935048,img,Posts)
			bot.send_message(message.chat.id,"Ma'lumotlar adminga jo'natildi tasdiqlansa kanalga chiqadi",reply_markup=markup)
		else:
			Posts=f"""
		Sotib olinadi

		🙎‍♂️ Xaridor :  {res['full_name']}
		📦 Sotib olinadi  :  {res['tovar']}"""
			if res['username']!='None':
				Posts=Posts+f"""
		📡 Username : @{res['username']}"""
			Posts=Posts+f"""
		☎️ Tel :  {res['tel']}
		🌐 Manzil : {res['manzil']}
		💰 Narx : {res['narx']}
		📌Qo'shimcha ma'lumotlar : {res['qoshimcha']} 
		
		Kanal : @Elon_bor1
		"""
			filepath=res['photo_path']
			if filepath=='None':
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
			else:
				try:
					img=bot.download_file(file_path=filepath)
				except Exception as e:
					img=Image.open('img/elon.jpg')
					img=img.resize((270,200),Image.ANTIALIAS)
			bot.send_photo(-537935048,img,Posts)
			bot.send_message(message.chat.id,text="Ma'lumotlar adminga jo'natildi tasdiqlansa kanalga chiqadi",reply_markup=markup)
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='full_name')
def savefull_nameish(message):
    DB.altertableish(message.chat.id,message.text)
    bot.send_message(message.chat.id,"Yoshingizni kiriting  👇")
    DB.vqdbIshSetLastMessage(message.chat.id,'yosh')
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='yosh')
def saveyosh(message):
    DB.altertableish(message.chat.id,message.text)
    bot.send_message(message.chat.id,'Ish turini kiriting 👇 Masalan :(Usta Duradgor)')
    DB.vqdbIshSetLastMessage(message.chat.id,'ishturi')
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='ishturi')
def saveishturi(message):
	DB.altertableish(message.chat.id,message.text)
	markup=ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
	m=KeyboardButton('Keyingi')
	markup.add(m)
	bot.send_message(message.chat.id,"Ishga oid rasm bo'lsa jo'nating (faqat bir dona) 👇 (agar jo'natishni hohlamasangiz Keyingini bosing)",reply_markup=markup)
	DB.vqdbIshSetLastMessage(message.chat.id,'pathphoto')
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='pathphoto' and message.text=='Keyingi')
def KeyingSave(message):
	DB.altertableish(message.chat.id,'None')
	markup=ReplyKeyboardMarkup(row_width=2)
	markup=mid2_maker(markup)
	bot.send_message(message.chat.id,"Aloqa uchun tel raqamingizni kiriting 👇",reply_markup=markup)
	DB.vqdbIshSetLastMessage(message.chat.id,'tel')
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='pathphoto',content_types=['photo'])
def imgwriteish(message):
	markup=ReplyKeyboardMarkup(row_width=2)
	markup=mid2_maker(markup)
	file_ID=message.photo[-1].file_id
	file_path=bot.get_file(file_ID).file_path
	DB.altertableish(message.chat.id,file_path)
	bot.send_message(message.chat.id,"Aloqa uchun tel raqamingizni kiriting 👇",reply_markup=markup)
	DB.vqdbIshSetLastMessage(message.chat.id,'tel')
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='tel')
def savetel(message):
    DB.altertableish(message.chat.id,message.text)
    bot.send_message(message.chat.id,"Hududingizni kiriting 👇")
    DB.vqdbIshSetLastMessage(message.chat.id,'hudud')
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='hudud')
def savehudud(message):
    DB.altertableish(message.chat.id,message.text)
    bot.send_message(message.chat.id,"Narxini kiriting 👇")
    DB.vqdbIshSetLastMessage(message.chat.id,'narxi')
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='narxi')
def savenarx(message):
    DB.altertableish(message.chat.id,message.text)
    bot.send_message(message.chat.id, "Murojaat qilish vaqtini kiriting 👇")
    DB.vqdbIshSetLastMessage(message.chat.id,'vaqt')
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='vaqt')
def savevaqt(message):
    DB.altertableish(message.chat.id,message.text)
    bot.send_message(message.chat.id,"Qo'shimcha ma'lumotlar bo'lsa kiriting 👇")
    DB.vqdbIshSetLastMessage(message.chat.id,'qoshimcha')
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='qoshimcha')
def saveqoshimcha(message):
	DB.altertableish(message.chat.id,message.text)
	res=DB.ReadyIshPost(message.chat.id)
	for i in res:
		try:
			res[i]=res[i].replace("@!","'")
		except Exception as e:
			e
	if res['type']=='Ish joyi kerak':
		Posts=f"""
	 Ish joyi kerak

	👨‍✈️ Ism sharif  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}
	
	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=TasdiqMaker(markup)
		DB.vqdbIshSetLastMessage(message.chat.id,text='send')
		bot.send_photo(message.chat.id,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Hamma ma'lumotlar to'g'ri bo'lsa Ha tugmasini bosing va Post Adminga yuboriladi",reply_markup=markup)
	if res['type']=='Ishchi kerak':
		Posts=f"""
	 Ishchi kerak

	👨‍✈️ Mas'ul shaxs  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}

	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=TasdiqMaker(markup)
		DB.vqdbIshSetLastMessage(message.chat.id,text='send')
		bot.send_photo(message.chat.id,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Hamma ma'lumotlar to'g'ri bo'lsa Ha tugmasini bosing va Post Adminga yuboriladi",reply_markup=markup)
	if res['type']=='Shogirt Kerak':
		Posts=f"""
	 Shogirt kerak

	👨‍✈️ Ustoz  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}
	
	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception  as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=TasdiqMaker(markup)
		DB.vqdbIshSetLastMessage(message.chat.id,text='send')
		bot.send_photo(message.chat.id,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Hamma ma'lumotlar to'g'ri bo'lsa Ha tugmasini bosing va Post Adminga yuboriladi",reply_markup=markup)
	if res['type']=='Sherik kerak':
		Posts=f"""
	 Sherik kerak

	👨‍✈️ Sherik  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}
	
	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=TasdiqMaker(markup)
		DB.vqdbIshSetLastMessage(message.chat.id,text='send')
		bot.send_photo(message.chat.id,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Hamma ma'lumotlar to'g'ri bo'lsa Ha tugmasini bosing va Post Adminga yuboriladi",reply_markup=markup)
	if res['type']=='Ustoz kerak':
		Posts=f"""
	 Ustoz kerak

	👨‍✈️ Shogirt  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}

	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=TasdiqMaker(markup)
		DB.vqdbIshSetLastMessage(message.chat.id,text='send')
		bot.send_photo(message.chat.id,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Hamma ma'lumotlar to'g'ri bo'lsa Ha tugmasini bosing va Post Adminga yuboriladi",reply_markup=markup)
@bot.message_handler(func=lambda message:DB.GetLastMessageIsh(message.chat.id)[0]=='send' and message.text in tasdiq_btn)
def savearchieveandsend(message):
	if message.text=="Yo'q":
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=mainmaker(markup)
		bot.send_message(message.chat.id,'Qabul qilinmadi',reply_markup=markup)
		DB.vqdbishCLear(message.chat.id)
		return	
	res=DB.ReadyIshPost(message.chat.id)	
	DB.SaveArchieveIsh(message.chat.id,res['full_name'],res['yosh'],res['ishturi'],res['pathphoto'],res['username'],res['tel'],res['hudud'],res['narxi'],res['vaqt'],res['qoshimcha'],res['type'])
	for i in res:
		try:
			res[i]=res[i].replace("@!","'")
		except Exception as e:
			e
	if res['type']=='Ish joyi kerak':
		Posts=f"""
	 Ish joyi kerak

	👨‍✈️ Ism sharif  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}

	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=mainmaker(markup)
		bot.send_photo(-537935048,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Post adminga jo'natildi agar admin tasdiqlasa kanalga chiqadi",reply_markup=markup)
		DB.vqdbishCLear(message.chat.id)
	if res['type']=='Ishchi kerak':
		Posts=f"""
	 Ishchi kerak

	👨‍✈️ Mas'ul shaxs  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}
	
	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=mainmaker(markup)
		bot.send_photo(-537935048,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Post adminga jo'natildi agar admin tasdiqlasa kanalga chiqadi",reply_markup=markup)
		DB.vqdbishCLear(message.chat.id)
	if res['type']=='Shogirt Kerak':
		Posts=f"""
	 Shogirt kerak

	👨‍✈️ Ustoz  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}
	
	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=mainmaker(markup)
		bot.send_photo(-537935048,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Post adminga jo'natildi agar admin tasdiqlasa kanalga chiqadi",reply_markup=markup)
		DB.vqdbishCLear(message.chat.id)
	if res['type']=='Sherik kerak':
		Posts=f"""
	 Sherik kerak

	👨‍✈️ Sherik  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}
	
	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=mainmaker(markup)
		bot.send_photo(-537935048,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Post adminga jo'natildi agar admin tasdiqlasa kanalga chiqadi",reply_markup=markup)
		DB.vqdbishCLear(message.chat.id)
	if res['type']=='Ustoz kerak':
		Posts=f"""
	 Ustoz kerak

	👨‍✈️ Shogirt  :  {res['full_name']}
	📆 Yosh  :  {res['yosh']}
	🛠  Ish turi  :  {res['ishturi']}"""
		if res['username']!='None':
			Posts=Posts+f"""
	📡Username : @{res['username']}"""
		Posts=Posts+f"""
	☎️ Tel : {res['tel']}
	🌐 Hudud : {res['hudud']}
	💰 Narx  :  {res['narxi']}
	⏰ Murojaat qilish vaqti :  {res['vaqt']}
	📌 Qo'shimcha : {res['qoshimcha']}
	
	Kanal : @Elon_bor1
	"""
		filepath=res['pathphoto']
		if filepath=='None':
			img=Image.open('img/elon.jpg')
			img=img.resize((270,200),Image.ANTIALIAS)
		else:
			try:
				img=bot.download_file(file_path=filepath)
			except Exception as e:
				img=Image.open('img/elon.jpg')
				img=img.resize((270,200),Image.ANTIALIAS)
		markup=ReplyKeyboardMarkup(row_width=2)
		markup=mainmaker(markup)
		bot.send_photo(-537935048,photo=img,caption=Posts)
		bot.send_message(message.chat.id,text="Post adminga jo'natildi agar admin tasdiqlasa kanalga chiqadi",reply_markup=markup)
		DB.vqdbishCLear(message.chat.id)

bot.polling()