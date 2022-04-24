# 热身：使用NumPy

在介绍 PyTorch 之前，我们将首先使用 NumPy 实现网络。

NumPy 提供了一个n维数组对象和许多用于操作这些数组的函数。
NumPy 是用于科学计算的通用框架；它对计算图、深度学习和梯度一无所知。
然而，我们可以很容易地使用 NumPy，手动实现网络的前向和反向传播，来拟合随机数据：

```python
# 可运行代码见本文件夹中的 two_layer_net_numpy.py
import numpy as np

# N 是批大小；D_in 是输入维度
# H 是隐藏层维度；D_out 是输出维度  
N, D_in, H, D_out = 64, 1000, 100, 10

# 产生随机输入和输出数据
x = np.random.randn(N, D_in)
y = np.random.randn(N, D_out)

# 随机初始化权重
w1 = np.random.randn(D_in, H)
w2 = np.random.randn(H, D_out)

learning_rate = 1e-6

for t in range(500):
    # 前向传播：计算预测值y
    h = x.dot(w1)
    h_relu = np.maximum(h, 0)
    y_pred = h_relu.dot(w2)

    # 计算并显示loss（损失）
    loss = np.square(y_pred - y).sum()
    print(t, loss)

    # 反向传播，计算w1、w2对loss的梯度
    grad_y_pred = 2.0 * (y_pred - y)
    grad_w2 = h_relu.T.dot(grad_y_pred)
    grad_h_relu = grad_y_pred.dot(w2.T)
    grad_h = grad_h_relu.copy()
    grad_h[h < 0] = 0
    grad_w1 = x.T.dot(grad_h)

    # 更新权重
    w1 -= learning_rate * grad_w1
    w2 -= learning_rate * grad_w2
```
