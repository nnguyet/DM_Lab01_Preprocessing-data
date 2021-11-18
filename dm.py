import sys, argparse
from numpy import exp, sqrt
import pandas as pd
import re

# Hàm thông báo sai cú pháp tham số dòng lệnh
def announce(parser, noti):
    print(noti)
    parser.print_help()

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

# Vì pandas đọc kiểu float là 1 string nên hàm này để chuyển định dạng str về float
def fix_if_float(arr):
    for i in range(len(arr)):
        if arr[i] == '':
            continue
        if type(arr[i]) == int:
            continue
        arr[i] = float(arr[i])

# Hàm tìm mode
def mode(attr):
    clean_attr = list(filter(lambda x: x!='', attr))        # Loại bỏ các giá trị rỗng trong thuộc tính
    return max(clean_attr, key = clean_attr.count)          # Trả về giá trị xuất hiện nhiều nhất

# Hàm tìm mean
def mean(attr):
    clean_attr = list(filter(lambda x: x!='', attr))        # Loại bỏ các giá trị rỗng trong thuộc tính
    return sum(clean_attr)/len(clean_attr)

# Hàm tìm median
def median(attr):
    clean_attr = list(filter(lambda x: x!='', attr))        # Loại bỏ các giá trị rỗng trong thuộc tính
    clean_attr.sort()                   # Sắp xếp các giá trị của thuộc tính theo thứ tự tăng dần
    n = len(clean_attr)                 # n là số lượng giá trị
    if n%2==1:
        return clean_attr[n//2]
    else:
        return (clean_attr[n//2]+clean_attr[n//2-1])/2

# Hàm tìm min
def min_attr(attr):
    clean_attr = list(filter(lambda x: x!='', attr))        # Loại bỏ các giá trị rỗng trong thuộc tính
    return min(clean_attr)

# Hàm tìm max
def max_attr(attr):
    clean_attr = list(filter(lambda x: x!='', attr))        # Loại bỏ các giá trị rỗng trong thuộc tính
    return max(clean_attr)

# Hàm tìm độ lệch chuẩn
def standard_deviation(attr):
    clean_attr = list(filter(lambda x: x!='', attr))        # Loại bỏ các giá trị rỗng trong thuộc tính
    n = len(clean_attr)
    aver = mean(clean_attr)
    s = 0
    for i in range(n):
        s += (clean_attr[i] - aver)/(n - 1)         # Tính phương sai
    return sqrt(s)

# 1. Liệt kê cột bị thiếu
def column_has_missing(titles, attrs):
    res = []
    for x in titles:
        if "" in attrs[x]:
            res.append(x)
    if (len(res)==0):
        print('Khong co cot nao bi thieu du lieu.')
    else:
        print(f'Co {len(res)} cot bi thieu du lieu:')
        for x in res:
            print(x)

# 2. Đếm số dòng bị thiếu dữ liệu
def row_has_missing(samples):
    res = 0
    for row in samples:
        if "" in row:
            res += 1
    print(f'Co {res} dong bi thieu du lieu.')

# 3. Điền giá trị bị thiếu
def fill_missing(method, attr):
    fix_if_float(attr)
    if method == 'mean':
        value = mean(attr)
    elif method == 'median':
        value = median(attr)
    elif method == 'mode':
        value = mode(attr)
    for i in range(len(attr)):
        if attr[i] == '':
            attr[i] = value
    return attr

# 4. Tìm các dòng thiếu dữ liệu với ngưỡng tỉ lệ ratio
def row_ratio_miss(limit, row):
    res = []        # Lưu index các dòng cần xóa
    for i in range(len(row)):
        cnt = 0
        for j in range(len(row[i])):
            if row[i][j] == '':
                cnt += 1
                if cnt >= limit:
                    res.append(i)
                    break
    return res

# 5. Tìm các cột thiếu dữ liệu với ngưỡng tỉ lệ ratio
def col_ratio_miss(limit, col):
    res = []        # Lưu tên các thuộc tính cần xóa
    for attr in col:
        cnt = 0
        for i in range(len(col[attr])):
            if col[attr][i] == '':
                cnt += 1
                if cnt >= limit:
                    res.append(attr)
                    break
    return res

# 6. Tìm index của các dòng bị trùng
def duplicate_rows(rows):
    res = []        # Lưu index các dòng bị trùng
    for i in range(len(rows)):
        if i in res:
            continue
        for j in range(i+1, len(rows)):
            if rows[i][0] == rows[j][0]:           # Yêu cầu cột đầu tiên phải là id (mã phân biệt giữa các dòng)
                res.append(j)
    return res

# 7. Chuẩn hóa thuộc tính
# Chuẩn hóa min-max
def min_max_normalize(attr, new_min, new_max):
    fix_if_float(attr)
    old_min = min_attr(attr)
    old_max = max_attr(attr)
    for i in range(len(attr)):
        if attr[i]!='':         # Dữ liệu bị mất thì không chuẩn hóa được
            attr[i] = (attr[i]-old_min)/(old_max-old_min)*(new_max-new_min) + new_min
    return attr

# Chuẩn hóa z-score
def zscore_normalize(attr):
    fix_if_float(attr)
    mu = mean(attr)
    sigma = standard_deviation(attr)
    for i in range(len(attr)):
        if attr[i]!='':
            attr[i] = (attr[i] - mu)/sigma
    return attr

# 8.tính thuộc tính mới    
def newAttr(df, prototype, newAttr):
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

def main(argv):
    file = 'house-prices.csv'       # Gán cứng để tiết kiệm thời gian test code, xóa sau khi hoàn thành

    # Phân tích cú pháp tham số dòng lệnh
    parser = argparse.ArgumentParser(epilog="* Read 'README.pdf' for more help.")
    parser.add_argument('file', help='csv file name')
    parser.add_argument('func_code', type=int, metavar='N', choices=[1, 2, 3, 4, 5, 6, 7, 8], help='number of function')
    parser.add_argument('-m', nargs='*', choices=['mean', 'median', 'mode', 'minmax', 'zscore'], default=argparse.SUPPRESS, help='method (need when use function 3 or 7)')
    parser.add_argument('-attr', nargs='*', default=argparse.SUPPRESS, help='attributes (need when use function 3 or 7)')
    parser.add_argument('-ratio', type=float, default=argparse.SUPPRESS, help='ratio (need when use function 4 or 5)')
    parser.add_argument('-exp', default=argparse.SUPPRESS, help='expression (need when use function 8)')
    parser.add_argument('-nc', default=argparse.SUPPRESS, help='new column name (need when use function 8)')
    parser.add_argument('-o', default=argparse.SUPPRESS, help='output file name (need when use function 3 -> 8)')

    args = vars(parser.parse_args(argv))

    #df = pd.read_csv(args['file'], keep_default_na=False)      # Đọc dữ liệu file csv
    df = pd.read_csv(file, keep_default_na=False)
    titles = list(df.columns)    # Lấy tên các thuộc tính

    # fill_missing(argv,df,titles)
    if args['func_code'] == 1:
        attrs = {x:df[x].values.tolist() for x in titles}     # Lấy danh sách dữ liệu của từng cột
        column_has_missing(titles, attrs)

    elif args['func_code'] == 2:
        samples = df.values.tolist()     # Lấy danh sách các dòng dữ liệu
        row_has_missing(samples)

    elif args['func_code'] == 3:
        if 'm' not in args or 'attr' not in args or 'o' not in args:
            announce(parser, 'Wrong syntax!')
            return
        if 'minmax' in args['m'] or 'zscore' in args['m']:
            announce(parser, 'Wrong method!')
            return

        attrs = {x:df[x].values.tolist() for x in titles}     # Lấy danh sách dữ liệu của từng cột
        
        if len(args['m']) == 1:         # Chỉ truyền 1 method cho tất cả attribute
            for attr in args['attr']:
                fill_col = fill_missing(args['m'][0], attrs[attr])
                df[attr] = fill_col

        elif len(args['m']) == len(args['attr']):       # Mỗi attribute có 1 method riêng
            for attr in args['attr']:
                fill_col = fill_missing(args['m'][args['attr'].index(attr)], attrs[attr])
                df[attr] = fill_col
        else:
            announce(parser, 'Miss arguments!')
            return
        df.to_csv(args['o'], index=False)

    elif args['func_code'] == 4:
        if 'ratio' not in args or 'o' not in args:
            announce(parser, 'Wrong syntax!')
            return
        samples = df.values.tolist()     # Lấy danh sách các dòng dữ liệu
        limit = args['ratio']/100 * len(titles)
        rows = row_ratio_miss(limit, samples)
        df = df.drop(rows)
        df.to_csv(args['o'], index=False)

    elif args['func_code'] == 5:
        if 'ratio' not in args or 'o' not in args:
            announce(parser, 'Wrong syntax!')
            return
        attrs = {x:df[x].values.tolist() for x in titles}     # Lấy danh sách dữ liệu của từng cột
        limit = args['ratio']/100 * len(df.index)
        cols = col_ratio_miss(limit, attrs)
        for attr in cols:
            df = df.drop(columns=attr)
        df.to_csv(args['o'], index=False)

    elif args['func_code'] == 6:
        if 'o' not in args:
            announce(parser, 'Wrong syntax!')
            return
        samples = df.values.tolist()     # Lấy danh sách các dòng dữ liệu
        rows = duplicate_rows(samples)
        df = df.drop(rows)
        df.to_csv(args['o'], index=False)

    elif args['func_code'] == 7:
        if 'm' not in args or 'attr' not in args or 'o' not in args:
            announce(parser, 'Wrong syntax!')
            return
        if 'mean' in args['m'] or 'median' in args['m'] or 'mode' in args['m']:
            announce(parser, 'Wrong method!')
            return

        attrs = {x:df[x].values.tolist() for x in titles}     # Lấy danh sách dữ liệu của từng cột
        if len(args['m']) == 1:
            if args['m'][0] == 'minmax':
                for attr in args['attr']:
                    df[attr] = min_max_normalize(attrs[attr], 0, 1)
            else:
                for attr in args['attr']:
                    df[attr] = zscore_normalize(attrs[attr])

        elif len(args['m']) == len(args['attr']):
            for attr in args['attr']:
                if args['m'][args['attr'].index(attr)] == 'minmax':
                    df[attr] = min_max_normalize(attrs[attr], 0, 1)
                else:
                    df[attr] = zscore_normalize(attrs[attr])
        else:
            announce(parser, 'Miss arguments!')
            return
        df.to_csv(args['o'])

    elif args['func_code'] == 8:
        """chức năng 8: <tên ct> <tên file csv> <mã chức năng> -exp <biểu thức viết liền không khoảng trắng> -nc <tên thuộc tính mới> -con[console] -o <tên file mới>
    note: tên thuộc tính phải chính xác (phân biệt chữ cái hoa - thường)
    vd1 in ra file mới: dm.py house-prices.csv 8 -exp 1stFlrSF+2ndFlrSF -nc newCol -o newfile.csv
    vd2 in ra console:  dm.py house-prices.csv 8 -exp 1stFlrSF+2ndFlrSF -nc newCol -con"""
        if 'exp' not in args or 'nc' not in args or 'o' not in args:
            announce(parser, 'Wrong syntax!')
            return
        newAttr(df, args['exp'], args['nc'])
        df.to_csv(args['o'], index=False)
        # if '-o' in sys.argv:
        #     df.to_csv(sys.argv[sys.argv.index('-o')+1])
        # elif '-con' in sys.argv:
        #     print(df.head())
    else:
        announce(parser, 'Wrong syntax!')

if __name__=="__main__":
    main(sys.argv[1:])
