# tkinter: GUIアプリケーション作成用の標準ライブラリ。
import tkinter as tk
# tkinter.messagebox: ポップアップメッセージボックスを表示するためのモジュール。
from tkinter import messagebox

# pip install pyzbar
# pyzbar: バーコードおよびQRコードを読み取るためのライブラリ。
import pyzbar.pyzbar as pyzbar

# pip install Pillow
# PIL: Python Imaging Library、画像処理を行うためのライブラリ。
from PIL import Image, ImageGrab, ImageTk

# pip install clipboard
# clipboard: クリップボード操作を行うためのライブラリ。
import clipboard

# threading: マルチスレッド処理を可能にするモジュール。
from threading import Thread

# time: 時間に関連する関数を提供するモジュール。
import time

# pip install pyautogui
# pyautogui: GUI操作を自動化するためのライブラリ。
import pyautogui



def launch_screenshot_tool():
    """
    スクリーンショット取得ツールを起動する関数。
    キーボードショートカット[shift]+[windows]+[s]をシミュレートして、スクリーンショットツールを起動します。
    """
    
    # [shift]+[windows]+[s]キーを送りSnipping Toolを起動
    pyautogui.hotkey('shift', 'win', 's')


def read_codes_from_clipboard(image):
    """
    与えられた画像からバーコードまたはQRコードを読み取り、デコードする関数。
    引数:
        image (Image): PIL Image オブジェクト。
    戻り値:
        list: 読み取ったコードのデータを含むリスト。コードがなければ空のリストを返します。
    """
    try:
        codes = pyzbar.decode(image)
        return [code.data.decode('utf-8') for code in codes]
    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました: {e}")
        return []


# 一致判定用リスト（ここに一致させたいデータを追加）
MATCH_LIST = ["JRWEST", ""]

def check_match(codes):
    """
    読み取ったコードがMATCH_LISTに一致するか判定し、ラベルに表示
    """
    for code in codes:
        if code in MATCH_LIST:
            lbl_match.config(text=f"一致しました: {code}", fg="green")
            return
    lbl_match.config(text="一致するデータはありません", fg="red")


def update_codes_display():
    """
    クリップボードを定期的に監視し、新しい画像がある場合はその画像からコードを読み取り、
    テキストボックスに表示する関数。また、画像をGUIのキャンバスに表示します。
    """
    while not exit_flag:
        try:
            img = ImageGrab.grabclipboard()
            if img and isinstance(img, Image.Image):  # imgがPIL Imageオブジェクトであることを確認
                # キャンバスサイズに応じて画像を縮小して表示
                canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()
                img_width, img_height = img.size
                scale = min(canvas_width / img_width, canvas_height / img_height)
                if scale < 1:
                    img = img.resize((int(img_width * scale), int(img_height * scale)))

                # キャンバスに画像配置
                photo = ImageTk.PhotoImage(img)
                canvas.create_image(10, 10, image=photo, anchor=tk.NW) # 左上から10ピクセル右、10ピクセル下の位置に画像配置
                canvas.image = photo  # イメージオブジェクトを保持

                # 画像からバーコードやQRコードを読み込み
                codes = read_codes_from_clipboard(img)
                if codes:
                    codes_text = '\n'.join(reversed(codes))
                    txt_codes.delete('1.0', tk.END)
                    txt_codes.insert(tk.END, codes_text)
                    
                    # 一致する部分を抽出して表示
                    matched = [code for code in codes if code in MATCH_LIST and code]
                    if matched:
                        lbl_match.config(text=f"一致: {', '.join(matched)}", fg="green")
                    else:
                        lbl_match.config(text="一致するデータはありません", fg="red")
                else:
                    lbl_match.config(text="一致するデータはありません", fg="red")

            time.sleep(2)  # 2秒間隔でクリップボードを監視
        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました: {e}")



def copy_clipboard(text):
    """
    指定されたテキストをクリップボードにコピーする関数。
    引数:
        text (str): クリップボードにコピーするテキスト。
    """
    clipboard.copy(text)


def copy_button_on_click():
    """
    「クリップボードにコピー」ボタンがクリックされた際の処理
    テキストボックスの内容をクリップボードにコピーし、成功メッセージを表示します。
    """
    text = txt_codes.get('1.0', tk.END).strip()
    if text:
        copy_clipboard(text)
        messagebox.showinfo("成功", "コードがクリップボードにコピーされました。")


def exit_button_on_click():
    """
    「終了」ボタンがクリックされた際の処理
    アプリケーションを終了させるため、フラグを立ててGUIを破棄します。
    """

    global exit_flag
    exit_flag = True
    root.destroy()






# TKinter GUIの初期設定
root = tk.Tk()
root.title("コードリーダー")

clipboard.copy('')  # 起動時にクリップボードをクリア

# GUI要素の設定
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# 読み取ったコードの表示
txt_codes = tk.Text(root, height=10, width=80)
txt_codes.pack(pady=10)

frame_buttons = tk.Frame(root)
frame_buttons.pack(anchor='e')

# Snipping Toolを起動ボタン
btn_screen_shot = tk.Button(frame_buttons, text="Snipping Toolを起動", command=launch_screenshot_tool)
btn_screen_shot.pack(side='left', padx=5)

# テキストをクリップボードにコピーボタン
btn_copy = tk.Button(frame_buttons, text="テキストをクリップボードにコピー", command=copy_button_on_click)
btn_copy.pack(side='left', padx=5)

# コードリーダーを終了ボタン
btn_exit = tk.Button(frame_buttons, text="コードリーダーを終了", command=exit_button_on_click)
btn_exit.pack(side='left')

# 読み取り結果の一致判定ラベル（root生成後に配置）
lbl_match = tk.Label(root, text="", fg="red", font=("Arial", 14))
lbl_match.pack()

# スレッドと終了フラグの設定
exit_flag = False
thread = Thread(target=update_codes_display)
thread.start()

# メインループを開始
root.mainloop()
