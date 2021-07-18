#=============这份代码跟hmm无关.只是dtw的一个实验而已.
from scipy.io import wavfile
from python_speech_features import mfcc
import numpy as np

# 提取mfcc特征
def compute_mfcc(filename):
    fs, audio = wavfile.read(filename)
    mfcc_feat = mfcc(audio) #fs 是采样率frame sample, audio是音频array
    return mfcc_feat

#计算两个矩阵的最小的DTW和
def DTW(array1, array2):
    r = array1.shape[0]
    c = array2.shape[0]
    D0 = np.zeros((r + 1, c + 1))
    D0[0, 1:] = np.inf # D0 (i,j) 表示array1里面i位置和array2里面j位置2个13维度的向量的距离.
    D0[1:, 0] = np.inf # i,j 任意一个取0都不是我们要的索引,所以填上inf即可.
    D1 = D0[1:, 1:]#初始值不用管.下面也是动态规划重新算. D1(i,j) 的物理含义,是 数组1的i位置和数组2的j位置必须匹配上的情况下.之前其他位置可以一对多或者多对一的匹配时候的最短距离.
    #计算初始的距离矩阵
    for i in range(r):
        for j in range(c):
            D0[i+1, j+1] = np.sqrt(np.sum(np.square(array1[i][0:] - array2[j][0:])))
    #应用动态规划，寻找最短路径，由于不需要知道具体路径只关心最后的数值
    #我并没有对于过程路径进行存储
    for i in range(r):
        for j in range(c):
            a = np.sqrt(np.sum(np.square(array1[i][0:] - array2[j][0:])))
            #课件上的算法，斜对角系数为2，其余系数为1
            D1[i, j] += min(D0[i, j]+2*a, D0[i, j + 1]+a, D0[i + 1, j]+a) # 动态规划. D1[i,j] 表示 i,j如果对应序列的长度,那么他的最优匹配距离.
    return D1[r-1, c-1]

#用于计算10个模板语料的特征矩阵。开始的时候放在了calculate中，
#经检验calculate要应用于循环之种，此时10个模板语料特征矩阵的计算
#也就重复了多次，完全没有必要，所以把这一段单独提出。
def base_cal():
    base_feat = []
    for i in range(10):
        filepath = 'test_data/1_' + str(i + 1) + '.wav'
        base_feat.append(compute_mfcc(filepath))
    return base_feat

def calculate(filepath,num,base_feat):
    mfcc_feat = compute_mfcc(filepath)  # filepath是输入的训练语音的路径, num是输入语音的类型, baes_feat是测试的所有音频数据.
    min = np.inf # 下面我们用dtw来得到2个语音的距离, 2个语音距离越近表示他们越相似.
    seq = 100000
    # for i in range(10):
    #     filepaths = 'base_data/1_'+str(i+1)+'.wav'
    #     mfcc_base = compute_mfcc(filepaths)
    #     result = DTW(mfcc_base,mfcc_feat)
    #     if result < min:
    #         min = result
    #         seq = i+1
    for i in range(10): #一共有10句话需要测试.
        result = DTW(base_feat[i],mfcc_feat) #dtw 输入的是2个语音的numpy数据.
        if result < min:
            min = result
            seq = i+1
    print("测试语音类型："+str(num)+'，匹配语音类型'+str(seq)+"  ")

if __name__ == "__main__":
    print('序号1：打开电灯， 序号2：关闭电灯， 序号3：空调开启， 序号4：空调关闭， 序号5：升高温度')
    print('序号6：降低温度， 序号7：播放音乐， 序号8：停止播放， 序号9：提升音量， 序号10：降低音量')
    base_feat = base_cal()
    for i in range(5):
        for j in range(10):
            thestr = 'training_data/' + str(i + 1) + "_"+str(j+1)+'.wav'
            calculate(thestr,j+1,base_feat)