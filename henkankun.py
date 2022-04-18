## HenKanKun.exe Version beta for windows/python
## Copyright - November 2021 - by T.Kanatake JE6VGZ
## modifications by N4FWD, Thomas Kocourek
import tkinter as tk

## changed the 'MSG' to 'MESG' because 'MSG' in JS8call has a special meaning, N4FWD

## txt2 is an Text widget passed to these functions
## NOTE: txt_1 is not needed. Altered txt_1 to txt_2 in functions below. N4FWD
## Adding 'DECODE MESG:' will not be needed. Decoded message will show in the Text Area. N4FWD

#def btn_click():
def decodeUTF8(params):
    txt_2 = params
    ## Text widgets return a string with the 'get()'
    etext = txt_2.get('1.0',tk.END)
    txt_2.delete('1.0', tk.END)    #Erase the text in the output window txt_2.
    #etext = str(txt_1.get())        # Get the encoded sentence starting with "/" from the variable "txt_1" and store it in the variable "etext".
    x = etext.count('/') #From the "etext" variable, count the number of "/" characters in the encoded text, i.e., the number of characters in the plain text.
    y = 1 #Start encoding from the left end of the sentence. 0 is for blanks.
    for i in range(x): #Repeat the indented section as many times as there are variable”x” to the right end of the sentence.
        b = etext.split('/')  #Split the string of the variable "etext" with "/".
        c = b[y].replace('/', '') # Remove the delimiter "/" from the string of variable "b".
        d =  bytes.fromhex(c).decode("utf-8") # Consider the variable "c" as a byte character, change the hexadecimal number back to UTF-8, and decode it from the UTF-8 number to a plain text character.
        txt_2.insert(tk.END,d)# Set the string of variable "d" to the right end of the output window "txt_2".
        y = y+1 #Shift the string to be encoded by one character to the right.
        #Repeat so far.
    #txt_2.insert('1.0', "DECODE MESG : ")   # Set the fixed statement "DECODE MSG :" to the left end of the output window txt_2.    
    #Click event ends here.

    #def btn_click():
def encodeUTF8(params):
    txt_2 = params
    ## Text widgets return a string with the 'get()'
    plaintext = txt_2.get('1.0',tk.END)
    #Erase the text in the output window txt_2.
    txt_2.delete('1.0', tk.END)
    #Get the plaintext from the input window txt_1 and store it in the variable plaintext.
    #plaintext = str(txt_1.get()) #Read the plaintext from the input window "txt_1" and set it as a string in the variable "plaintext".
    x =len(plaintext) #Count the number of characters in plain text.
    y = 0 #Start encoding from the left end of the sentence, i.e., the first character.
    
    for i in range(x): #Repeat the indentation part "x" times. That is, repeat as many times as the number of characters.
        b = plaintext[y].encode('utf-8') #denotes the UTF-8 number of the y-th character, where y is the UTF-8 number of the 1,2,3...th character as it increases with each process.
        c = b.hex() #Replace the UTF-8 number in variable "c" with a hexadecimal number and enter it in variable "d".
        d = '/' + c #Read the variable "c", precede it with "/", and enter it in the variable "d"." The "/" is responsible for separating characters from characters.
        e = d.upper() # Get the string from the variable d, convert lowercase to uppercase, and store it in variable "e". 
        txt_2.insert(tk.END,e)# Set the string of variable "e" to the output window "txt_2".
        y = y+1 #Shift the character to be encoded one character to the right.
        #Repeat up to here.
    # When the repetition is over, set the fixed statement to txt_2.
    txt_2.insert('1.0', "ENC IN UTF-8 MESG: ")
    # End of button click event.

    #def btn_click():
def encodeShiftJIS(params):
    txt_2 = params
    # txt_1から平文を取得し、変数numに格納する。
    ## Text widgets return a string with the 'get()'
    plaintext = txt_2.get('1.0',tk.END)
    #出力窓txt_2のテキストを消去する。
    txt_2.delete('1.0', tk.END)
    # txt_1から平文を取得し、変数numに格納する。
    #plaintext = str(txt_1.get())    
    x =len(plaintext) #文字数をカウントする。
    y = 0 #文左端からエンコードを始める。
    
    for i in range(x): #インデント部を文の右端まで1文字ずつエンコード/デコードする。
        b = plaintext[y].encode('shift-jis') #y番目の文字のUTF-8の番号を示す。
        c = b.hex() #cを16進数に置き換える。
        d = '/' + c #文字と文字の区切り/を置く。
        e = d.upper() # 変数eから文字列を取得し、小文字を大文字に変換し、fに格納する。 
        txt_2.insert(tk.END,e)# 変数eの文字列をtxt_2にセットする。
        y = y+1 #エンコードする文字を1文字右にずらす。
        #ここまで繰り返し。
    # 固定文ををtxt_2にセットする。
    ## changed the 'MSG' to 'MESG' because 'MSG' in JS8call has a special meaning, N4FWD
    txt_2.insert('1.0', "ENC IN S-JIS MESG: ")
    #クリックイベントココまで。

    #def btn_click():
def decodeShiftJIS(params):
    txt_2 = params
    ## Text widgets return a string with the 'get()'
    etext = txt_2.get('1.0',tk.END)        # txt_1から（/から始まる）エンコード文を取得し、変数etextに格納する。
    txt_2.delete('1.0', tk.END)    #出力窓txt_2のテキストを消去する。これをしないと前の奴が残る。
    #etext = str(txt_1.get())        # txt_1から（/から始まる）エンコード文を取得し、変数etextに格納する。
    x = etext.count('/') #エンコード文の"/"数＝平文の文字数をカウントする。
    y = 1 #文の左端からエンコードを始める。0はブランク分
    for i in range(x): #インデント部を文の右端まで1区切りずつデコードする。それをx回繰り返す。
        b = etext.split('/')  #変数aの文字列を/で分割する。
        c = b[y].replace('/', '') #文字と文字の区切りの"/"を除去する。
        d =  bytes.fromhex(c).decode("shift-jis", "replace") #cをバイト文字と見なし、16進数をUTF-8に戻し、UTF-8の番号から文字に戻す。
        txt_2.insert(tk.END,d)# 変数dの文字列をtxt_2の右端にセットする。
        y = y+1 #エンコードする文字を右に1文字ずらす。
        #繰り返しはここまで。
    #txt_2.insert('1.0', "DECODE MESG : ")   # 固定文ををtxt_2にセットする。
    #ボタンクリック時の動作はここまで。