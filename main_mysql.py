import requests
while True:
    try:
        import telebot
        from telebot import types
        from mybottoken import mytoken
        import mysql.connector
        import myhost
        import os
        import time
        from math import ceil
        mh = myhost.MyHostForumuzOffline
        bot = telebot.TeleBot(mytoken)
        
        def soxa():
            s = [
                'Matematika','Fizika','Kimyo','Java','Python',
                'C++','C#','Linux','Windows','MacOS','Algebra',
                'Geometriya','Chizmachilik','Biologiya','Telegram Bot',
                'Android'
                ]
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
                    auth_plugin=mh[3],
                    database=mh[4])
                mydb = db.cursor()
                try:
                    mydb.execute(f"CREATE DATABASE IF NOT EXISTS {mh[4]}")
                    db.commit()
                except:
                    pass
                mydb.execute("CREATE TABLE IF NOT EXISTS users(user_id VARCHAR(15) NOT NULL,onbot tinyint(1) NOT NULL,reyting INT NOT NULL, soxa text)")  
                mydb.execute("CREATE TABLE IF NOT EXISTS savol(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,savol text,hashtags text, user_id VARCHAR(15) NOT NULL)") 
                mydb.execute("CREATE TABLE IF NOT EXISTS javob(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,javob text, user_id VARCHAR(15) NOT NULL, savol_id INT, javob_id INT, FOREIGN KEY (savol_id) REFERENCES savol(id), FOREIGN KEY (javob_id) REFERENCES javob(id) )")
                db.commit()
                return db
            except:
                pass
            
        def savol_javob(user_id=None,text=None,savol_id=None,javob_id=None,reyting=None, mode=None):
            db = connects()
            mydb = db.cursor()
            if mode=="savol":
                code=f"INSERT INTO savol(savol,user_id) VALUES ('{text}','{user_id}')"
            if mode=="javob":
                if savol_id!=None:
                    code=f"INSERT INTO javob(javob,savol_id,user_id) VALUES ('{text}','{savol_id}','{user_id}')"
                elif javob_id!=None:
                    code=f"INSERT INTO javob(javob,javob_id,user_id) VALUES ('{text}','{javob_id}','{user_id}')"
            mydb.execute(code)
            db.commit()
            db.close()
        def shifr(mode=None, t=None):
            if mode=='shifr':
                return t.encode('utf-8').hex()
            elif mode=='deshifr': 
                return bytes.fromhex(t).decode('utf-8')
        def is_new_users(user_id=None, onbot=1, reyting=0):
            try:
                db = connects()
                mydb = db.cursor()
                mydb.execute("SELECT * FROM users")
                e1,e2=0,0
                for x in mydb:
                    if x[0]==str(user_id):
                        e1=1
                        if x[1]==0:
                            e2=1
                        break
                if e1==0:
                    text=f"INSERT INTO users(user_id,onbot,reyting) VALUES ('{user_id}',{onbot},{reyting})"
                    mydb.execute(text)
                    db.commit()
                if e2==1:
                    text=f"UPDATE users SET onbot={onbot} WHERE user_id='{user_id}'"
                    mydb.execute(text)
                    db.commit()
                db.close()
            except:
                pass
                
        def users():
            try:
                db = connects()
                mydb = db.cursor()
                mydb.execute("SELECT user_id FROM users WHERE onbot=1")
                k=[]
                for x in mydb:
                    k.append(x[0])
                return k
            except:
                pass 
        def helpMessage():
            text = f"Botdan foydalanish:\nOxirgi yangilanish: {fut()}\n* Savolingizni shunday yozavering\n* Savolingizni xato yozdingizmi? Unda savolingizni shunchaki to'g'irlang\n* Javob berish uchun shunchaki \"reply\" qilib yozing\n* Hammasini qilib bo'lgach \"'OK\" tugmasini bosing\n\"Ok\" tugmasini bosgandan keyin o'zgartira olmaysiz\n* Xabaringiz o'chirish uchun \"Bekor qilish\" tugmasini bosing\n* Savolingiz yoki javobingiz yuborilganini tagidagi tugmalar yo'q bo'lib qolganda bilasiz"
            return text
        
        def user_soxa(user_id):
            try:
                db = connects()
                mydb = db.cursor(buffered=True)
                s=[]
                mydb.execute(f"SELECT soxa FROM users WHERE user_id='{user_id}'")
                for x in mydb:
                    if x[0]!=None:
                        s=x[0].split(';')
                        s=[s[x] for x in range(len(s)) if s[x]!='']
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
        
        def qolip(text=None, hashtag=None):
            l = len(text)
            head = text[:text.find(':')]
            f = text.rfind(';')
            if f==-1:
                foot = text[text.find(':')+1:]
            else:
                foot = text[f+1:]
            hash = text[len(head):l-len(foot)]
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
            is_new_users(user_id=m.chat.id)
            try:
                text = m.reply_to_message.text
            except:
                text = m.text
            mode = "savol"
            mid = m.message_id
            s = user_soxa(m.chat.id)
            if (("#savol" in text) or ("#javob" in text)) and (m.reply_to_message.entities[0].type=="hashtag"):
                mode = "javob"
                mid = m.reply_to_message.message_id
                s=['None']
                try:
                    bot.edit_message_text(chat_id=m.chat.id, message_id=mid, text=m.reply_to_message.text)
                except:
                    pass
            else:
                 pass
            
            sv = types.InlineKeyboardMarkup()
            if s[0]!='None':
                for x in range(len(s)):
                    sv.add(IKB(t=f"#{s[x]}", c=f"hashtag_{x}"))
            sv.add(IKB(t="Ok",c=f"Ok_{mode}"), IKB(t="Bekor qilish",c="cancel"))
            base = f"#{mode}: \n{m.text}"
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
            base = '%.2d. Yo\'nalish tanlang:' % cpg
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
                    txt = qolip(text=a, hashtag='\n'+names[text]+';')
                bot.edit_message_text(chat_id=m.chat.id, message_id=edit, text=txt, reply_markup=key)
        
                
        @bot.message_handler(commands=["start"])
        def starts(m):
            bot.send_message(m.chat.id, f"Assalomu alaykum {m.from_user.first_name}")
            is_new_users(user_id=m.chat.id)
            bot.send_message(m.chat.id,helpMessage())
            example(m)
            
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
                    example(m=call.message, edit=call.message.message_id, text=call.data)
                
                elif call.data[:8]=='hashtag_':
                    begins(call.message, edited=True,k=int(call.data[8:]))
                elif call.data=='ok':
                    try:
                        db = connects()
                        mydb = db.cursor()
                        mess = call.message.text[call.message.text.rfind(':')+2:].replace('\n','')
                        print(mess)
                        mydb.execute(f"UPDATE users SET soxa='{mess}' WHERE user_id='{call.message.chat.id}'")
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
                    but1 = types.InlineKeyboardButton(text="Bekor qilish", callback_data="cancel")
                    key.add(but1)
                    text = shifr(mode='shifr',t=call.message.text[call.message.text.rfind('\n')+1:])
                    for x in u:
                        if int(x)!=call.message.chat.id:
                            try:
                                bot.send_message(int(x),f"\"{call.message.chat.first_name}\" dan\n{call.message.text}",reply_markup=key)
                                print('ok_savol')
                            except:
                                bot.send_message(call.message.chat.id,f"{x} id egasi mavjud emas")
                                mydb.execute(f"UPDATE users SET onbot=0 WHERE user_id={x}")
                                db.commit()
                    db.close()
                    savol_javob(mode="savol",user_id=call.message.chat.id,text=text)
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
                    text = shifr(mode='shifr',t=call.message.text[call.message.text.rfind('\n')+1:])
                    if ('#savol' in txt):
                        txt = shifr(mode='shifr', t=txt[txt.rfind('\n')+1:])
                        mydb.execute("SELECT id,savol,user_id FROM savol")
                        for x in mydb:
                            print(x, txt)
                           #print(shifr(mode='shifr',t=txt))
                            if x[1] in txt and x[2]!=str(call.message.chat.id):
                                try:
                                    bot.send_message(int(x[2]),f"\"{call.message.chat.first_name}\" dan\n{call.message.text}",reply_markup=key)
                                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=call.message.text)
                                    print('ok_javob')
                                except:
                                    bot.send_message(call.message.chat.id,"savol egasi botda foydalanishni to\'xtatgan")
                                    mydb.execute(f"UPDATE users SET onbot=0 WHERE user_id={x[2]}")
                                    db.commit()
                                break
                        savol_javob(mode="javob",user_id=call.message.chat.id,savol_id=x[0],text=text)
                        bot.answer_callback_query(callback_query_id=call.id,show_alert=False, text="Javob savol beruvchiga yuborildi")
                        
                    elif ('#javob' in txt):
                        txt = txt[txt.rfind('\n')+1:]
                        mydb.execute("SELECT * FROM javob")
                        for x in mydb:
                            if x[1] in txt and x[2]!=str(call.message.chat.id):
                                try:
                                    bot.send_message(int(x[2]),f"\"{call.message.chat.first_name}\" dan\n{call.message.text}",reply_markup=key)
                                    print('ok_javob')
                                except:
                                    bot.send_message(call.message.chat.id,"savol egasi botda foydalanishni to\'xtatgan")
                                    mydb.execute(f"UPDATE users SET onbot=0 WHERE user_id={x[2]}")
                                    db.commit()
                                break
                        savol_javob(mode="javob",user_id=call.message.chat.id,javob_id=x[0],text=text)
                        bot.answer_callback_query(callback_query_id=call.id,show_alert=False, text="Javobga xabar yuborildi")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=call.message.text)
                    
                    db.close()
                    
                    
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
                    txt = shifr(mode='shifr', t=txt[txt.rfind('\n'):])
                    user_id=0
                    mydb.execute(f"SELECT * FROM javob WHERE javob='{txt}'")
                    for y in mydb:
                        print(y)
                        user_id = y[2]
                        break
                    #print(user_id, type(user_id))
                    
                    mydb.execute(f"SELECT * FROM users WHERE user_id={user_id}")
                    reyting=0
                    for x in mydb:
                        print(x)
                        reyting = x[2]+k
                        break
                    #print(reyting)
                    
                    mydb.execute(f"UPDATE users SET reyting={reyting} WHERE user_id='{user_id}'")
                    db.commit()
                    db.close()
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=call.message.text)
        
        
        if __name__=='__main__':
            bot.polling(none_stop=True)
    except (requests.exceptions.ConnectionError, requests.packages.urllib3.exceptions.ProtocolError):
        pass