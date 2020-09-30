import telebot
from telebot import types
from mybottoken import mytoken
import sqlite3
import os
import time
from math import ceil
bot = telebot.TeleBot(mytoken)

def soxa():
    s = [
        'Matematika','Fizika','Kimyo','Java','Python','C++',
        'C#','Linux','Windows','MacOS','Biologiya','Geografiya'
        'Telegram_Bot','Android','Informatika'
        ]
    s.sort()
    return s

def button_key(pages=0,N=0,soxa=None,key=None):
    l = len(soxa)
    p = pages*N
    fan={}
    if p<=l and key!=None:
        for x in range(0,N):
            if (p+x)<l:
                name=f'{key}_{x}'
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
        i=1
        db = sqlite3.connect('forumuz.db')
        i=2
        mydb = db.cursor()
        i=3
        mydb.execute("CREATE TABLE IF NOT EXISTS users(user_id text NOT NULL,onbot INTEGER NOT NULL,reyting INTEGER NOT NULL, soxa text);")
        i=4
        db.commit()
        i=5
        mydb.execute("CREATE TABLE IF NOT EXISTS savol(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,savol text,hashtags text, user_id text NOT NULL);")
        i=6
        db.commit()
        i=7
        mydb.execute("CREATE TABLE IF NOT EXISTS javob(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,javob text, user_id text NOT NULL, savol_id INTEGER, javob_id INTEGER, FOREIGN KEY (savol_id) REFERENCES savol(id), FOREIGN KEY (javob_id) REFERENCES javob(id) );")
        i=8
        db.commit()
        #print('connected')
        return db
    except:
        pass
    #print(i)

def hashtags(m):
    a = m.find(':\n')
    b = m.rfind(';\n')
    if a==-1 or b==-1:
        return 0
    return m[a+2:b]

def savol_javob(user_id=None,text=None,savol_id=None,javob_id=None,reyting=None, mode=None):
    db = connects()
    #print(text)
    ht = hashtags(text)
    #print(ht)
    mydb = db.cursor()
    text = shifr(mode='shifr',t=text[text.rfind(';\n')+2:])
    if mode=="savol":
        code=f"INSERT INTO savol(savol,hashtags,user_id) VALUES ('{text}','{ht}','{user_id}');"
    if mode=="javob":
        if savol_id!=None:
            code=f"INSERT INTO javob(javob,savol_id,user_id) VALUES ('{text}','{savol_id}','{user_id}');"
        elif javob_id!=None:
            code=f"INSERT INTO javob(javob,javob_id,user_id) VALUES ('{text}','{javob_id}','{user_id}');"
    mydb.execute(code)
    db.commit()
    db.close()

def shifr(mode=None, t=None):
    if mode=='shifr':
        return t.encode('utf-8').hex()
    elif mode=='deshifr':
        return bytes.fromhex(t).decode('utf-8')

def is_new_users(user=None, onbot=1, reyting=0):
    try:
        user_id=user.chat.id
        db = connects()
        mydb = db.cursor()
        mydb.execute("SELECT * FROM users;")
        e1,e2=0,0
        for x in mydb:
            if x[0]==str(user_id):
                e1=1
                if x[1]==0:
                    e2=1
                break
        if e1==0:
            text=f"INSERT INTO users(user_id,onbot,reyting) VALUES ('{user_id}',{onbot},{reyting});"
            mydb.execute(text)
            db.commit()
            example(user)
        if e2==1:
            text=f"UPDATE users SET onbot={onbot} WHERE user_id='{user_id}';"
            mydb.execute(text)
            db.commit()
        db.close()
    except:
        bot.send_message(578017143, f'Bot kodida xatolik, [USER!](tg://user?id={user_id}) foydalanuvchi qo\'shilmadi', parse_mode='MARKUP')

def users():
    try:
        db = connects()
        mydb = db.cursor()
        mydb.execute("SELECT user_id FROM users WHERE onbot=1;")
        k=[]
        z = mydb.fetchall()
        for x in z:
            k.append(x[0])
        return k
    except:
        pass

def helpMessage():
    text = f'''
Botdan foydalanish:
Oxirgi yangilanish: {fut()}
* Savolingizni shunday yozavering
* Savolingizni xato yozdingizmi? Unda savolingizni shunchaki to'g'irlang
* Javob berish uchun shunchaki \"reply\" qilib yozing
* Hammasini qilib bo'lgach \"'OK\" tugmasini bosing
\"Ok\" tugmasini bosgandan keyin o'zgartira olmaysiz
* Xabaringiz o'chirish uchun \"Bekor qilish\" tugmasini bosing
* Savolingiz yoki javobingiz yuborilganini tagidagi tugmalar yo'q bo'lib qolganda bilasiz

!!! Botda muammo yoki taklifingiz bo\'lsa,
/adminga "xabar" jo\'nating '''
    return text

def user_soxa(user_id):
    try:
        db = connects()
        mydb = db.cursor()
        s=[]
        mydb.execute(f"SELECT soxa FROM users WHERE user_id='{user_id}';")
        x = mydb.fetchone()
        if x[0]!=None:
            s=x[0].split(';')
            s=[s[x] for x in range(len(s)) if s[x]!='']
        else:
            s.append('empty')
        db.close()
        return s
    except:
        pass

def qolip(text=None, hashtag=None):
    #print(text)
    l = len(text)
    d = text.find(':')
    head = text[:d+1]
    f = text.rfind(';')
    k=d-l+1
    if f==-1:
        if k!=0:
            foot = text[d+1:]
        else:
            foot = ''
    else:
        foot = text[f+1:]
    hash = text[len(head):l-len(foot)]
    #print(l, len(head), len(hash), len(foot), f)
    if f!=-1:
        if hashtag in hash:
            hash = hash[:hash.find(hashtag)]+hash[hash.find(hashtag)+len(hashtag):]
        else:
            hash = hash+hashtag
    else:
        hash = hash+hashtag
    txt = head + hash + foot
    return txt

def begins(m,edited=None,k=None):
    is_new_users(user=m)
    try:
        text = m.reply_to_message.text
    except:
        text = m.text
    mode = "savol"
    mid = m.message_id
    s = user_soxa(m.chat.id)
    #print(s)
    if (("#savol" in text) or ("#javob" in text)) and (m.reply_to_message.entities[0].type=="hashtag"):
        mode = "javob"
        mid = m.reply_to_message.message_id
        s=['empty']
        try:
            bot.edit_message_text(chat_id=m.chat.id, message_id=mid, text=m.reply_to_message.text)
        except:
            pass
    else:
         pass

    sv = types.InlineKeyboardMarkup()
    if s[0]!='empty':
        for x in range(len(s)):
            sv.add(IKB(t=f"{s[x]}", c=f"hashtag_{x}"))
    sv.add(IKB(t="Ok",c=f"Ok_{mode}"), IKB(t="Bekor qilish",c="cancel"))
    base = f"#{mode}:\n{m.text}"
    if edited==False:
        txt = base
        bot.send_message(chat_id=m.chat.id, text=txt, reply_markup=sv, reply_to_message_id=mid)
    elif edited==True:
        try:
            txt = qolip(text=m.text, hashtag='\n#'+s[k]+';')
            bot.edit_message_text(chat_id=m.chat.id, message_id=mid, text=txt, reply_markup=sv)
        except:
            pass

def example(m,pg=None,edit=None, sb=soxa(),text=None):
    key = types.InlineKeyboardMarkup()
    pgl=6
    pgn=[0,ceil(len(sb)/pgl)]
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
    base = '%.2d. Yo\'nalish tanlang:\n' % cpg
    for x in range(len(keys)):
        key.add(IKB(t=names[keys[x]], c=keys[x]))
    key.add(IKB(t='<',c='p') , IKB(t=f'{cpg}-sahifa',c='center') , IKB(t='>',c='n') )
    key.add(IKB(t='Tayyor', c='ok'),IKB(t='Bekor qilish', c='cancel'))


    a = base+m.text[len(base):]
    if edit==None:
        txt = base
        bot.send_message(m.chat.id,txt,reply_markup=key)
    elif edit!=None:
        if text==None:
            txt = a
        else:
            print('>>',names[text])
            txt = qolip(text=a, hashtag='\n'+names[text]+';')
            print('>>>',txt)
        bot.edit_message_text(chat_id=m.chat.id, message_id=edit, text=txt, reply_markup=key)


@bot.message_handler(commands=["start"])
def starts(m):
    bot.send_message(m.chat.id, f"Assalomu alaykum {m.from_user.first_name}")
    is_new_users(user=m)
    bot.send_message(m.chat.id,helpMessage())
    example(m)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, helpMessage())

@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, 'Muallif: Otaboboyev Akmal')

@bot.message_handler(commands=['soxa'])
def soxalar(message):
    example(message)

@bot.message_handler(commands=['get_soxa'])
def gs(m):
    k = user_soxa(m.chat.id)
    for x in k:
        bot.send_message(m.chat.id,x)
@bot.message_handler(commands=['adminga'])
def adminga(m):
    t = m.text
    if t.find(' ')!=-1:
        bot.send_message(578017143, f"[{m.chat.first_name}](tg://user?id={m.chat.id})\n>>>{t[t.find(' ')+1:]}", parse_mode='MARKDOWN')
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
            example(m=call.message, edit=call.message.message_id, text=call.data)

        elif call.data[:8]=='hashtag_':
            begins(call.message, edited=True,k=int(call.data[8:]))
        elif call.data=='ok':
            try:
                i=1
                db = connects()
                i=2
                mydb = db.cursor()
                i=3
                mess = call.message.text[call.message.text.rfind(':')+2:].replace('\n','')
                i=4
                #print(mess)
                i=5
                mydb.execute(f"UPDATE users SET soxa='{mess}' WHERE user_id='{call.message.chat.id}';")
                i=6
                db.commit()
                i=7
                db.close()
                i=8
                bot.send_message(call.message.chat.id, mess)
                i=9
                bot.delete_message(call.message.chat.id,call.message.message_id)
            except:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='Xatolik')
            #print('>>>i =',i)
        elif call.data=='n':
            example(m=call.message, pg='n', edit=call.message.message_id)
        elif call.data=='p':
            example(m=call.message, pg='p', edit=call.message.message_id)
        elif call.data=="Ok_savol":
            db = connects()
            mydb = db.cursor()
            u=users()
            key = types.InlineKeyboardMarkup()
            but1 = IKB(t="Bekor qilish", c="cancel")
            key.add(but1)
            text = call.message.text#[call.message.text.rfind('\n')+1:]
            sanoq=soni=0
            ht = hashtags(text)
            if ht!=0:
                ht = ht.replace("#","")
                ht = ht.split(";\n")
            for x in u:
                if int(x)!=call.message.chat.id:
                    mydb.execute(f"SELECT soxa FROM users WHERE user_id='{x}';")
                    a = mydb.fetchone()
                    print('>>>a>>',a)
                    #print('>>>ht>>',ht)
                    bor=False
                    if ht!=0 and a[0]!=None:
                        for y in ht:
                            if y in a[0].split(';'):
                                bor=True

                    elif ht==0:
                        sanoq=-1
                        break
                    if bor:
                        try:
                            bot.send_message(int(x),f"\"{call.message.chat.first_name}\" dan\n{call.message.text}",reply_markup=key)
                            #print('>>> ok_savol')
                            sanoq=1
                            soni+=1
                        except:
                            #bot.send_message(call.message.chat.id,f"{x} id egasi mavjud emas")
                            mydb.execute(f"UPDATE users SET onbot=0 WHERE user_id={x};")
                            db.commit()
                    else:
                        pass
            ma = ['Siz yo\'nalish tanlamagansiz!!','Siz tanlagan yo\'nalishda foydalanuvchi mavjud emas',f"Savol barcha shu yo\'nalishdagi( {soni}ta ) bot foydalanuvchilariga yuborildi"]
            bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text=ma[sanoq+1])

            db.close()
            if sanoq+1==2:
                savol_javob(mode="savol",user_id=call.message.chat.id,text=text)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)

        elif call.data=="Ok_javob":
            db = connects()
            mydb = db.cursor()
            key = types.InlineKeyboardMarkup()
            key.add(IKB(t=u"\U0001F44D +1",c="Up"), IKB(t="0",c="Neytral"), IKB(t=u"\U0001F44E -1",c="Down"))

            txt1 = call.message.reply_to_message.text
            txt = shifr(mode='shifr', t=txt1[txt1.rfind('\n')+1:])
            text = call.message.text[call.message.text.rfind('\n')+1:]
            ok=False
            k=0
            if ('#savol' in txt1):
                mydb.execute("SELECT id,savol,user_id FROM savol;")
                k=1
            elif ('#javob' in txt1):
                mydb.execute("SELECT * FROM javob;")

            z = mydb.fetchall()
            for x in z:
                #print(x, txt)
                #print(shifr(mode='shifr',t=txt))
                if x[1] in txt and x[2]!=str(call.message.chat.id):
                    try:
                        bot.send_message(int(x[2]),f"\"{call.message.chat.first_name}\" dan\n>>>savol:\n{txt1[txt1.rfind(';')+2:]}\n>>>{call.message.text}",reply_markup=key)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=call.message.text)
                        #print('ok_javob')
                        ok=True
                    except:
                        #bot.send_message(call.message.chat.id,"savol egasi botda foydalanishni to\'xtatgan")
                        mydb.execute(f"UPDATE users SET onbot=0 WHERE user_id={x[2]};")
                        db.commit()
            if k==1:
                a=[x[0],None]
            else:
                a=[None,x[0]]
            savol_javob(mode="javob",user_id=call.message.chat.id,savol_id=a[0],javob_id=a[1],text=text)
            if ok:
                bot.answer_callback_query(callback_query_id=call.id,show_alert=False, text="Javob savol beruvchiga yuborildi")
            else:
                bot.send_message(call.message.chat.id, 'Bot kodida xatolik')

        elif call.data=="cancel":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Bekor qilindi')

        elif call.data in ["Up", "Neytral", "Down"] :
            db = connects()
            mydb = db.cursor()
            if call.data=="Up":
                k=1
            elif call.data=="Neytral":
                k=0
            elif call.data=="Down":
                k=-1
            txt = call.message.text
            #print('>>>',txt)
            txt = shifr(mode='shifr', t=txt[txt.rfind(':\n')+3:])
            #print('>>>',txt)
            user_id=0
            mydb.execute(f"SELECT * FROM javob WHERE javob='{txt}';")
            y = mydb.fetchone()
            print('<<>>',y)
            user_id = y[2]

            mydb.execute(f"SELECT * FROM users WHERE user_id='{user_id}';")
            reyting=0
            x = mydb.fetchone()
            reyting = x[2]+k

            mydb.execute(f"UPDATE users SET reyting={reyting} WHERE user_id='{user_id}';")
            db.commit()
            db.close()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=call.message.text)


if __name__=='__main__':
    bot.polling(none_stop=True)
