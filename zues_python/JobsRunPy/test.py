import h5py

# 打开并读取h5文件
with h5py.File('best_model.h5', 'r') as f:
    # 在文件中查找名为'dataset'的数据集
    # dset = f['dataset']
    # # 读取'dataset'数据集的数据
    # data = dset[:]
    for key in f.keys():
        # print(f[key].name)  # 获得名称，相当于字典中的key
        for key1 in f[key].keys():
            print("aaaaaaaa")
            print(f[key][key1].keys())
            print(type(f[key][key1]))
