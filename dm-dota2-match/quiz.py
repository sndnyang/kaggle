# -*-coding: utf-8-*-

def check_steps(answer, steps):
    if not isinstance(answer, int):
        return '有几步，回答个整数，回答个 ' + type(answer) + ' 我可不认'
    return '''没有标准答案，参考: 
    1.打开网页，
    2.查找图片链接地址URL，
    3.下载保存'''

def check_openpages(name):
    if name.lower().startswith('urllib'):
        return True
    return False

def check_findlinks(name):
    if name.lower() == 're':
        return '没错，我也是这么想的'
    return '最好的应该是正则表达式的 re 吧？'


