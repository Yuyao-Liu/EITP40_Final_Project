import csv

# 输入文件路径和输出文件路径
input_file = '9.csv'


# 打开输入文件，读取数据
with open(input_file, 'r', newline='') as infile:
    reader = csv.reader(infile)
    rows = list(reader)
    
    # 在第121行之前插入一行空白行
    rows.insert(1200, [])
    
    # 写入到输出文件
    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
