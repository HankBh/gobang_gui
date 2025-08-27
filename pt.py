# -*- coding: utf-8 -*-

"""
Positive Tool 5
一個好用的工具箱
by TW_bh
"""

import os
import subprocess
import logging
import sys
import shutil
import unicodedata
import inspect

from rich import traceback
from rich.logging import RichHandler

traceback.install()

############################
# version
pt_ver = "5-23"
pt_pre_ver = True
############################

log_file_path = os.path.join(".", ".log")

frame = inspect.currentframe()

FORMAT = "%(asctime)s | %(name)s | %(levelname)s | [%(filename)s:%(funcName)s::%(lineno)d] | %(message)s"
DATEFMT = "[%Y-%m-%d %H:%M:%S]"
# 建立 RichHandler（終端輸出）
console_handler = RichHandler(rich_tracebacks=True)
console_handler.setLevel(logging.WARNING)  # 終端只顯示 WARNING 以上

# 建立 FileHandler（輸出到檔案）
file_handler = logging.FileHandler(log_file_path, encoding="utf-8", mode="a")
file_handler.setLevel(logging.DEBUG)  # 檔案紀錄 DEBUG 全部訊息

# 設定 Formatter
formatter = logging.Formatter(fmt=FORMAT, datefmt=DATEFMT)
file_handler.setFormatter(formatter)

# 設定 logging 基本設定
logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT,
    datefmt=DATEFMT,
    handlers=[console_handler, file_handler],
)

# 使用 Logger
pt_logger = logging.getLogger("PT_log")


PT_change_log = """
5.0:
    **2025-05-30**
    !!!!!!!!!!!!!!!!!!!
    **BREAKING UPDATE**
    **破壞性更新**
    !!!!!!!!!!!!!!!!!!!
    1更改print_color & con接受的內容，從str變為list

5.1:
    **2025-05-30**
    1修復錯誤。

5.2:
    **2025-05-31**
    1修復錯誤。

5.3:
    **2025-06-02**
    !!!!!!!!!!!!!!!!!!!
    **BREAKIBG UPDATE**
    **破壞性更新**
    !!!!!!!!!!!!!!!!!!!
    1con & print_color顏色改回str。

5.4:
    **2025-06-05**
    1開始使用logging module。
    2將.get()改為[]。,因為已經if color in COLORS過了

5.5:
    **2025-06-08**
    1修復clear()的錯誤。,只存在windows系統

5.6:
    **2025-06-08**
    1將原本的welcome()正名為credit()，新增（新）welcome()。

5.7:
    **2025-06-10**
    1新增print_len，顯示或返回指定長度的文字。

5.8:
    **2025-06-11**
    1在clear新增Unicode 清除類型，原為command 。

5.9:
    **2025-06-13**
    1新增get_lines()。

5.10:
    **2025-06-14**
    1使用get_lines()重寫print_long()。

5.11:
    **2025-06-15**
    1優化。

5.12:
    **2025-06-15**
    **BREAKING UPDATE**
    **破壞性更新 — get_lines()將被刪除（搬移）**
    1get_lines()將搬移到ptbi.py，pt.py將不會有get_lines()。

5.13:
    **2025-06-17**
    1新增get_parts()。

5.14:
    **2025-06-22**
    1刪除logging
    2修復錯誤。,test的對齊 & 註解錯字

5.15:
    **2025-06-23**
    1新增logging。

5.16:
    **2025-06-25**
    1新增AutoResetColor。

5.17:
    1新增print_right()

5.18:
    1刪除print_error()
    2print_space() 新增 real_space 選項

5.19:
    1新增print_middle()
    2新增run_cli_cmd()，可以用args傳指令，(beta)，(但是windows不能使用雙引號也不能用powershell)

5.20:
    1優化。

Pre 5.21:
    1新增get_values()
    2刪除AutoResetColor

Pre 5.22:
    1刪除sleep()
    2刪除run_cli_cmd()
"""

CREDIT_TEXT_1 = r"""
     |
     |
     |
     |
     |---
     |   \
     |   /
     |---
"""

CREDIT_TEXT_2 = r"""
    \      /
     \    /
      \  /
        /
       /
      /
     /
"""

CREDIT_TEXT_5 = r"""
         |            |
         |            |
         |            |
         |            |
         |            |
         |            |
         |            |
         |------      |-------
         |      \     |       |
         |      |     |       |
         |      /     |       |
         |------      |       |
"""

WELCOME_TEXT_PT = r"""
        |------\        -------------
        |       \             |
        |        |            |
        |       /             |
        |------/              |
        |                     |
        |                     |
        |                     |
        |                     |
        |                     |
        |                     |
        |                     |

"""

# --- 顏色與樣式定義 (依類型及數字排序) ---
COLORS = {
    "reset": "\033[0m",  # 重置所有屬性
    # --- 文字樣式 (1-9, 21-29, 51-53) ---
    "bold": "\033[1m",  # 粗體 (或增亮)
    "dim": "\033[2m",  # 黯淡/變暗
    "italic": "\033[3m",  # 斜體 (終端支援度不一)
    "underline": "\033[4m",  # 底線
    "blink": "\033[5m",  # 閃爍 (慢)
    "rapid_blink": "\033[6m",  # 快速閃爍 (更少終端支援)
    "reverse": "\033[7m",  # 反白 (交換前景色和背景色)
    "concealed": "\033[8m",  # 隱藏 (前景顏色與背景相同)
    "crossed_out": "\033[9m",  # 刪除線 (或劃掉)
    "double_underline": "\033[21m",  # 雙底線 (終端支援度不一)
    "reset_bold_dim": "\033[22m",  # 重置粗體和黯淡
    "reset_italic": "\033[23m",  # 重置斜體
    "reset_underline": "\033[24m",  # 重置底線 (包括雙底線)
    "reset_blink": "\033[25m",  # 重置閃爍
    "reset_reverse": "\033[27m",  # 重置反白
    "reset_concealed": "\033[28m",  # 重置隱藏
    "reset_crossed_out": "\033[29m",  # 重置刪除線
    "frame": "\033[51m",  # 框架 (終端支援度低)
    "encircled": "\033[52m",  # 外框 (終端支援度低)
    "overlined": "\033[53m",  # 上劃線 (終端支援度不一)
    # --- 基本前景顏色 (30-37) ---
    "black": "\033[30m",  # 黑色
    "red": "\033[31m",  # 紅色
    "green": "\033[32m",  # 綠色
    "yellow": "\033[33m",  # 黃色
    "blue": "\033[34m",  # 藍色
    "purple": "\033[35m",  # 紫色 (洋紅)
    "magenta": "\033[35m",  # 洋紅 (同 purple)
    "cyan": "\033[36m",  # 青色
    "light_gray": "\033[37m",  # 淺灰色 (或白色)
    # --- 基本背景顏色 (40-47) ---
    "bg_black": "\033[40m",  # 背景黑色
    "bg_red": "\033[41m",  # 背景紅色
    "bg_green": "\033[42m",  # 背景綠色
    "bg_yellow": "\033[43m",  # 背景黃色
    "bg_blue": "\033[44m",  # 背景藍色
    "bg_purple": "\033[45m",  # 背景紫色 (洋紅)
    "bg_magenta": "\033[45m",  # 背景洋紅 (同 bg_purple)
    "bg_cyan": "\033[46m",  # 背景青色
    "bg_light_gray": "\033[47m",  # 背景淺灰色 (或白色)
    # --- 亮色/高強度前景顏色 (90-97) ---
    "dark_gray": "\033[90m",  # 深灰色 (亮黑)
    "light_red": "\033[91m",  # 淺紅色 (亮紅)
    "light_green": "\033[92m",  # 淺綠色 (亮綠)
    "light_yellow": "\033[93m",  # 淺黃色 (亮黃)
    "light_blue": "\033[94m",  # 淺藍色 (亮藍)
    "light_purple": "\033[95m",  # 淺紫色 (亮洋紅)
    "light_magenta": "\033[95m",  # 亮洋紅 (同 light_purple)
    "light_cyan": "\033[96m",  # 淺青色 (亮青)
    "white": "\033[97m",  # 白色 (亮白)
    # --- 亮色/高強度背景顏色 (100-107) ---
    "bg_dark_gray": "\033[100m",  # 背景深灰色 (亮黑)
    "bg_light_red": "\033[101m",  # 背景淺紅色 (亮紅)
    "bg_light_green": "\033[102m",  # 背景淺綠色 (亮綠)
    "bg_light_yellow": "\033[103m",  # 背景淺黃色 (亮黃)
    "bg_light_blue": "\033[104m",  # 背景淺藍色 (亮藍)
    "bg_light_purple": "\033[105m",  # 背景淺紫色 (亮洋紅)
    "bg_light_magenta": "\033[105m",  # 背景亮洋紅 (同 bg_light_purple)
    "bg_light_cyan": "\033[106m",  # 背景淺青色 (亮青)
    "bg_white": "\033[107m",  # 背景白色 (亮白)
    # --- "Bright" 顏色 (使用 ;1m 組合，效果常與 90-97 相同或相似，但某些終端可能不同) ---
    #     (依據基本色的數字 30-37 排序)
    "bright_black": "\033[30;1m",  # 亮黑色 (常同 dark_gray)
    "bright_red": "\033[31;1m",  # 亮紅色 (常同 light_red)
    "bright_green": "\033[32;1m",  # 亮綠色 (常同 light_green)
    "bright_yellow": "\033[33;1m",  # 亮黃色 (常同 light_yellow)
    "bright_blue": "\033[34;1m",  # 亮藍色 (常同 light_blue)
    "bright_purple": "\033[35;1m",  # 亮紫色
    "bright_magenta": "\033[35;1m",  # 亮洋紅色 （同bright_purple）(常同 light_magenta)
    "bright_cyan": "\033[36;1m",  # 亮青色 (常同 light_cyan)
    "bright_white": "\033[37;1m",  # 亮白色 (常同 white)
    # --- 256 色模式前景範例 ( \033[38;5;{n}m ) ---
    #     (依顏色編號 n 排序)
    "steel_blue": "\033[38;5;67m",  # 鋼藍色 (顏色編號 67)
    "sky_blue": "\033[38;5;117m",  # 天藍色 (顏色編號 117)
    "brown": "\033[38;5;130m",  # 棕色 (顏色編號 130)
    "lime_green": "\033[38;5;154m",  # 萊姆綠 (顏色編號 154)
    "deep_pink": "\033[38;5;197m",  # 深粉紅 (顏色編號 197)
    "orange": "\033[38;5;208m",  # 橘色 (顏色編號 208)
    "medium_gray": "\033[38;5;244m",  # 中灰色 (顏色編號 244)
    # --- 256 色模式背景範例 ( \033[48;5;{n}m ) ---
    #     (依顏色編號 n 排序)
    "bg_steel_blue": "\033[48;5;67m",  # 背景鋼藍色
    "bg_sky_blue": "\033[48;5;117m",  # 背景天藍色
    "bg_brown": "\033[48;5;130m",  # 背景棕色
    "bg_lime_green": "\033[48;5;154m",  # 背景萊姆綠
    "bg_deep_pink": "\033[48;5;197m",  # 背景深粉紅
    "bg_orange": "\033[48;5;208m",  # 背景橘色
    "bg_medium_gray": "\033[48;5;244m",  # 背景中灰色
    # --- True Color (24-bit) 前景範例 ( \033[38;2;{r};{g};{b}m ) ---
    #     (r, g, b 從 0 到 255)
    "true_orange": "\033[38;2;255;165;0m",  # RGB(255, 165, 0) 的橘色
    "true_teal": "\033[38;2;0;128;128m",  # RGB(0, 128, 128) 的藍綠色
    # --- True Color (24-bit) 背景範例 ( \033[48;2;{r};{g};{b}m ) ---
    #     (r, g, b 從 0 到 255)
    "bg_true_orange": "\033[48;2;255;165;0m",  # 背景 RGB(255, 165, 0) 的橘色
    "bg_true_teal": "\033[48;2;0;128;128m",  # 背景 RGB(0, 128, 128) 的藍綠色
    # --- 語意化顏色 (別名) ---
    #     (方便使用，這些是上面定義的別名)
    "critical": "\033[31;1m",  # 嚴重錯誤 (亮紅色)
    "debug": "\033[90m",  # 除錯 (深灰色)
    "error": "\033[31m",  # 錯誤 (紅色)
    "info": "\033[36m",  # 資訊 (青色)
    "success": "\033[32m",  # 成功 (綠色)
    "warning": "\033[33m",  # 警告 (黃色)
}


def select(select_type: str, give_road: str | None = None) -> str | None:
    if select_type == "file":
        return select_file_dir(give_road)
    elif select_type == "file+folder":
        return select_folder_file(give_road)
    elif select_type == "folder":
        return select_folder_dir(give_road)


def select_check_road(give_road: str | None = None) -> str:
    """select五件套的副程式，檢查路徑
    (return str)"""
    if give_road is None:
        RunningPath = os.getcwd()
    else:
        try:
            if os.path.isdir(give_road) is True:
                RunningPath = give_road
            elif os.path.isfile(give_road) is True:
                RunningPath = os.path.dirname(give_road)
        except FileNotFoundError:
            RunningPath = os.path.join(os.getcwd(), give_road)
    ##
    try:
        if os.path.isdir(RunningPath) is True:
            pass
        elif os.path.isfile(RunningPath) is True:
            # 正常情況不會出現
            RunningPath = os.path.dirname(RunningPath)
    except (FileNotFoundError, PermissionError):
        RunningPath = os.getcwd()
    ##
    if os.path.exists(RunningPath) is False:
        RunningPath = os.getcwd()
    ##
    return RunningPath


def select_error_tip(SelectedDir: str, DirNum: int):
    """select五件套的副程式，輸出錯誤原因"""
    SelectedDir = str(SelectedDir)
    if len(SelectedDir) > 1 and SelectedDir[0] == "0":
        print_color("light_red", "輸入錯誤，原因：數字前加入0")
        return
    try:
        SelectedDirInt = int(SelectedDir)
    except ValueError:
        print_color("light_red", "輸入非數字")
        print()
        return
    if SelectedDirInt < 0:
        print_color("light_red", "輸入錯誤：低於最低數（0）。")
        pass
    elif SelectedDirInt > DirNum:
        print_color("light_red", "輸入錯誤：高於檔案+資料夾數量。")
        pass
    else:
        print_color("bright_red", "未知錯誤，請再試一次。")
        pass
    print()
    return


def select_list_dir(RunningPath: str):
    """select五件套的副程式，列出所有檔案/資料夾"""
    try:
        AllDir = os.listdir(RunningPath)
        return AllDir
    except PermissionError as e:
        raise PermissionError(
            "發生錯誤，可能的原因：顯示需root的資料夾" + "\n" + "詳細資訊：" + str(e)
        )
    except FileNotFoundError as e:
        raise FileNotFoundError("找不到資料夾，詳細資訊：" + "\n" + str(e))


def select_print_dir(
    RunningPath: str,
    NumColor: str = "dim",
    PrintFile: bool = True,
    FileColor: str = "reset",
    PrintDir: bool = True,
    DirColor: str = "yellow",
    LineColor: str = "dark_gray",
    ConColor: str = "dim",
    ConText: str = "請輸入選擇的檔案/資料夾的編號： ",
    TipColor: str = "bright_yellow",
    PgNumColor: str = "dim",
    show_hide_file: bool = True,
    InputChoose: bool = True,
) -> list:
    """select五件套的副程式，顯示所有檔案/資料夾
    NumColor: str,數字顏色
    PrintFile: bool,是否顯示檔案
    FileColor: str,檔案顏色
    PrintDir: bool,是否顯示資料夾
    DirColor: str,資料夾顏色
    show_hide_file: bool,是否顯示隱藏（.開頭）檔案, (未測試，可能會發生錯誤)
    (return int, dict, str)"""
    DirNum: int = 0
    DirDict: dict = {}
    AllDir = select_list_dir(RunningPath)
    for Dirs in AllDir:
        FullPath = os.path.join(RunningPath, Dirs)
        if os.path.isfile(FullPath) is True and PrintFile is True:
            pass
        elif os.path.isdir(FullPath) is True and PrintDir is True:
            pass
        else:
            continue
        DirNum += 1
        DirNumStr = str(DirNum)
        DirDict[DirNumStr] = Dirs
    ##
    MaxDirNum = DirNum
    max_page_count = (MaxDirNum // 25) + 1
    page_num = 1
    list_min = 0
    list_max = 25
    while True:
        print_color(TipColor, "輸入n下一頁/b上一頁。")
        print_color(PgNumColor, "目前頁數：")
        print_color("bright_yellow", str(page_num))
        print_color(PgNumColor, "/")
        print_color("light_yellow", str(max_page_count))
        print()
        for DirNumStr in list(DirDict.keys())[list_min:list_max]:
            DirNum = int(DirNumStr)
            Dirs = DirDict[DirNumStr]
            FullPath = os.path.join(RunningPath, Dirs)
            print_space(NumColor, DirNumStr + "： ", 5)
            if Dirs[0] == "." and show_hide_file is False:
                continue
            if os.path.isfile(FullPath) is True and PrintFile is True:
                print_color(FileColor, Dirs)
            elif os.path.isdir(FullPath) is True and PrintDir is True:
                print_color(DirColor, Dirs + "/")
            print()
        line(LineColor)
        if InputChoose is False:
            return [DirNum, DirDict, ""]
        Selected = con(ConColor, ConText)
        if Selected in ["next", "n"]:
            list_min += 25
            list_max += 25
            page_num += 1
        elif Selected in ["back", "b"]:
            list_min -= 25
            list_max -= 25
            page_num -= 1
        elif Selected in ["cls", "clear"]:
            clear()
        else:
            return [MaxDirNum, DirDict, Selected]
        ##檢查
        if list_min < 0:
            print_color("light_red", "頁數低於1。")
            print()
            list_min += 25
            list_max += 25
            page_num += 1
        elif list_min > MaxDirNum:
            print_color("light_red", "頁數高於數量。")
            print()
            list_min -= 25
            list_max -= 25
            page_num -= 1
        else:
            pass


def select_folder_file(give_road: str | None = None) -> str:
    """選擇檔案或資料夾"""
    RunningPath = select_check_road(give_road)
    # main
    while True:
        print_color("reset", "")
        print()
        line("dark_gray")
        print_color("dim", "目前位子：")
        print_color("light_yellow", RunningPath)
        print()
        print_color("bg_dark_gray", "輸入finish(f)選擇資料夾")
        print_color("dim", "，請選擇檔案/資料夾：")
        print()
        print_color("dim", "0：返回上一個資料夾(../)")
        print()
        #
        DirNum, DirDict, SelectedDir = select_print_dir(
            RunningPath,
            NumColor="dim",
            PrintFile=True,
            FileColor="reset",
            PrintDir=True,
            DirColor="yellow",
        )
        #
        if SelectedDir in ["f", "finish"]:
            return RunningPath
        elif SelectedDir in ["0", "..", "../"]:
            RunningPath = os.path.dirname(RunningPath)
            continue
        elif SelectedDir in DirDict:
            FullPath = os.path.join(RunningPath, DirDict[SelectedDir])
            if os.path.isfile(FullPath) is True:
                return FullPath
            elif os.path.isdir(FullPath) is True:
                RunningPath = FullPath
                continue
        else:
            select_error_tip(SelectedDir, DirNum)


def select_file_dir(give_road: str | None = None) -> str:
    """自由選擇資料夾內的檔案"""
    RunningPath = select_check_road(give_road)
    # main
    while True:
        print_color("reset", "\n")
        line("green")
        print_color("light_green", RunningPath)
        print()
        print_color("reset", "請選擇一個檔案。")
        print()
        ##
        print_color("green", "0： 返回上一個資料夾(../)" + "\n")
        #
        FileNum, FileDict, SelectedFile = select_print_dir(
            RunningPath,
            NumColor="reset",
            PrintFile=True,
            FileColor="light_cyan",
            PrintDir=True,
            DirColor="purple",
            LineColor="green",
            ConColor="light_green",
            ConText="請輸入選擇的檔案的編號： ",
            TipColor="green",
            PgNumColor="light_green",
        )
        #
        if SelectedFile == "0":
            RunningPath = os.path.dirname(RunningPath)
            continue
        # 驗證是否輸入正確編號,在DirDict
        elif SelectedFile in FileDict:
            FullFilePath = os.path.join(RunningPath, FileDict[SelectedFile])
            if os.path.isfile(FullFilePath):
                return FullFilePath
            elif os.path.isdir(FullFilePath):
                RunningPath = FullFilePath
                continue
        else:
            # 告知使用者：詳細輸入錯誤原因。
            select_error_tip(SelectedFile, FileNum)


def select_file(give_road: str | None = None):
    """在指定的資料夾內選擇檔案"""
    RunningPath = select_check_road(give_road)
    # main
    while True:
        print_color("reset", "")
        print()
        line("cyan")
        print_color("light_cyan", "位子：")
        print_color("bright_cyan", RunningPath)
        print()
        print_color("light_cyan", "可選擇的檔案：")
        print()
        print_color("bright_cyan", "0：直接返回。")
        print()
        #
        file_num, file_dict, selected_file = select_print_dir(
            RunningPath,
            NumColor="light_cyan",
            PrintFile=True,
            FileColor="reset",
            PrintDir=False,
            LineColor="cyan",
            ConColor="light_cyan",
            ConText="請輸入要選擇的檔案的編號： ",
            TipColor="sky_blue",
            PgNumColor="steel_blue",
        )
        #
        if selected_file == "0":
            return None
        elif selected_file in file_dict:
            return os.path.join(RunningPath, file_dict[selected_file])
        else:
            ##詳細錯誤原因
            select_error_tip(selected_file, file_num)
            continue


def select_folder_dir(give_road: str | None = None) -> str:
    """在可以自由選擇資料夾的狀態，選擇資料夾。"""
    RunningPath = select_check_road(give_road)
    # main
    while True:
        print_color("reset", " ")
        print()
        line("dark_gray")
        print_color("dim", "目前位子：")
        print_color("light_yellow", RunningPath)
        print()
        print_color("dim", "請選擇一個資料夾，")
        print_color("bg_dark_gray", "輸入f完成：")
        print()
        print_color("bright_yellow", "0： 返回上一個資料夾(../)")
        print()
        #
        FolderNum, FolderDict, SelectedFolder = select_print_dir(
            RunningPath,
            NumColor="light_purple",
            PrintFile=False,
            PrintDir=True,
            DirColor="reset",
            ConText="請輸入選擇的資料夾的編號： ",
        )
        #
        if SelectedFolder == "0":
            RunningPath = os.path.dirname(RunningPath)
            continue
        elif SelectedFolder in ["f", "finish", "finished"]:
            return RunningPath
        elif SelectedFolder in FolderDict:
            RunningPath = os.path.join(RunningPath, FolderDict[SelectedFolder])
        else:
            # 詳細錯誤原因
            select_error_tip(SelectedFolder, FolderNum)


def select_folder(give_road: None | str = None):
    """在指定的資料夾內選擇資料夾"""
    RunningPath = select_check_road(give_road)
    #
    while True:
        folder_num = 0
        folder_dict = {}
        print_color("reset", "\n")
        line("purple")
        print_color("light_purple", "位子：")
        print_color("bright_purple", RunningPath)
        print()
        print_color("light_purple", "可選擇的資料夾：")
        print()
        print_color("bright_purple", "0：直接返回。")
        print()
        #
        folder_num, folder_dict, selected_folder = select_print_dir(
            RunningPath,
            NumColor="light_purple",
            PrintFile=False,
            PrintDir=True,
            DirColor="reset",
            LineColor="purple",
            ConText="請輸入要選擇的資料夾編號： ",
            ConColor="light_purple",
            TipColor="bright_purple",
            PgNumColor="purple",
        )
        #
        if selected_folder == "0":
            return None
        elif selected_folder in folder_dict:
            return os.path.join(RunningPath, folder_dict[selected_folder])
        else:
            ##詳細原因
            select_error_tip(selected_folder, folder_num)


def credit(clean_screen: bool = False, clean_type: str = "command"):
    """顯示作者
    用法：
        `need_clean`
            True時,清楚螢幕上的內容
            False時,不清除
    (return None)"""
    if clean_screen is True:
        clear(clean_type)
    print_color("purple", CREDIT_TEXT_1)
    print()
    print_color("purple", CREDIT_TEXT_2)
    print()
    print_color("bright_cyan", CREDIT_TEXT_5)
    print()
    return None


def welcome(clean_screen: bool = False, clean_type: str = "command"):
    """
    用法：
        `clean_screen` 選項
            =>True  清除螢幕上的內容（文字）
            =>False 不清除
    (return None)"""
    if clean_screen is True:
        clear(clean_type)
    print_color("bright_blue", WELCOME_TEXT_PT)
    print()
    return None


def clear(clear_type="command"):
    """清楚螢幕上的內容
    用法：
        `clear_type`可用選項:
            =>command   這是最推薦的選項
            =>unicode   不推薦，效果不佳
            =>count     大量換行
    (return None)"""
    if clear_type in ["command", "命令"]:
        if os.name == "nt":
            subprocess.run("cls", shell=True)
        else:
            subprocess.run(["clear"])
    elif clear_type in ["unicode", "編碼"]:
        print_color("reset", "\033[H \033[J")
    elif clear_type in ["count", "數量"]:
        print_color("reset", "\n" * 100000000)
    #
    return None


def print_color(color_give: str = "reset", *texts, end: str = "", type: str = "python"):
    r"""顯示多段相同顏色的文字，不換行
    用法：
        `color_give`    類型: 字串str，來自COLORS字典的顏色
        `end`           不會有顏色的文字，可以放「\r」 或 「\n」之類的
    """
    pt_logger.debug(f"(pt) [print_color] 顏色：「{color_give}」 | 文字：「{texts}」")
    color_code = ""
    color_list = get_parts(color_give.strip(), split_item=",")
    for color in color_list:
        if color in COLORS:
            color_code = color_code + COLORS[color]
    #
    all_text = ""
    for text in texts:
        all_text = all_text + str(text)
    ######
    finish_text = color_code + all_text + COLORS["reset"] + end
    if type in ["python", "py"]:
        print(finish_text, end="")
        ###
        if end == "\r":
            print(" " * 100, end="\r")
    elif type in ["sys"]:
        sys.stdout.write(finish_text)
        sys.stdout.flush()
    else:
        pt_logger.warning(f"(pt)[print_color]未知類型：「{type}」")


def print_space(
    color: str,
    text: str,
    space_long: int,
    from_front: bool = True,
    print_it: bool = True,
    fill_item: str = " ",
    real_space: bool = True,
):
    """在給予的文字前加入指定數量的空格，並顯示
    `space_long`
        文字需要的長度
    `from_front`
        true時從前方加
        Flase時從後方加
    `print_it`
        True時會在加完空格後顯示(return None)
        False時不顯示，但會返回(return)加完空格的字(str)
    `fill_item`
        選擇填充物(預設為空格)
    `real_space`
        True時  中文為2個fill_item，英文為1個fill_item
        False時 中文為1個fill_item，英文為1個fill_item
    (return None | str)"""
    text2print = str(text)
    if real_space is True:
        text_len = 0
        for i in text2print:
            if (unicodedata.east_asian_width(i) in ("W", "F")) is True:
                text_len += 2
            else:
                text_len += 1
    elif real_space is False:
        text_len = len(text2print)
    #
    if space_long > text_len:
        need_space = str(fill_item) * (space_long - text_len)
        if from_front is True:
            text2print = need_space + text2print
        elif from_front is False:
            text2print = text2print + need_space
    ##
    if print_it is True:
        print_color(color, text2print)
        return None
    elif print_it is False:
        return text2print


def print_long(
    color: str = "reset",
    text: str = PT_change_log,
    page_long_size: int = 25,
    clean_type: str = "command",
):
    """顯示很長的文字
    (return None)"""
    text_str: str = str(text)
    text_list: list = get_parts(text_str, split_item="\n")
    list_long_max: int = page_long_size
    list_long_min: int = 0
    while True:
        clear(clean_type)
        for i in range(list_long_min, list_long_max):
            if i > (len(text_list) - 1):
                break
            elif i == (len(text_list) - 1):
                print_color(color, text_list[i])
                print()
                print_color("dim", "（文字結尾）")
                print()
                break
            else:
                print_color(color, text_list[i])
                print()
        print()
        user_choose = con("bg_true_teal", "下一頁n/上一頁b，返回q： ")
        if user_choose in ["q", "quit"]:
            return None
        elif user_choose in ["n", "next"]:
            list_long_min += page_long_size
            list_long_max += page_long_size
            if list_long_max > len(text_list):
                list_long_max = len(text_list)
                list_long_min = list_long_max - page_long_size
                continue
        elif user_choose in ["b", "back"]:
            list_long_min -= page_long_size
            list_long_max -= page_long_size
            if list_long_min < 0:
                list_long_max = 0 - list_long_min
                list_long_min = 0
                continue
        else:
            clear()
            print_color("red", "未知指令!")
            print()
            con()


def print_len(
    color: str,
    text: str,
    len_long: int,
    print_it: bool = True,
    fill_item: str = " ",
    shorter_item: str = "...",
):
    """顯示或返回指定長度的文字
    用法：
        `color`, 類型: str，顏色
        `text`, 建議類型: str，註：不管哪種類型都會str(text)
        `print_it`
            True時,顯示(返回 None)
            False時,不顯示，返回結果文字
        `fill_item`, 建議類型: str，預設“ ”（空格）在長度不足時使用，註：不管哪種類型都會str(text)
    (return str | None)"""
    text_str = str(text)
    text_str_len = len(text_str)
    shorter_item_str = str(shorter_item)
    shorter_item_str_len = len(shorter_item_str)
    #
    if text_str_len > len_long:
        finish_text = text_str[: (len_long - shorter_item_str_len)] + str(shorter_item)
    elif text_str_len == len_long:
        finish_text = text_str
    elif text_str_len < len_long:
        need_len = len_long - text_str_len
        need_space = str(fill_item) * need_len
        finish_text = text_str + need_space
    #
    if print_it is True:
        print_color(color, finish_text)
        return None
    elif print_it is False:
        return finish_text


def color_text(
    color_give: str | list = "reset", text: str | list = "", ResetIt: bool = True
) -> str:
    """將文字著色
    用法：
        `color_give_str`    類型: str   ，來自COLORS字典的顏色
        `text`              類型: str   ，將要著色的文字
        `ResetIt`           類型: bool  ，是否在文字後面加上重置顏色的'\\033[0m'
    例：
        >>>print(color_text("red", "這是紅色文字"))
        這是紅色文字
        >>>print(color_text("green, bg_yellow", "這是綠色文字，背景黃色"))
        這是綠色文字，背景黃色
    (return str)"""
    if type(text) is str:
        text_str = text
    elif type(text) is list:
        text_str = "".join(text)
    color_code = ""
    ##
    if type(color_give) is list:
        color_list = color_give.copy()
    elif type(color_give) is str:
        color_list = [color_give]
    ##
    for color in color_list:
        if color in COLORS:
            color_code = color_code + COLORS[color]
    if ResetIt is True:
        return color_code + text_str + COLORS["reset"]
    else:
        return color_code + text_str


def print_right(
    color: str,
    text: str,
    already_text: int | str = 0,
    print_it: bool = True,
    fill_item: str = " ",
    real_space: bool = True,
) -> str | None:
    """
    already_text 如前面有文字，輸入文字數量(中文需*2)
    (return str | None)"""
    already_text_int: int = 0
    if type(already_text) is int:
        already_text_int = already_text
    elif type(already_text) is str:
        for i in already_text:
            if (
                real_space is True
                and (unicodedata.east_asian_width(i) in ("W", "F")) is True
            ):
                already_text_int += 2
            else:
                already_text_int += 1
    #
    width = shutil.get_terminal_size().columns
    finish_text = print_space(
        color,
        text,
        width - already_text_int,
        from_front=True,
        print_it=False,
        fill_item=fill_item,
    )
    if print_it is True:
        print_color(color, finish_text)
        return None
    elif print_it is False:
        return finish_text


def print_middle(
    color,
    text,
    already_text: int | str = 0,
    print_it: bool = True,
    real_space: bool = True,
) -> str | None:
    """
    already_text 如前面有文字，輸入文字數量(中文需*2)
    (return str | None)"""
    if type(already_text) is int:
        already_text_int = already_text
    elif type(already_text) is str:
        already_text_int = 0
        for i in already_text:
            if (
                real_space is True
                and (unicodedata.east_asian_width(i) in ("W", "F")) is True
            ):
                already_text_int += 2
            else:
                already_text_int += 1
    #
    width = shutil.get_terminal_size().columns
    if print_it is True:
        print_space(color, text, (width // 2) - already_text_int, from_front=True)
        return None
    elif print_it is False:
        return print_space(
            color,
            text,
            (width // 2) - already_text_int,
            from_front=True,
            print_it=False,
        )


def print_down(color: str, text: str):
    # 取得終端畫面尺寸
    size = shutil.get_terminal_size()
    rows = size.lines  # 總列數

    # ANSI 控制碼移動游標到最下方第一個位置（左下角）
    print_color(color, f"\033[{rows};1H{text}")


def line(
    color: str = "purple",
    fill_item: str = "-",
    line_count: int = 1,
    line_long: int = 12,
    full_screen: bool = False,
):
    """顯示一條線"""
    if full_screen is True:
        line_text = fill_item * shutil.get_terminal_size().columns
    else:
        line_text = (str(fill_item) * line_long) * line_count
    print_color(color, line_text)


def get_parts(text, split_item="_"):
    """取得每段的內容
    例：
        >>>print(get_parts('a_b_c'))
        ['a', 'b', 'c']
        >>>print(get_parts('1-2-3', '-'))
        ['1', '2', '3']
    (return all_lines: list)"""
    text_str = str(text)
    text_str_len = len(text_str)
    split_item_str = str(split_item)
    all_lines = []
    split_item_str_len = len(split_item_str)
    tmp_parts = ""
    i = 0
    while i < text_str_len:
        # 若剩餘長度小於分隔符長度，直接加剩下的內容
        if (i + split_item_str_len) > text_str_len:
            tmp_parts += text_str[i:]
            break
        # 若當前為分隔符
        if text_str[i : i + split_item_str_len] == split_item_str:
            all_lines.append(tmp_parts)
            tmp_parts = ""
            i += split_item_str_len
        else:
            tmp_parts = tmp_parts + text_str[i]
            i += 1
    # while 結束後，補上最後一段（若有內容）
    if tmp_parts != "" or (text_str.endswith(split_item_str)):
        all_lines.append(tmp_parts)
    return all_lines


def get_values(text: str, start: str, end: str | None = None) -> list:
    """
    用法：
        >>>print(get_values('-abc-', '-', '-'))
        ['abc']
        >>>print(get_values('+abc- +def-', '+', '-'))
        ['abc', 'def']
    (return all_values: list)"""
    all_values: list = []
    in_value: int = 0
    tmp: str = ""
    if end is None:
        end = start
    for i in text:
        if (in_value == 0) and (i != start):
            pass
        elif i == start:
            in_value += 1
        elif (in_value > 0) and (i != start) and (i != end):
            tmp = tmp + i
        elif (in_value > 0) and (i == end):
            in_value -= 1
            all_values.append(tmp)
            tmp = ""
    return all_values

def con(
    color_give: str = "reset",
    text: str | None = None,
    ExitInput: bool = True,
) -> str:
    """有顏色的文字，並輸入
    功能：
    `color`,可輸入COLORS字典有的顏色
    `ExitInput`
        True    時輸入「exit」會退出
        False   時不會退出
    """
    color_code = ""
    color_list = get_parts(color_give.strip(), split_item=",")
    for color in color_list:
        if color in COLORS:
            if color_code == "":
                color_code = COLORS[color]
            elif color_code != "":
                color_code = color_code + COLORS[color]
    #
    if text is None:
        text = "要繼續嗎 enter？退出輸入exit\n"
    colored_text = color_code + str(text) + COLORS["reset"]
    try:
        tmp_con = input(colored_text)
    except (EOFError, KeyboardInterrupt):
        exit()
    #
    if ExitInput is True and tmp_con.lower().strip() in ["exit", "exit()"]:
        exit()
    else:
        return tmp_con


def test() -> None:
    """測試功能"""
    global pt_ver
    welcome()
    print_color("bg_cyan", "Positive Tool工具箱版本:" + pt_ver)
    print()
    con()
    credit()
    print_color("bg_cyan", "PT by TW_bh")
    print()
    con()
    print()
    print_color("light_blue", "更改日誌：")
    print()
    print_color("cyan", PT_change_log)
    print()
    con("bg_blue", "有顏色的輸入測試文字(輸入enter)")
    ###
    print_color("dim", "功能測試<<")
    line()
    line()
    line()
    #
    print()
    print_space("reset", "顏色", 10, from_front=True, print_it=True, fill_item=" ")
    print_space("reset", "文字", 25, from_front=True, print_it=True, fill_item=" ")
    print()
    color_names = list(COLORS.keys())
    for test_color in color_names:
        print_space("reset", test_color, 20, from_front=False)
        print_space(
            test_color,
            "< 這是有顏色的測試文字" + test_color,
            30,
            from_front=False,
        )
        print_color(test_color, ">")
        print()
    #
    # 選擇檔案
    print("你選擇了：" + str(select_file_dir()) + "。")
    # 選擇資料夾
    print("你選擇了：" + str(select_folder_dir()) + "。")
    ##
    print("你選擇了：" + str(select_folder_file()) + "。")
    ##
    print()
    print()
    print_color("bold", "[print_len]測試文字：「文字，文字，文字，還是文字」")
    print()
    print_color("dim", "不完全顯示")
    print_len("reset", "    =>文字，文字，文字，還是文字", 15)
    print()
    print_color("dim", "完全顯示  ")  # 手動對其，因為中文所占空間=兩個英文
    print_len("reset", "    =>文字，文字，還是文字", 30)
    print()
    #
    print(get_values("a>c><v<b", ">", "<"))
    ##
    print()
    line()
    line()
    line()
    print_color("green", ">>測試完畢")
    print()


if __name__ == "__main__":
    test()
