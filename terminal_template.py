
import curses
import logging.config

VERSION = 1.0

MOTD01 =  "-----------------------------------------------------------\n"
MOTD01 += "   ____ _   _ ____  ____  _____ ____   ____ __  __ ____ \n"
MOTD01 += "  / ___| | | |  _ \/ ___|| ____/ ___| / ___|  \/  |  _ \ \n"
MOTD01 += " | |   | | | | |_) \___ \|  _| \___ \| |   | |\/| | | | |\n"
MOTD01 += " | |___| |_| |  _ < ___) | |___ ___) | |___| |  | | |_| |\n"
MOTD01 += "  \____|\___/|_| \_\____/|_____|____/ \____|_|  |_|____/ \n"
MOTD01 += " Command Line Application Template Version + " + str(VERSION) + "\n"
MOTD01 += "-----------------------------------------------------------\n"
                                                         
MOTD02 = "Commands: \n"
MOTD02 += "<H>ELP, <S>TATUS, <T>IMER, <E>CHO, \n"
MOTD02 += "<R>ECONNECT, <D>ISCONNECT, <Q>UIT/EXIT\n"

                                 
def disp(stdscr, current_line, text, newLine = False):
    curses.echo()
    # if current_line moves stuff off screen, move the screen first
    # by that many text lines before display
    actual_current_line = current_line
    max_y, max_x = stdscr.getmaxyx()    
    if current_line >= max_y - 1:
        actual_current_line = min(max_y-1, current_line)
        stdscr.move(1, 0)
        stdscr.refresh()
    if newLine:
        stdscr.addstr(actual_current_line, 0, text + "\n")
    else:
        stdscr.addstr(actual_current_line, 0, text)        
    # display the text    
    stdscr.refresh()    

def increment(stdscr, in_line):
    max_y, max_x = stdscr.getmaxyx()
    return min(max_y-1, in_line + 1)
    
def my_raw_input(stdscr, r, prompt_string):
    input = stdscr.getstr(r, len(prompt_string), 20)
    return input  #       ^^^^  reading input at next line  

if __name__ == "__main__":
    # Configure the logger
    # loggerConfigFileName: The name and path of your configuration file
    loggerConfigFileName = "./logconfig.txt"
    logging.config.fileConfig(loggerConfigFileName)

    # Create the logger
    # Admin_Client: The name of a logger defined in the config file
    myLogger = logging.getLogger('APP' + str(VERSION))

    #myLogger.debug(msg)
    myLogger.info("Initialized APP" + str(VERSION))
    #myLogger.warn(msg)
    #myLogger.error(msg)
    #myLogger.critical(msg)

    stdscr = curses.initscr()
    stdscr.scrollok(1)
    stdscr.idlok(1)
    stdscr.idcok(1)    

    stdscr.keypad(True)
    stdscr.clear()
    disp(stdscr, 0, MOTD01)
    disp(stdscr,len(MOTD01.split("\n"))+1, MOTD02)
    MOTD_line_count = len(MOTD01.split("\n")) + len(MOTD02.split("\n"))
    
    prompt = "APP" + str(VERSION) + " <"+ "IN[off] OUT[off]" + "> "
    
    keep_going = True
    return_prompt = True
    cycling_history = False
    max_y, max_x = stdscr.getmaxyx()
    current_line = MOTD_line_count + 1    
    while keep_going:
        curses.echo()
        myLogger.debug("current_line after prompt display: " + str(current_line))
        myLogger.debug("screen height before prompt display: " + str(max_y))
        if return_prompt:
            disp(stdscr, current_line, prompt)
        choice = my_raw_input(stdscr, current_line, prompt).lower().strip()
        current_line = increment(stdscr, current_line)        
        if choice == "help" or choice == "h":
            pass
        elif choice == "timer" or choice == "t":
            pass
        elif choice == "reconnect" or choice == "r":
            pass
        elif choice == "disconnect" or choice == "d":
            pass
        elif choice == "status" or choice == "s":
            disp(stdscr, current_line, "status called", newLine=True)
            myLogger.debug("current_line after status called: " + str(current_line))
            myLogger.debug("screen height after status called: " + str(max_y))
            current_line = increment(stdscr, current_line)
            return_prompt = True
        elif choice == "":
            return_prompt = True            
            pass        
        elif choice == "quit" or choice == "exit" or choice == "q":
            keep_going = False
        else:
            disp(stdscr, current_line, "Invalid Input. Type <help> for commands.", newLine=True)
            current_line = increment(stdscr, current_line)
            return_prompt = True
    myLogger.info("Shutting Down APP" + str(VERSION))            
    curses.endwin()
    logging.shutdown()
