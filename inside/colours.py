def colours (curses):
    if curses.can_change_color ():
        curses.start_color ()
        curses.use_default_colors ()
        curses.init_color (10,96, 978, 121) # lightgreen
        curses.init_pair (1,10,-1) # main color
        curses.init_color (11,211, 720, 930) # blue
        curses.init_pair (2,11,-1) # warning message
    else:
        raise Exception ("terminalmu tidak bisa menggunakan warna")