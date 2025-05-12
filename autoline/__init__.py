import time
import pygetwindow as gw
import pyautogui
import pyperclip
def showWindow(title):
    '''
    show the window corespond with the title
    title:line chat group name string
    return window object
    Note:the chat group window must be separated from the LINE main window
    '''
    windows = gw.getWindowsWithTitle(title)
    for window in windows:
        if window.title==title:
            window.activate()
            window.maximize()
            return window
    print('找不到視窗')
    return None
def hideWindow(title="LINE"):
    '''
    hide the window corespond with the title
    title:line chat group name string
    return window object
    Note:the chat group window must be separated from the LINE main window
    '''
    windows = gw.getWindowsWithTitle(title)
    for window in windows:
        if window.title==title:
            window.minimize()
            return window
    return None

def send(title,msg):
    '''
    show the window correspond with the title and paste msg on messagebox to send the message
    title:line chat group name string
    msg:message string
    
    return window object
    Note:the chat group window must be separated from the LINE main window
    '''
    window=showWindow(title)
    if window:
        x,y=0.5*(window.left+window.right),window.top+30
        time.sleep(0.5)
        for i in range(3):time.sleep(0.5);pyautogui.press('end')
        pyautogui.click(x,y)
        pyautogui.click(x,window.bottom-50)
        pyperclip.copy(msg)
        time.sleep(1)
        pyautogui.hotkey('ctrl','a')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        return window
    return None

        
# send('家齊linebot','ok')