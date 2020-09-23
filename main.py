import os
try:
    import telebot
except:
    os.system("pip3 install pyTelegramBotAPI")
    import telebot
from telebot import types
from mybottoken import mytoken
try:
    import mysql.connector
except:
    os.system("pip3 install mysql-connector")
    import mysql.connector
import myhost
import time
from math import ceil
mh = myhost.MyHostForumuzOffline
bot = telebot.TeleBot(mytoken)

def soxa():
    s = [
        'Matematika','Fizika','Kimyo','Java','Python',
        'C++','C#','Linux','Windows','MacOS','Algebra',
        'Geometriya','Chizmachilik','Biologiya','Kino',
        'Android']
    s.sort()
    return s

def button_key(pages=0,N=0,soxa=None,key=None):
    l = len(soxa)
    p = pages*N
    fan={}
    if p<l and key!=None:
        for x in range(0,N+1):
            if (p+x)<l:
                name=f'{key}_{x+1}'
                fan[name]=soxa[p+x]
            else:
                break
    try:         
        return fan
    except:
        pass

def IKB(t=None, c=None):
    return types.InlineKeyboardButton(text=t, callback_data=c)

def fut():
    f = os.path.abspath(__file__)
    m = os.path.getmtime(f)
    t = time.localtime(m)
    str = "%.2d.%.2d.%.4d %.2d:%.2d:%.2d" % (t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec)
    return str

def connects():
    try:
        db = mysql.connector.connect(
            host=mh[0],
            user=mh[1],
            passwd=mh[2],
            auth_plugin=mh[3])
        mydb = db.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS forumuz")
        db.commit()
        mydb.execute("CREATE TABLE IF NOT EXISTS forumuz.users(user_id VARCHAR(15) NOT NULL,onbot tinyint(1) NOT NULL,reyting INT NOT NULL, soxa text)")  
        mydb.execute("CREATE TABLE IF NOT EXISTS forumuz.savol(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,savol text,hashtags text, user_id VARCHAR(15) NOT NULL)") 
        mydb.execute("CREATE TABLE IF NOT EXISTS forumuz.javob(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,javob text, user_id VARCHAR(15) NOT NULL, savol_id INT, javob_id INT, FOREIGN KEY (savol_id) REFERENCES forumuz.savol(id), FOREIGN KEY (javob_id) REFERENCES forumuz.javob(id) )")
        db.commit()
        return db
    except:
        pass
    
def savol_javob(user_id=None,text=None,savol_id=None,javob_id=None,reyting=None, mode=None):
    db = connects()
    mydb = db.cursor()
    if mode=="savol":
        code=f"INSERT INTO forumuz.savol(savol,user_id) VALUES ('{text}','{user_id}')"
    if mode=="javob":
        if savol_id!=None:
            code=f"INSERT INTO forumuz.javob(javob,savol_id,user_id) VALUES ('{text}','{savol_id}','{user_id}')"
        elif javob_id!=None:
            code=f"INSERT INTO forumuz.javob(javob,javob_id,user_id) VALUES ('{text}','{javob_id}','{user_id}')"
    mydb.execute(code)
    db.commit()
    db.close()

def is_new_users(user_id=None, onbot=1, reyting=0):
    try:
        db = connects()
        mydb = db.cursor()
        mydb.execute("SELECT * FROM forumuz.users")
        e1,e2=0,0
        for x in mydb:
            if x[0]==str(user_id):
                e1=1
                if x[1]==0:
                    e2=1
                break
        if e1==0:
            text=f"INSERT INTO forumuz.users(user_id,onbot,reyting) VALUES ('{user_id}',{onbot},{reyting})"
            mydb.execute(text)
            db.commit()
        if e2==1:
            text=f"UPDATE forumuz.users SET onbot={onbot} WHERE user_id='{user_id}'"
            mydb.execute(text)
            db.commit()
        db.close()
    except:
        pass
        
def users():
    try:
        db = connects()
        mydb = db.cursor()
        mydb.execute("SELECT user_id FROM forumuz.users WHERE onbot=1")
        k=[]
        for x in mydb:
            k.append(x[0])
        return k
    except:
        pass 
def helpMessage():
    text = f"Botdan foydalanish:\nOxirgi yangilanish: {fut()}\n* Savolingizni shunday yozavering\n* Savolingizni xato yozdingizmi? Unda savolingizni shunchaki to'g'irlang\n* Javob berish uchun shunchaki \"reply\" qilib yozing\n* Hammasini qilib bo'lgach \"'OK\" tugmasini bosing\n\"Ok\" tugmasini bosgandan keyin o'zgartira olmaysiz\n* Xabaringiz o'chirish uchun \"Bekor qilish\" tugmasini bosing\n* Savolingiz yoki javobingiz yuborilganini tagidagi tugmalar yo'q bo'lib qolganda bilasiz"
    return text
    
def mess(text):
    text2=''
    for x in range(len(text)):
        if text[x]=="'":
            text2+='`'
        else:
            text2+=text[x]
    return text2

def user_soxa(user_id):
    try:
        db = connects()
        mydb = db.cursor(buffered=True)
        s=[]
        mydb.execute(f"SELECT soxa FROM forumuz.users WHERE user_id='{user_id}'")
        for x in mydb:
            if x[0]!=None:
                s=x[0].split(',')
            else:
                s.append('None')
        db.close()
        return s    
    except:
        pass
        
def editor(m,pg=None,edit=None, sb=soxa(),text=None):
    try:
        pass
    except:
        pass
    
def begins(message,edited=None):
    try:
        is_new_users(user_id=message.chat.id)
        mode=''
        savol=0
        try:
            text = message.reply_to_message.text
        except:
            pass
        if message.reply_to_message==None:
            mode = "savol"
            mid = message.message_id
        elif (("#savol" in text) or ("#javob" in text)) and (message.reply_to_message.entities[0].type=="hashtag"):
            mode = "javob"
            mid = message.reply_to_message.message_id
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=mid, text=message.reply_to_message.text)
            except:
                pass
        else:
             pass
        s = user_soxa(message.chat.id)
        sv = types.InlineKeyboardMarkup()
        
        if message.reply_to_message==None:
            if s[0]!=None:
                for x in range(len(s)):
                    sv.add(IKB(t=f"#{s[x]}", c=f"hashtag_{x+1}"))
        
        b1 = IKB(t="Ok",c=f"Ok_{mode}")
        b2 = IKB(t="Bekor qilish",c="cancel")
        sv.add(b1,b2)
        
        if edited==False:
            bot.send_message(chat_id=message.chat.id, text=f"#{mode} {message.text}", reply_markup=sv, reply_to_message_id=mid)
        elif edited==True:
            bot.edit_message_text(chat_id=message.chat.id, message_id=mid+1, text=f"#{mode} {message.text}", reply_markup=sv)
    except:
        pass

def example(m,pg=None,edit=None, sb=soxa(),text=None):
    key = types.InlineKeyboardMarkup()
    pgl=6
    pgn=[0,ceil(len(sb)/pgl)]
    
    bs = [['Tayyor','ok'], ['Bekor qilish','cancel']]
    if pg==None:
        if m.text[:2].isdigit()==True:
            cpg = int(m.text[:2])
        else:
            cpg=1
            
    elif pg == 'n':
        cpg = int(m.text[:2])+1
    elif pg == 'p':
        cpg = int(m.text[:2])-1
        
    if cpg < pgn[0]+1:
        cpg = pgn[1] 
    elif cpg > pgn[1]:
        cpg = pgn[0]+1
    names = button_key(pages=cpg-1,N=pgl,soxa=sb, key='fan')
    keys = list(names.keys())
    base = '%.2d. Yo\'nalish tanlang:' % cpg
    rem=0
    if len(m.text[len(base):])==0:
        fanlar = ''
    else:
        fanlar = m.text[len(base):]
        st = fanlar.split('\n')
        if text!=None:
            if names[text] in st:
                rem=1
    for x in range(len(keys)):
        key.add(IKB(t=names[keys[x]], c=keys[x]))
    key.add(IKB(t='<',c='p') , IKB(t=f'{cpg}-sahifa',c='center') , IKB(t='>',c='n') )
    key.add(IKB(t=bs[0][0], c=bs[0][1]),IKB(t=bs[1][0], c=bs[1][1]))
    
    if text==None and pg==None:
        txt = base
    elif text==None and pg!=None:
        txt = base + fanlar
    elif text!=None and pg==None:
        if len(base)==len(m.text):
            txt = base + '\n' + names[text]
        elif rem==0:
            txt = base + fanlar + '\n' + names[text]
        elif rem==1:
            fanlar=''
            for y in range(len(st)):
                if names[text]!=st[y] and st[y]!='':
                    fanlar+='\n'+st[y]
                
            txt = base + fanlar    
    if edit==None:
        bot.send_message(m.chat.id,txt,reply_markup=key)
    elif edit!=None:
        bot.edit_message_text(chat_id=m.chat.id, message_id=edit, text=txt, reply_markup=key)

        
@bot.message_handler(commands=["start"])
def starts(m):
    bot.send_message(m.chat.id, f"Assalomu alaykum {m.from_user.first_name}")
    is_new_users(user_id=m.chat.id)
    bot.send_message(m.chat.id,helpMessage())
    
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, helpMessage())

@bot.message_handler(commands=['soxa'])
def soxalar(message):
    example(message)

@bot.message_handler(commands=['get_soxa'])
def gs(m):
    k = user_soxa(m.chat.id)
    for x in k:
        bot.send_message(m.chat.id,x)

@bot.message_handler(content_types=["text"])
def standart(message):
    begins(message, edited=False)

@bot.edited_message_handler(content_types=["text"])
def edited(message):
    begins(message, edited=True)

@bot.callback_query_handler(func=lambda call: True)
def tasdiq(call):
    if call.message:
        if call.data[:4]=='fan_':
            example(m=call.message, edit=call.message.message_id, sb=soxa() , text=call.data)
        
        elif call.data[:8]=='hashtag_':
            editor(m=call.message, edit=call.message.message_id, sb=user_soxa(call.message.chat.id) ,text=call.data)
        elif call.data=='ok':
            try:
                db = connects()
                mydb = db.cursor()
                mess = call.message.text[call.message.text.rfind(':')+2:].replace('\n',',')
                print(mess)
                mydb.execute(f"UPDATE forumuz.users SET soxa='{mess}' WHERE user_id='{call.message.chat.id}'")
                db.commit()
                db.close()
                bot.send_message(call.message.chat.id, mess)
                bot.delete_message(call.message.chat.id,call.message.message_id)
            except:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='Xatolik')
            
        elif call.data=='n':
            example(m=call.message, pg='n', edit=call.message.message_id)
        elif call.data=='p':
            example(m=call.message, pg='p', edit=call.message.message_id)
        elif call.data=="Ok_savol":
            db = connects()
            mydb = db.cursor()
            u=users()
            key = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(text="Bilmayman", callback_data="Delete")
            key.add(but1)
            for x in u:
                if int(x)!=call.message.chat.id:
                    try:
                        bot.send_message(int(x),f"\"{call.message.chat.first_name}\" dan\n{call.message.text}",reply_markup=key)
                        print('ok_savol')
                    except:
                        bot.send_message(call.message.chat.id,f"{x} id egasi mavjud emas")
                        mydb.execute(f"UPDATE forumuz.users SET onbot=0 WHERE user_id={x}")
                        db.commit()
            db.close()
            savol_javob(mode="savol",user_id=call.message.chat.id,text=mess(call.message.text)[7:])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
            bot.answer_callback_query(callback_query_id=call.id,show_alert=False, text="Savol barcha bot foydalanuvchilariga yuborildi")
        elif call.data=="Ok_javob":
            db = connects()
            mydb = db.cursor()
            key = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(text=u"\U0001F44D +1",callback_data="Up")
            but2 = types.InlineKeyboardButton(text="0",callback_data="Neytral")
            but3 = types.InlineKeyboardButton(text=u"\U0001F44E -1",callback_data="Down")
            key.add(but1,but2,but3)
            txt = call.message.reply_to_message.text
            txt = txt[txt.find('\n')+1:]
            print(txt)
            if ('#savol' in txt):
                mydb.execute("SELECT id,savol,user_id FROM forumuz.savol")
                for x in mydb:
                    print(x)
                    if x[1]==txt[7:] and x[2]!=str(call.message.chat.id):
                        try:
                            bot.send_message(int(x[2]),f"\"{call.message.chat.first_name}\" dan\n{call.message.text}",reply_markup=key)
                            print('ok_javob')
                        except:
                            bot.send_message(call.message.chat.id,"savol egasi botda foydalanishni to\'xtatgan")
                            mydb.execute(f"UPDATE forumuz.users SET onbot=0 WHERE user_id={x[2]}")
                            db.commit()
                        break
                savol_javob(mode="javob",user_id=call.message.chat.id,savol_id=x[0],text=mess(call.message.text)[7:])
                bot.answer_callback_query(callback_query_id=call.id,show_alert=False, text="Javob savol beruvchiga yuborildi")
            elif ('#javob' in txt):
                mydb.execute("SELECT * FROM forumuz.javob")
                for x in mydb:
                    if x[1]==txt[7:] and x[2]!=str(call.message.chat.id):
                        try:
                            bot.send_message(int(x[2]),f"\"{call.message.chat.first_name}\" dan\n{call.message.text}",reply_markup=key)
                            print('ok_javob')
                        except:
                            bot.send_message(call.message.chat.id,"savol egasi botda foydalanishni to\'xtatgan")
                            mydb.execute(f"UPDATE forumuz.users SET onbot=0 WHERE user_id={x[2]}")
                            db.commit()
                        break
                savol_javob(mode="javob",user_id=call.message.chat.id,javob_id=x[0],text=mess(call.message.text)[7:])
                bot.answer_callback_query(callback_query_id=call.id,show_alert=False, text="Javobga xabar yuborildi")
            db.close()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=call.message.text)
            
            
        elif call.data=="cancel":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Bekor qilindi')
            
        elif call.data in ["Up", "Neytral", "Down"] :
            db = connects()
            mydb = db.cursor(buffered=True)
            if call.data=="Up":
                k=1
            elif call.data=="Neytral":
                k=0
            elif call.data=="Down":
                k=-1
            txt = call.message.text
            txt = txt[txt.find('\n')+8:]
            user_id=0
            mydb.execute(f"SELECT * FROM forumuz.javob WHERE javob='{txt}'")
            for y in mydb:
                print(y)
                user_id = y[2]
                break
            #print(user_id, type(user_id))
            
            mydb.execute(f"SELECT * FROM forumuz.users WHERE user_id={user_id}")
            reyting=0
            for x in mydb:
                print(x)
                reyting = x[2]+k
                break
            #print(reyting)
            
            mydb.execute(f"UPDATE forumuz.users SET reyting={reyting} WHERE user_id='{user_id}'")
            db.commit()
            db.close()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=call.message.text)


if __name__=='__main__':
    bot.polling(none_stop=True)
