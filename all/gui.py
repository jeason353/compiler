from semantic import analyse as semantic
from syntax import syntax_analysis as syntax
from lexical import lexical
import tkinter

def on_click():
    text_semantic.delete(1.0, 'end')  # 清空上次扫描结果
    text_1.delete(1.0, 'end')
    text_lex.delete(1.0, 'end')
    text_syntax.delete(1.0, 'end')

    token = lexical()
    codes, symbols = semantic()
    out = ''
    for key, value in symbols.items():
        out += key + ' : ' + str(value) + '\n'

    syn = syntax()

    text_semantic.insert(1.0, codes)
    text_lex.insert(1.0, token)
    text_syntax.insert(1.0, syn)
    text_1.insert(1.0, out)

if __name__=='__main__':
    root = tkinter.Tk()
    root.title('语义分析')

    fram = tkinter.Frame(root)

    tkinter.Button(fram, text='分析', command=on_click, font=("Arial", 12), width=7, height=1).pack(side=tkinter.TOP)
    fram.pack(side=tkinter.LEFT)

    fram3 = tkinter.Frame(root)
    tkinter.Label(fram3, text='token', font=("Arial", 12), width=7, height=2).pack(side=tkinter.TOP)
    scroll_3 = tkinter.Scrollbar(fram3)
    scroll_3.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    text_lex = tkinter.Text(fram3, font=("Arial", 10), width=30, height=20)
    scroll_3.config(command=text_lex.yview)
    text_lex.config(yscrollcommand=scroll_3.set)
    text_lex.pack(side=tkinter.LEFT)
    fram3.pack(side='left')

    fram4 = tkinter.Frame(root)
    tkinter.Label(fram4, text='归约顺序', font=("Arial", 12), width=7, height=2).pack(side=tkinter.TOP)
    scroll_4 = tkinter.Scrollbar(fram4)
    scroll_4.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    text_syntax = tkinter.Text(fram4, font=("Arial", 10), width=30, height=20)
    scroll_4.config(command=text_syntax.yview)
    text_syntax.config(yscrollcommand=scroll_4.set)
    text_syntax.pack(side=tkinter.LEFT)
    fram4.pack(side='left')


    fram1 = tkinter.Frame(root)
    tkinter.Label(fram1, text='四元式', font=("Arial", 12), width=7, height=2).pack(side=tkinter.TOP)
    scroll_1 = tkinter.Scrollbar(fram1)
    scroll_1.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    text_semantic = tkinter.Text(fram1, font=("Arial", 10), width=30, height=20)
    scroll_1.config(command=text_lex.yview)
    text_semantic.config(yscrollcommand=scroll_1.set)
    text_semantic.pack(side=tkinter.LEFT)
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

