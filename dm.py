import sys
from numpy import exp
import pandas as pd
import re
# xét độ ưu tiên của các toán hạng
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0
# tính giá trị biểu thức giữa 2 số
def Cal(val1,val2,op):
    if op=='+': return val1+val2
    if op=='-': return val1-val2
    if op=='*': return val1*val2
    if op=='/': return val1/val2
# tính giá trị biểu thức truyền vào ở dạng chuỗi 
# (nếu có phép tính không hợp lệ (chia cho 0) thì giá trị trả về là NaN)
def evaluate(expression):
    operands=[]
    operators=[]
    i=0
    while i<len(expression):
        if expression[i]=='(':
            operators.append(expression[i])
        elif expression[i].isdigit():
            val=0
            while i<len(expression) and expression[i].isdigit():
                val=val*10+int(expression[i])
                i+=1
            operands.append(val)
            i-=1
        elif expression[i]==')':
            while len(operators)!=0 and operators[-1]!='(':
                val2=operands.pop()
                val1=operands.pop()
                op=operators.pop()
                if val2==0 and op=='/': return 'NaN'
                operands.append(Cal(val1,val2,op))
            operators.pop()
        else:
            while len(operators)!=0 and precedence(operators[-1])>=precedence(expression[i]):
                val2=operands.pop()
                val1=operands.pop()
                op=operators.pop()
                if val2==0 and op=='/': return 'NaN'
                operands.append(Cal(val1,val2,op))
            operators.append(expression[i])
        i+=1

    while len(operators)!=0:
        val2=operands.pop()
        val1=operands.pop()
        op=operators.pop()
        if val2==0 and op=='/': return 'NaN'
        operands.append(Cal(val1,val2,op))
    return operands[-1]

#tính thuộc tính mới    
def newAttr(df,prototype,newAttr):
    title=list(df.columns) # danh sách thuộc tính cũ
    prototypeAttr=re.split('\+|-|\*|/',prototype.strip()) # lấy các thuộc tính được đề cập trong biểu thức
    newCol=[] # mảng lưu giá trị thuộc tính mới
    for i in range(len(df[title[0]])):
        flag=True
        toCal=prototype
        for p in prototypeAttr: # duyệt các thuộc tính trong biểu thức
            if df[p][i]=='': # nếu tại dòng i thuộc tính bị thiếu giá thì dừng vòng lặp
                flag=False
                break
            toCal=toCal.replace(p,str(df[p][i])) 
            """nếu tại dòng i không có thuộc tính thiếu giá trị thì thay lần lượt các tên
            thuộc tính thành giá trị của thuộc tính đó tại i"""
        newCol.append(evaluate(toCal)) if flag else newCol.append('') # tính giá trị nếu có và thêm vào dòng i của thuộc tính mới
    df[newAttr]=newCol # thêm thuộc tính mới vào dataframe
    return df
    
def main():
    # file = 'house-prices.csv'       # Gán cứng để tiết kiệm thời gian test code, xóa sau khi hoàn thành
    file = sys.argv[1]      # Tham số dòng lệnh thứ 2 là tên file csv
    df = pd.read_csv(file)      # Đọc dữ liệu file csv
    title = list(df.columns)    # Lấy tên các thuộc tính

    """chức năng 8: <tên ct> <tên file csv> <mã chức năng> -exp <biểu thức viết liền không khoảng trắng> -nc <tên thuộc tính mới> -con[console] -o <tên file mới>
    note: tên thuộc tính phải chính xác (phân biệt chữ cái hoa - thường)
    vd1 in ra file mới: dm.py house-prices.csv 8 -exp 1stFlrSF+2ndFlrSF -nc newCol -o newfile.csv
    vd2 in ra console:  dm.py house-prices.csv 8 -exp 1stFlrSF+2ndFlrSF -nc newCol -con"""
    if sys.argv[2]=='8':
        newAttr(df,sys.argv[sys.argv.index('-exp')+1],sys.argv[sys.argv.index('-nc')+1])
        if '-o' in sys.argv:
            df.to_csv(sys.argv[sys.argv.index('-o')+1])
        elif '-con' in sys.argv:
            print(df.head())

if __name__=="__main__":
    main()