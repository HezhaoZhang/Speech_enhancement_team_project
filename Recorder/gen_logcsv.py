import pandas as pd

# 读取第一个txt文件
df1 = pd.read_csv('../data/VoiceBank-DEMAND/log_trainset_56spk.txt', delimiter=' ', header=None)
# 读取第二个txt文件
df2 = pd.read_csv('../data/VoiceBank-DEMAND/log_testset.txt', delimiter=' ', header=None)

# 拼接两个数据框
df = pd.concat([df1, df2])

# 输出为csv文件
df.to_csv('log_corpus.csv', index=False)