import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image, ImageDraw
import threading
import sys
import autoline
import os
from datetime import datetime

def on_show(icon, item): show_window()
def on_exit(icon, item):
    icon.stop()
    root.destroy()
    sys.exit()

def show_window():
    root.deiconify()
    root.lift()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))

def log(msg):
    text_box.config(state='normal')
    text_box.insert(tk.END, msg)
    text_box.see(tk.END)
    text_box.config(state='disabled')

isDone = False
last_checked_day = [None]

def bring_to_front():
    global isDone
    now = datetime.now()
    if last_checked_day[0] != now.day:
        isDone = False
        last_checked_day[0] = now.day

    selected_hour = int(hour_var.get())
    selected_min = int(min_var.get())

    group_title = title_var.get().strip()

    if now.hour == selected_hour and now.minute == selected_min and not isDone:
        log(f"[{now.strftime('%H:%M:%S')}] 推播時間到達！\n")
        show_window()
        isDone = True
        for fn in os.listdir('msg'):
            f = open(f'msg/{fn}',encoding='utf-8')
            msg = f.read()
            if  autoline.send(group_title, msg+'\n') == None:isDone = False
        if isDone:log('done')
    if now.hour == 23 and now.minute > 50 : isDone = False

    if autoline.hideWindow(group_title) is None:
        log(f"未開啟視窗 [{group_title}] \n")

    try:
        interval = int(interval_var.get())
    except:
        interval = 5
    root.after(interval * 1000, bring_to_front)

def on_closing(): root.withdraw()

def setup_tray():
    icon_image = Image.open("2.ico")
    icon = pystray.Icon("AutoLine", icon_image, "AutoLine", menu=pystray.Menu(
        pystray.MenuItem("顯示", on_show),
        pystray.MenuItem("退出", on_exit)
    ))
    icon.run()

# --- 主視窗 ---
root = tk.Tk()
root.iconbitmap("2.ico")
root.geometry("360x360")
root.title("每日推播提醒")

main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True, padx=10, pady=10)

# 群組視窗標題
tk.Label(main_frame, text="群組視窗標題：", anchor='w').pack(anchor='w')
title_var = tk.StringVar(value="LINE")
tk.Entry(main_frame, textvariable=title_var).pack(fill='x', pady=(0, 10))

# 推播時間
tk.Label(main_frame, text="推播時間：", anchor='w').pack(anchor='w')
time_frame = tk.Frame(main_frame)
time_frame.pack(anchor='w', pady=(0, 10))
hour_var = tk.StringVar(value="08")
min_var = tk.StringVar(value="00")
spin_hour = ttk.Spinbox(time_frame, from_=0, to=23, width=5, textvariable=hour_var, format="%02.0f", justify='left')
spin_min = ttk.Spinbox(time_frame, from_=0, to=59, width=5, textvariable=min_var, format="%02.0f", justify='left')
spin_hour.pack(side='left')
tk.Label(time_frame, text=":").pack(side='left', padx=2)
spin_min.pack(side='left')

# 核取方塊
daily_var = tk.BooleanVar(value=True)
holiday_var = tk.BooleanVar(value=False)
chk_daily = tk.Checkbutton(main_frame, text="每日", variable=daily_var, anchor='w', justify='left')
chk_holiday = tk.Checkbutton(main_frame, text="包含假日", variable=holiday_var, anchor='w', justify='left')
chk_daily.pack(anchor='w')
chk_holiday.pack(anchor='w')

# 訊息欄（唯讀 + 捲軸）
tk.Label(main_frame, text="訊息欄：", anchor='w').pack(anchor='w', pady=(10, 0))
log_frame = tk.Frame(main_frame)
log_frame.pack(fill='both', expand=True)

text_scrollbar = tk.Scrollbar(log_frame)
text_scrollbar.pack(side='right', fill='y')

text_box = tk.Text(log_frame, height=6, width=40, wrap='word', yscrollcommand=text_scrollbar.set, state='disabled')
text_box.pack(side='left', fill='both', expand=True)
text_scrollbar.config(command=text_box.yview)

# 下拉選單：檢查間隔
tk.Label(main_frame, text="檢查間隔（秒）：", anchor='w').pack(anchor='w', pady=(10, 0))
interval_var = tk.StringVar(value="5")
interval_combo = ttk.Combobox(main_frame, textvariable=interval_var, state="readonly", values=["5", "10", "30", "60"])
interval_combo.pack(anchor='w')

# 視窗關閉攔截
root.protocol("WM_DELETE_WINDOW", on_closing)

# 啟動系統匣
threading.Thread(target=setup_tray, daemon=True).start()

# 定期跳出
bring_to_front()
root.mainloop()
