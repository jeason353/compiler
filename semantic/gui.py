from semantic import analyse
import tkinter

def on_click():
    text.delete(1.0, 'end')  # 清空上次扫描结果
    text_1.delete(1.0, 'end')
    output = ''
    output_1 = ''

    codes, symbols = analyse()
    out = ''
    for key, value in symbols.items():
        out += key + ' : ' + str(value) + '\n'


    text.insert(1.0, codes)
    text_1.insert(1.0, out)

if __name__=='__main__':
    root = tkinter.Tk()
    root.title('语义分析')

    fram = tkinter.Frame(root)
    # tkinter.Label(fram, text='输入文件', font=("Arial", 12), width=7, height=2).pack(side=tkinter.TOP)
    # filepath = tkinter.StringVar()
    # file = tkinter.Entry(fram, textvariable=filepath, bd=3)
    # filepath.set('')
    # file.pack(side=tkinter.TOP)
    tkinter.Button(fram, text='语义分析', command=on_click, font=("Arial", 12), width=7, height=1).pack(side=tkinter.TOP)
    fram.pack(side=tkinter.LEFT)

    fram1 = tkinter.Frame(root)
    tkinter.Label(fram1, text='四元式', font=("Arial", 12), width=7, height=2).pack(side=tkinter.TOP)
    scroll = tkinter.Scrollbar(fram1)
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    text = tkinter.Text(fram1, font=("Arial", 10), width=30, height=20)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    text.pack(side=tkinter.LEFT)
    fram1.pack(side='left')

    fram2 = tkinter.Frame(root)
    tkinter.Label(fram2, text='符号表', font=("Arial", 12), width=7, height=2).pack(side=tkinter.TOP)
    scroll_1 = tkinter.Scrollbar(fram2)
    scroll_1.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    text_1 = tkinter.Text(fram2, font=("Arial", 10), width=20, height=20)
    scroll_1.config(command=text_1.yview)
    text_1.config(yscrollcommand=scroll_1.set)
    text_1.pack(side=tkinter.LEFT)
    fram2.pack(side='left')


    root.mainloop()

