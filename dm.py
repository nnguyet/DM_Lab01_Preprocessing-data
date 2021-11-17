import sys
import pandas as pd

# 1. Liệt kê cột bị thiếu
def column_has_missing(title, attr):
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

def main():
    file = 'house-prices.csv'       # Gán cứng để tiết kiệm thời gian test code, xóa sau khi hoàn thành
    #file = sys.argv[1]      # Tham số dòng lệnh thứ 2 là tên file csv

    df = pd.read_csv(file, keep_default_na=False)      # Đọc dữ liệu file csv
    title = list(df.columns)    # Lấy tên các thuộc tính
    sample = df.values.tolist()     # Lấy danh sách các dòng dữ liệu
    attr = {x:df[x].values.tolist() for x in title}     # Lấy danh sách dữ liệu của từng cột

    #print(attr['Alley'][0])

    # Test chức năng 1
    #column_has_missing(title, attr)


if __name__=="__main__":
    main()
