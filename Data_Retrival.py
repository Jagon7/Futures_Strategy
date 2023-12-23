import pandas as pd
import os

# 自行輸入要拼接檔案所在的資料夾完整路徑，不可包含中文
Folder_Path = r'/Users/jagon/Desktop/Finance Coding/Futures_Strategy/RawData'

#拚接後檔案保存的資料夾路徑
SaveFile_Path =  r'/Users/jagon/Desktop/Finance Coding/Futures_Strategy/Data'

#拚接後要保存的檔案名
SaveFile_Name = r'taiwanfuture_all_TX.csv'

#選取特定產品來組合資料，TX和後面的空格代表大台期貨產品
Column_Product_Select = 'TX     '

#修改目前工作目錄
os.chdir(Folder_Path)

#將該資料夾下的所有檔案名存入一個列表
file_list = os.listdir()
print(Folder_Path +'/'+ file_list[0])

#讀取第一個CSV檔案並包含表頭
#編碼預設UTF-8，為讀取中文更改為 GB18030
df = pd.read_csv(Folder_Path +'/'+ file_list[0],encoding="GB18030")
df.columns = ['Date', 'Product', 'DueMonth', 'Time', 'Price', 'Volume', 'NearMPrice', 'FarMPrice', 'OpenEx']

#選取台指期
df = df.loc[df['Product'] == Column_Product_Select]

#將讀取的第一個CSV檔案寫入合併後的檔案保存
df.to_csv(SaveFile_Path+'/'+ SaveFile_Name,encoding="GB18030",index=False)

#遞迴瀏覽列表中的各個CSV檔案名，並追加到合併後的檔案
for i in range(1,len(file_list)):
    df = pd.read_csv(Folder_Path + '/'+ file_list[i],encoding="GB18030")
    df.columns = ['Date', 'Product', 'DueMonth', 'Time', 'Price', 'Volume', 'NearMPrice', 'FarMPrice', 'OpenEx']
    df = df.loc[df['Product'] == Column_Product_Select]
    df.to_csv(SaveFile_Path+'/'+ SaveFile_Name,encoding="GB18030",index=False, header=False, mode='a+')

#轉換後保存的檔案名
NewFile_Name = r'taiwanfuture_all_TX_second.csv'
df = pd.read_csv(SaveFile_Path +'/'+ SaveFile_Name, encoding="GB18030")

#選取所關心的欄位
dh = df.loc[:, ['Date', 'DueMonth', 'Time', 'Price', 'Volume']]

#在Price, Volume後新增一個欄位叫PV，等於價乘上量，視為成交額，以進行價格平均
dh.eval('PV = Price * Volume', inplace = True)

#依序依照日期、到期月份、時間分組，把剩下的欄位值加總，再解除groupby層狀索引
dh = dh.groupby(['Date', 'DueMonth', 'Time']).sum().reset_index()

#重新根據PV/Volume平均出該秒鐘內的成交均價
dh['Price'] = dh.apply(lambda x: x['PV'] / x['Volume'], axis=1)

#因為原始檔案的成交量是 B+S，所以除以二(此行也可不除，如前後一致不影響分析)
dh['Volume'] = dh.apply(lambda x: x['Volume'] / 2, axis=1)

#除掉PV
dh = dh.loc[:, ['Date', 'Time', 'DueMonth', 'Price', 'Volume']]

#儲存整理後的數據到新的csv檔
dh.to_csv(SaveFile_Path+'/'+ NewFile_Name,encoding="GB18030",index=False)
