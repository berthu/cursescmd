import curses
import time
import logging, logging.config
import subprocess

VERSION = 2.5
PROMPT = "catsim" + str(VERSION) + "> "
chars = '1234567890qwertyuoipasdfghjklzxcvbnm'
chars = list(chars)

def disp(screen, r, c, text, newLine = False):
    curses.echo()
    screen.addstr(r, c , text)
    screen.refresh()

# Input: screen, width of box, height of box, and text
# Output: a list of lines formatted to the box by width
def format_line_to_box(screen, W, line):
    result = []
    finger = 0
    remaining_letters = len(line)
    while remaining_letters > 0:
        if remaining_letters >= W:
            result += [line[finger:finger+W]]
            finger += W
            remaining_letters = len(line[finger:finger+W])
        elif remaining_letters < W:
            result += [line[finger:finger+remaining_letters]]
            remaining_letters = 0
    return result
    
def disp_msg_box(screen, current_buffer, c, width, height,
                 text, newLine = False):
    # reformat the current_buffer first
    new_buffer_text = ""
    if len(current_buffer) == 0:
        new_buffer_text = text
    else:
        new_buffer_text = '\n'.join(current_buffer) + '\n' + text
    new_buffer_lines = []
    fitted_lines = []
    # split the text into lines
    lines = new_buffer_text.split('\n')
    # fit each line
    for line in lines:
        if len(line) > width:
            fitted_sublines = format_line_to_box(screen, width, line)
            fitted_lines += fitted_sublines
        else:
            fitted_lines += [line]            
    for line in fitted_lines:
        new_buffer_lines += [line]
    current_line = 1
    for line in new_buffer_lines[-1-height+1:]: #display the last height lines
        padded_line = line + ' '*(width-len(line))
        disp(screen, current_line, c, padded_line)
        current_line += 1
    return new_buffer_lines

    
def clear_prompt(screen):
    max_y, max_x = screen.getmaxyx()
    disp(screen, max_y-2, 1, PROMPT)
    screen.clrtoeol()
    screen.refresh()

def print_char_stack(screen, char_stack):
    max_y, max_x = screen.getmaxyx()    
    disp(screen, max_y-2, 1, PROMPT + char_stack)
    cur_y, cur_x = screen.getyx()        
    screen.refresh()
    

    
if __name__ == "__main__":
    # Configure the logger
    # loggerConfigFileName: The name and path of your configuration file
    loggerConfigFileName = "./logconfig.txt"
    logging.config.fileConfig(loggerConfigFileName)

    # Create the logger
    # Admin_Client: The name of a logger defined in the config file
    myLogger = logging.getLogger('APP' + str(VERSION))
    myLogger.info("Initialized APP" + str(VERSION))
    
    # curses setup
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad( 1 )
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
    highlightText = curses.color_pair( 1 )
    normalText = curses.A_NORMAL    
    screen.border( 0)
    curses.curs_set( 1 )
    curses.halfdelay(5)
    screen.leaveok(0)
    # prompt_box
    max_y, max_x = screen.getmaxyx()

    status_box = curses.newwin(3, max_x, max_y-6, 0)
    status_box.box()
    prompt_box = curses.newwin(3, max_x, max_y-3, 0)
    prompt_box.box()
    msgbox = curses.newwin( max_y - 6, int(max_x/2), 0, 0 )
    msgbox.box()
    logbox = curses.newwin( max_y - 6, max_x - int(max_x/2), 0, int(max_x/2) )
    logbox.box()

    screen.refresh()
    max_y, max_x = screen.getmaxyx()
    char_stack = ""
    run_command = False
    last_char = -10000
    continue_app = True
    msg_buffer = []
    log_buffer = []
    while continue_app:
        char = screen.getch()
        last_char = char
        resize = curses.is_term_resized(max_y, max_x)
        if resize:        
            max_y, max_x = screen.getmaxyx()            
            status_box = curses.newwin(3, max_x, max_y-6, 0)
            status_box.box()
            prompt_box = curses.newwin(3, max_x, max_y-3, 0)
            prompt_box.box()
            msgbox = curses.newwin( max_y - 6, int(max_x/2), 0, 0 )
            msgbox.box()
            logbox = curses.newwin( max_y - 6, max_x - int(max_x/2), 0, int(max_x/2))
            logbox.box()    
            disp(screen, max_y-2, 1, PROMPT)            
        max_y, max_x = screen.getmaxyx()
        screen.refresh()
        msgbox.refresh()
        logbox.refresh()
        prompt_box.refresh()
        status_box.refresh()
        curses.echo()
        cur_y, cur_x = screen.getyx()        
        screen.refresh()
        if char != curses.ERR and char not in range(256):
            disp(screen, 1, 1, "Processing key: " + str(char))            
            if char == 263:
                char_stack = char_stack[0:-1]
                clear_prompt(screen)
                print_char_stack(screen, char_stack)
        elif char != curses.ERR and char == curses.KEY_RESIZE:
            max_y, max_x = screen.getmaxyx()            
            status_box = curses.newwin(3, max_x, max_y-6, 0)
            status_box.box()            
            prompt_box = curses.newwin(3, max_x, max_y-3, 0)
            prompt_box.box()            
            box = curses.newwin( max_y - 6, max_x, 0, 0 )
            box.box()
            disp(screen, max_y-2, 1, PROMPT + char_stack)
        elif char != curses.ERR and char == 10:
            command = char_stack.lower()
            if command == "":
                pass            
            myLogger.debug("Processing command: " + command)
            msg_buffer = disp_msg_box(screen, msg_buffer,
                                      1, int(max_x/2) - 2, max_y-6-2,
                                      "Processing command: " + command)
            if command == "quit" or command == "q":
                continue_app = False
            char_stack = ""
            clear_prompt(screen)
        elif char != curses.ERR and char in range(256):
            char_stack += chr(char)
            print_char_stack(screen, char_stack)
        elif char != curses.ERR:
            pass
        else:
            disp(screen, max_y-6+1, 1, str(time.time()))
            f = subprocess.Popen(['tail','-n',str(max_y-6-2),'./terminal.log'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            new_log_lines = []
            for i in range(0,max_y-6-2):
                line = f.stdout.readline()
                line = line[11:19] + line[43:]
                new_log_lines += [line]
                
            log_buffer = disp_msg_box(screen, log_buffer,
                                      int(max_x/2)+2, max_x - int(max_x/2) - 3, max_y-6-2,
                                      ''.join(new_log_lines))
            disp(screen, max_y-2, 1, PROMPT + char_stack)

        
    curses.endwin()
    exit()
