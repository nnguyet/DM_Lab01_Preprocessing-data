import sys
import pandas as pd

file = 'house-prices.csv'       # Gán cứng để tiết kiệm thời gian test code, xóa sau khi hoàn thành
#file = sys.argv[1]      # Tham số dòng lệnh thứ 2 là tên file csv

df = pd.read_csv(file)      # Đọc dữ liệu file csv
title = list(df.columns)    # Lấy tên các thuộc tính
print(title)