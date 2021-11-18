import sys, argparse
import pandas as pd

# Hàm thông báo sai cú pháp tham số dòng lệnh
def announce():
    print('Wrong syntax!')
    print("Read 'README.pdf' for more help.")

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

# 1. Liệt kê cột bị thiếu
def column_has_missing(titles, attrs):
    res = []
    for x in title:
        if "" in attr[x]:
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
def fill_missing(method, attr, df, titles):
    attrs = {x:df[x].values.tolist() for x in titles}     # Lấy danh sách dữ liệu của từng cột
    samples = df.values.tolist()     # Lấy danh sách các dòng dữ liệu
    print(argv)

    #print(argv)
    #print(opts)
    """for opt, arg in opts:
        print(opt)
        print(arg)"""

def main(argv):
    file = 'house-prices.csv'       # Gán cứng để tiết kiệm thời gian test code, xóa sau khi hoàn thành

    # Phân tích cú pháp tham số dòng lệnh
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='csv file name')
    parser.add_argument('func_code', type=int, metavar='N', choices=[1, 2, 3, 4, 5, 6, 7, 8], help='number of function')
    parser.add_argument('-m', nargs='*', default=argparse.SUPPRESS, help='method (need when use function 3 or 7)')
    parser.add_argument('-attr', nargs='*', default=argparse.SUPPRESS, help='attributes (need when use function 3 or 7)')
    parser.add_argument('-ratio', default=argparse.SUPPRESS, help='ratio (need when use function 4 or 5)')
    parser.add_argument('-exp', default=argparse.SUPPRESS, help='expression (need when use function 8)')
    parser.add_argument('-nc', default=argparse.SUPPRESS, help='new column name (need when use function 8)')
    parser.add_argument('-o', default=argparse.SUPPRESS, help='output file name (need when use function 3 -> 8')

    args = vars(parser.parse_args(argv))

    #file = sys.argv[0]      # Lấy tên file csv
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
        print('func3')
    else:
        parser.print_help()
        announce()
        #parse_func_3(agrv[2:], df)

"""    elif args['func_code'] == 4:

    elif args['func_code'] == 5:

    elif args['func_code'] == 6:

    elif args['func_code'] == 7:

    elif args['func_code'] == 8:"""
    

if __name__=="__main__":
    main(sys.argv[1:])
