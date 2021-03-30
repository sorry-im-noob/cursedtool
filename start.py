
import curses
import traceback
import string
import textwrap
def main (scr):
    # curses variable options
    mouse = True # default true
    cur = False # default false

    # curses options
    curses.curs_set (cur)
    curses.mousemask (mouse)
    curses.noecho ()
    scr.keypad (True)

    # curses colours
    curses.start_color ()
    curses.use_default_colors ()
    if curses.can_change_color ():
        curses.init_color (10,96, 978, 121) # lightgreen
        curses.init_pair (1,10,-1) # main color
        curses.init_color (11,211, 720, 930) # blue
        curses.init_pair (2,11,-1) # warning message
    else:
        raise Exception ("terminalmu tidak bisa menggunakan warna")


    # curses useful variables
    pos_y = 11
    pos_x = 14
    real_pos_y = 0
    real_pos_x = 0
    scroll_line = 0
    refresh = True
    scr_y,scr_x = scr.getmaxyx ()
    key = 0
    use_d = ()
    pas_d = ()
    error_py = scr_y//2
    error_px = scr_x-33
    k410 = 0
    

    # error messages
    sml = "layar anda terlalu kecil untuk ditampilkan,  silahkan perbesar  dulu layarnya dan buka  kembali scriptnya"
    error_m = ""
    error_w = scr.subwin (scr_y//3+5,scr_x//2,3,3)


    # making windows for username and password section
    use_w = scr.subwin (3,25,10,13) # default position
    pas_w = scr.subwin (3,25,14,13) # default position

    # making subwindows for header and foot section
    head_w = scr.subwin (9,scr_x,0,0)
    head_y,head_x = head_w.getmaxyx ()
    text = (
        "sebelum masuk dan menggunakan",
        "script ini, anda harus memasukan",
        "username dan password dulu.",
        "username dan password yang dimaksud",
        "adalah username dan password dari",
        "script ini, bukan dari facebook",
        "atau akun pribadi milik anda"
    )
    text2 = "made by [@sorry.i.m.noob] 2021"

    # start program
    ex = False
    while not ex:
        try:

            # check if the size smaller than 33
            # check if the size has been changed
            if key == 410:
                scr_y,scr_x = scr.getmaxyx ()
                if scr_x < 40 or scr_y < 19:
                    exit (sml)
                else:
                    refresh = True
                    head_w.resize (9,scr_x)
                    head_y,head_x = head_w.getmaxyx ()
                    error_py = scr_y//2
                    error_px = scr_x-33
            
            # refresh display with needed condition
            if refresh:
                scr.erase ()
                use_w.bkgd (" ",curses.color_pair (1)+curses.A_BLINK)
                pas_w.bkgd (" ",curses.color_pair (1)+curses.A_BLINK)
                head_w.bkgd (" ",curses.color_pair (1)+curses.A_BLINK)
                use_w.box ()
                pas_w.box ()
                head_w.box ()
                scr.addstr (11,3,"username:",curses.color_pair (1)+curses.A_STANDOUT)
                scr.addstr (15,3,"password:",curses.color_pair(1)+curses.A_STANDOUT)
                for x in range  (len (text)):
                    head_w.addstr (1+x,head_x//2-len (text [x])//2,text [x])
                if len (error_m) > 0:
                    error_message (scr,"[pesan dari script]",error_m,error_py,error_px)
                    refresh = True
                else:                    
                    refresh = False

            # the username and password output
            scr.addstr (11,14,"".join (use_d),curses.color_pair (2)+curses.A_BLINK)
            scr.addstr (15,14,"*"*len (pas_d),curses.color_pair (2)+curses.A_BLINK)
            scr.hline (scr_y-1,0," ",scr_x,curses.color_pair (1)+curses.A_STANDOUT)
            scr.addstr (scr_y-1,scr_x//2-len (text2)//2,text2,curses.color_pair (1)+curses.A_STANDOUT)

            # the position of real_pos_x
            if pos_y==11:real_pos_x = pos_x+len (use_d)
            elif pos_y==15:real_pos_x = pos_x+len (pas_d)
                
            #scr.addstr (14,0,str(scr.getmaxyx ()))
            key = scr.getch (pos_y,real_pos_x)
            error_m = ""

            if not mouse:
                if key==curses.KEY_UP:
                    pos_y = 11
                elif key==curses.KEY_DOWN:
                    pos_y = 15
                elif chr (key) in string.ascii_letters + string.digits:
                    if pos_y == 11:use_d += (chr (key),)
                    elif pos_y == 15:pas_d += (chr (key),)
                elif key == 127:
                    if pos_y == 11:
                        if len (use_d)==0:
                            error_m = "sebenarnya yang mau dihapus apa?"
                            refresh = True
                        use_d = use_d [0:-1]
                    elif pos_y==15:
                        if len (pas_d)==0:pos_y = 11
                        pas_d = pas_d [0:-1]
                    refresh = True
                elif key in [32,46]:
                    error_m = "dilarang menggunakan spasi atau tanda titik"
                    refresh = True
                elif key == 10:
                    if len (use_d) == 0:
                        error_m = "username belum disi";
                        refresh = True
                    elif len  (pas_d)==0 and pos_y==15:
                        error_m = "password belum disi"
                        refresh = True
                    elif len (pas_d)==0:
                        pos_y = 15
                    else:
                        if "".join (use_d)=="imnoob" and "".join (pas_d)=="heartnet":
                            exit ("you successed")
                        else:
                            error_m = "username atau passwordnya salah"
                            refresh = True
                        
                elif key in (127,10):
                    refresh = True
                elif key in (409,410):
                    pass
                elif (chr (key) not in string.ascii_letters+string.digits):
                    error_m = "tidak boleh memasukan selain huruf dan angka"
                    refresh = True
            _,x_m,y_m,_,_ = curses.getmouse ()

            # checking for getmouse function
            use_cek = y_m in range (10,13) and x_m in range (2,39) 
            pas_cek = y_m in range (13,16) and x_m in range (2,39)
            if use_cek:
                mouse = False
                pos_y = 11
                pos_x = 14
                cur = True
            elif pas_cek:
                mouse = False
                pos_y = 15
                pos_x = 14
                cur = True
            """
            elif not (use_cek and pas_cek):
                mouse = True
                cur =  False
            """
            curses.curs_set(cur)
            # scr.addstr (14,0,str(key))
        except curses.error as err:
            if (str (err)=="getmouse() returned ERR"):
                pass
            else:
                exit(traceback.format_exc ())
        except (KeyboardInterrupt,EOFError):
            exit ("exit program")
def error_message (win,top,text,begin_y,begin_x):
    new = win.derwin (6,30,begin_y,begin_x)
    new.bkgd (" ",curses.color_pair (2)+curses.A_BLINK)
    new.box ()
    #new.hline (2,1,"-",2)
    new.addstr (0,3,top)
    text = textwrap.wrap (text,28)
    for i,x in enumerate (text):
        new.addstr (2+i,1,x)
        


curses.wrapper (main)