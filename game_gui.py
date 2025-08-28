import logging
import os
import datetime
import threading
import time

from pt import pt_ver
from dearpygui import dearpygui as dpg
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QApplication,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QMessageBox,
    QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QFont, QFontDatabase

gobang_ver: str = "b-2"
gobang_pre_ver: bool = True

gobang_logger = logging.getLogger("五子棋Gobang_logger")

font_path = os.path.join(
    ".", "font", "Noto_Sans_TC", "static", "NotoSansTC-Regular.ttf"
)

start_time = 0
count_time = 0
board_size_x: int = 19
board_size_y: int = 19
board_data: dict = {}
turn: str = "藍"  # sky_blue
##藍sky_blue→橘orange→青cyan→棕brown  詳見：player_num
turn_num: int = 1

player_count: int = 2
##紀錄有幾個玩家遊玩

win_need: int = 5
##連幾格獲勝

player_color: dict = {
    "空": [255, 255, 255, 255],
    "數字": [219, 216, 0, 255],
    ##
    "藍": [0, 165, 255, 255],
    "橘": [255, 165, 0, 255],
    "青": [0, 255, 255, 255],
    "棕": [165, 42, 42, 255],
    "紫": [128, 0, 128, 255],
    "灰": [128, 128, 128, 255],
    "紅": [255, 0, 0, 255],
    "綠": [0, 255, 0, 255],
}
player_num: dict = {
    1: "藍",
    2: "橘",
    3: "青",
    4: "棕",
    5: "紫",
    6: "灰",
    7: "紅",
    8: "綠",
}
##計算最多人數
max_player_count: int = 0
for init_num in player_num:
    max_player_count = init_num

game_started: bool = False
game_finished: bool = False

setting: dict = {
    "show_out_of_board": False,
}

class main(QWidget):
    def __init__(self):
        super().__init__()
        self.app()

    def app(self):
        global gobang_ver, max_player_count
        layout = QVBoxLayout()
        v = QLabel("五子棋")
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(v)
        v = QLabel(f"版本 v({gobang_ver})")
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(v)
        #
        v = QLabel(f"pt版本：{pt_ver}")
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(v)
        #
        r_layout = QHBoxLayout()
        v = QLabel("連幾格獲勝：")
        self.le1 = QLineEdit()
        self.le1.setValidator(QIntValidator(2, 100))
        self.le1.setText("5")
        r_layout.addWidget(v)
        r_layout.addWidget(self.le1)
        layout.addLayout(r_layout)
        #
        r_layout = QHBoxLayout()
        v = QLabel("玩家數量：")
        self.le2 = QLineEdit()
        self.le2.setValidator(QIntValidator(2, max_player_count))
        self.le2.setText("2")
        r_layout.addWidget(v)
        r_layout.addWidget(self.le2)
        layout.addLayout(r_layout)
        #
        r_layout = QHBoxLayout()
        v = QLabel("(x)橫向棋盤長度：")
        self.le3 = QLineEdit()
        self.le3.setValidator(QIntValidator(5, 100))
        self.le3.setText("19")
        r_layout.addWidget(v)
        r_layout.addWidget(self.le3)
        layout.addLayout(r_layout)
        #
        r_layout = QHBoxLayout()
        v = QLabel("(y)直向棋盤長度：")
        self.le4 = QLineEdit()
        self.le4.setValidator(QIntValidator(5, 100))
        self.le4.setText("19")
        r_layout.addWidget(v)
        r_layout.addWidget(self.le4)
        layout.addLayout(r_layout)
        #
        self.cb1 = QCheckBox("超出範圍顯示")
        self.cb1.setChecked(False)
        layout.addWidget(self.cb1)
        #
        v = QPushButton("> 開始遊戲 <")
        v.clicked.connect(self.button_clicked)
        layout.addWidget(v)
        ###
        self.setLayout(layout)
        self.setWindowTitle("Gobang GUI")
        self.resize(540, 360)

    def button_clicked(self):
        global player_count
        global win_need
        global board_size_x, board_size_y
        global game_started, game_finished
        global setting
        if game_started is True:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setText("已有遊戲進行中!")
            msg_box.setWindowTitle("Gobang GUI 通知")
            msg_box.exec()
        else:
            game_started = True
            game_finished = False
            setting["show_out_of_board"] = self.cb1.isChecked()
            win_need = int(self.le1.text())
            player_count = int(self.le2.text())
            board_size_x = int(self.le3.text()) + 1
            board_size_y = int(self.le4.text()) + 1
            init()
            start_game()


def start_game():
    global font_path, turn, turn_num
    #
    turn_num = 1
    turn = player_num[turn_num]
    #
    dpg.create_context()
    with dpg.font_registry():
        with dpg.font(font_path, 30) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
    dpg.bind_font(default_font)
    dpg.create_viewport(title="Gobang GUI (game)")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()
    window = game()
    dpg.set_viewport_resize_callback(window.board_window_resizer)
    dpg.start_dearpygui()
    dpg.destroy_context()


class game:
    def __init__(self) -> None:
        self.create_choosed_window()
        self.out_of_board_create()
        self.create_notification_window()
        self.create_control_center()
        #
        dpg.set_exit_callback(self.__exit__)
        #game
        self.create_board()
        #
        update_thread = threading.Thread(target=self.data_updater)
        update_thread.start()
        #dpg.set_frame_callback(1, self.control_center_resizer)

    def create_board(self):
        global board_data, board_size_x, board_size_y
        with dpg.window(
                label="Gobang GUI 棋盤",
                width=dpg.get_viewport_width() - 10,
                height=dpg.get_viewport_height() - 10,
                tag="board_window",
                pos=[0, 0],
                no_close=True,
            ):
            #
            dpg.add_drawlist((30 * board_size_x), (30 * board_size_y), tag="board_drawing")
            #
            dpg.draw_text([0, 0], "現在是隊的下棋時間", size=30, tag="turn_text")
            self._change_turn__turn_text()
            #
            #all_num_list = []
            for x in range(1, board_size_x):
                #all_num_list.append(print_space("", str(i), 2, print_it=False, fill_item=" "))
                #dpg.draw_text([0, 0], "     " + "  ".join(all_num_list), size=30)
                pos_x = x * 30
                dpg.draw_text([pos_x, 30], str(x), size=30, color=player_color["數字"])
            #
            for y in range(1, board_size_y):
                pos_y = y * 30 + 30
                dpg.draw_text([0, pos_y], str(y), size=30, color=player_color["數字"])
            #
            for x in range(1, board_size_x):
                for y in range(1, board_size_y):
                    pos_x = x * 30
                    pos_y = y * 30 + 30
                    dpg.draw_text(
                        [pos_x, pos_y],
                        board_data[f"{x}~{y}"],
                        color=player_color[board_data[f"{x}~{y}"]],
                        size=30,
                        tag=f"piece_{x}~{y}"
                    )
        with dpg.handler_registry():
            dpg.add_mouse_click_handler(0, callback=self.get_click_pos)

    def redraw_board(self):
        global board_data, board_size_x, board_size_y
        for x in range(1, board_size_x):
            for y in range(1, board_size_y):
                #pos_x = x * 30
                #pos_y = y * 30
                #dpg.set_value(
                #    f"piece_{x}~{y}",
                #    board_data[f"{x}~{y}"],
                    #
                    # color=player_color[board_data[f"{x}~{y}"]],
                #)
                dpg.configure_item(
                    f"piece_{x}~{y}",
                    text=board_data[f"{x}~{y}"],
                    color=player_color[board_data[f"{x}~{y}"]]
                )

    def get_click_pos(self, sender, app_data) -> None:
        global board_size_x, board_size_y, setting, game_finished
        if game_finished is True:
            return None
        if (dpg.is_item_shown("choosed_window") is True) or (dpg.is_item_shown("notification_window") is True):
            return None
        pos_xy = dpg.get_mouse_pos()
        pos_x = pos_xy[0]
        pos_y = pos_xy[1]
        #x
        x = 0
        for i in range(1, board_size_x + 1):
            a = i * 30 - 30
            b = i * 30
            if pos_x in range(a, b):
                x = i
                break
        x -= 1
        #y
        y = 0
        for i in range(1, board_size_x + 2):
            a = i * 30 - 30
            b = i * 30
            if pos_y in range(a, b):
                y = i
                break
        y -= 2
        #
        if (y <= 0) or (x <= 0):
            if setting["show_out_of_board"] is True:
                gobang_logger.debug(f"超出棋盤範圍，Y：{y} X：{x}")
                self.out_of_board_show()
                return None
            else:
                return None
        #
        xy = f"{x}~{y}"
        if board_data[xy] != "空":
            self.already_piece(xy)
            return None
        board_data[xy] = turn
        #print(board_data, end="\n\n")
        #
        ##dpg.set_value("choosed_window_text", f"{turn}隊選擇({xy})")
        ##dpg.show_item("choosed_window")
        self.check_win()
        if game_finished is True:
            return None
        self.push_notification(f"{turn}隊選擇({xy})")
        #self.redraw_board()
        dpg.configure_item(
            f"piece_{x}~{y}",
            text=board_data[f"{x}~{y}"],
            color=player_color[board_data[f"{x}~{y}"]]
        )
        self.change_turn()
        return None

    def create_choosed_window(self):
        with dpg.window(modal=True, tag="choosed_window", show=False):
            dpg.add_text("", tag="choosed_window_text")
            dpg.add_button(label="確定", callback=self.close_choosed_window)

    def out_of_board_show(self):
        dpg.show_item("out_of_board")

    def out_of_board_hide(self):
        dpg.hide_item("out_of_board")

    def out_of_board_create(self):
        with dpg.window(label="Gobang GUI 通知", modal=True, tag="out_of_board", show=False):
            dpg.add_text("超出棋盤")
            dpg.add_button(label="確定", callback=self.out_of_board_hide)

    def close_choosed_window(self):
        dpg.hide_item("choosed_window")

    def already_piece(self, piece_pos):
        self.push_notification(f"該位子已有旗子({piece_pos})")

    def change_turn(self):
        global turn_num, player_num ,turn
        turn_num += 1
        if turn_num > player_count:
            turn_num = 1
        #
        turn = player_num[turn_num]
        self._change_turn__turn_text()

    def _change_turn__turn_text(self):
        #dpg.set_item_label("board_window", f"現在是{turn}隊的下棋時間")
        dpg.configure_item(
            "turn_text",
            text=f"現在是{turn}隊的下棋時間",
            color=player_color[turn]
        )

    def create_notification_window(self):
        window_width = 250
        window_height = 150
        pos_width = dpg.get_viewport_width()
        pos_height = dpg.get_viewport_height()
        window_pos_width = (pos_width - window_width) // 2
        window_pos_height = (pos_height - window_height) // 2
        with dpg.window(label="Gabang GUI 通知", tag="notification_window", pos=[window_pos_width, window_pos_height], show=False, modal=True, height=window_height, width=window_width):
            dpg.add_text("", tag="notification_text")
            dpg.add_button(label="確定", callback=self.hide_notification_window)

    def hide_notification_window(self) -> None:
        dpg.hide_item("notification_window")
        return None

    def show_notification_window(self) -> None:
        dpg.show_item("notification_window")
        return None

    def push_notification(self, text: str):
        dpg.set_value("notification_text", text)
        self.show_notification_window()

    def check_win(self):
        global board_size_x, board_size_y, board_data, win_need
        for y in range(1, board_size_y + 1):
            for x in range(1, board_size_x + 1):
                xy = str(x) + "~" + str(y)
                tmp = board_data[xy]
                #
                right_num = 0
                won_list = []
                for xplus in range(win_need):
                    #避免超出棋盤
                    if xplus > board_size_x:
                        break
                    #
                    x_tmp = x + xplus
                    if self.check(tmp, y, x_tmp) is True:
                        right_num += 1
                        won_list.append(str(x_tmp) + "~" + str(y))
                    else:
                        break
                if right_num >= win_need:
                    self.won(tmp, won_list)
                ##
                #
                right_num = 0
                won_list = []
                for yplus in range(win_need):
                    #避免超出棋盤
                    if yplus > board_size_y:
                        break
                    #
                    y_tmp = y + yplus
                    if self.check(tmp, y_tmp, x) is True:
                        right_num += 1
                        won_list.append(str(x) + "~" + str(y_tmp))
                    else:
                        break
                if right_num >= win_need:
                    self.won(tmp, won_list)
                ##
                #
                right_num = 0
                won_list = []
                for plus_num in range(win_need):
                    x_tmp = x + plus_num
                    y_tmp = y + plus_num
                    #避免超出棋盤
                    if (x_tmp > board_size_x) or (y_tmp > board_size_y):
                        break
                    #
                    if self.check(tmp, y_tmp, x_tmp) is True:
                        right_num += 1
                        won_list.append(str(x_tmp) + "~" + str(y_tmp))
                    else:
                        break
                if right_num >= win_need:
                    self.won(tmp, won_list)
                ##
                right_num = 0
                won_list = []
                for plus_num in range(win_need):
                    y_tmp = y + plus_num
                    x_tmp = x - plus_num
                    #避免超出棋盤
                    if (x_tmp < 0) or (y_tmp > board_size_y):
                        break
                    #
                    if self.check(tmp, y_tmp, x_tmp) is True:
                        right_num += 1
                        won_list.append(str(x_tmp) + "~" + str(y_tmp))
                    else:
                        break
                if right_num >= win_need:
                    self.won(tmp, won_list)
                #


    def check(self, tmp, y, x):
        global board_data, board_size_y, board_size_x
        xy = str(x) + "~" + str(y)
        if y > board_size_y or x > board_size_x:
            return False
        if y < 0 or x < 0:
            return False
        if (
            y <= board_size_y
            and x <= board_size_x
            and y > 0
            and x > 0
            and tmp == board_data[xy]
            and tmp != "空"
        ):
            return True


    def won(self, tmp, won_list):
        """
        won_list 目前未完成
        """
        global game_finished
        gobang_logger.debug("won")
        self.push_notification(f"{tmp}隊贏了")
        dpg.configure_item("turn_text", text=f"遊戲結束，{tmp}隊獲勝")
        game_finished = True

    def board_window_resizer(self, sender, app_data, user_data):
        dpg.set_item_height("board_window", dpg.get_viewport_height() - 210)
        dpg.set_item_width("board_window", dpg.get_viewport_width() - 10)
        dpg.set_item_width("control_center_window", dpg.get_viewport_width() - 10)

    def create_control_center(self):
        with dpg.window(
            label="Gobang GUI 控制中心",
            height=200,
            width=dpg.get_viewport_width(),
            no_close=True,
            tag="control_center_window"
        ):
            time_formated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dpg.add_text(f"遊戲開始時間：{time_formated}", pos=[10, 30])
            dpg.add_text(f"目前時間：{time_formated}", tag="control_center__time_text", pos=[500, 30])

    def control_center_resizer(self) -> None:
        if dpg.get_item_state("board_window")['visible'] is True:
            # 獲取第一個視窗的位置和高度
            first_window_pos = dpg.get_item_pos("board_window")
            first_window_height = dpg.get_item_height("board_window")
            # 計算第二個視窗的新位置
            # X 座標與第一個視窗相同
            # Y 座標為第一個視窗的 Y 加上其高度 (留一點間隙)
            if type(first_window_height) is int:
                new_y_pos = first_window_pos[1] + first_window_height + 5  # 加5作為間隙
                # 設定第二個視窗的新位置
                dpg.set_item_pos("control_center_window", [first_window_pos[0], new_y_pos])
            else:
                pass
            return None
        else:
            window_pos = dpg.get_item_pos("board_window")
            dpg.set_item_pos("control_center_window", [0, window_pos[1] + 35])

    def control_center_time_updater(self):
        time_formated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dpg.set_value("control_center__time_text", f"目前時間：{time_formated}")


    def data_updater(self):
        global game_started
        while True:
            if game_started is False:
                break
            else:
                self.control_center_resizer()
                self.control_center_time_updater()
                time.sleep(0.8)
        return None

    def __exit__(self, _):
        global game_started
        game_started = False


def init():
    global board_size_x, board_size_y, board_data
    # 清空並初始化 board_data
    board_data.clear()
    for x in range(board_size_x + 1):
        for y in range(board_size_y + 1):
            xy = str(x) + "~" + str(y)
            board_data[xy] = "空"
    #
    for x in range(board_size_x, board_size_x + 10):
        for y in range(board_size_y, board_size_y + 10):
            board_data[f"{x}~{y}"] = "空"

class launch:
    def __init__(self) -> None:
        global font_path
        ###
        app = QApplication()
        # 載入字型
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app_font = QFont(family, 12)  # 12為字體大小，可自行調整
        else:
            app_font = QFont("Microsoft JhengHei", 12)  # 若載入失敗則用系統字型
        app.setFont(app_font)
        self.window = main()
        self.window.show()
        app.exec()
        ###

    def close_window(self):
        self.window.hide()

    def show_window(self):
        self.window.show()





if __name__ == "__main__":
    launch()
