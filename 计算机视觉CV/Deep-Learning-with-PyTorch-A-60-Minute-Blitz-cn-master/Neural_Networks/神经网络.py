#%% [markdown]
# # 神经网络
#%% [markdown]
# 可以使用`torch.nn`包来构建神经网络.
# 
# 我们以及介绍了`autograd`，`nn`包依赖于`autograd`包来定义模型并对它们求导。一个`nn.Module`包含各个层和一个`forward(input)`方法，该方法返回`output`。
# 
# 例如，下面这个神经网络可以对数字进行分类：
# 
# ![](assets/mnist.png)
# 
# 这是一个简单的前馈神经网络（feed-forward network）。它接受一个输入，然后将它送入下一层，一层接一层的传递，最后给出输出。
# 
# 一个神经网络的典型训练过程如下：
# 
# * 定义包含一些可学习参数（或者叫权重）的神经网络
# * 在输入数据集上迭代
# * 通过网络处理输入
# * 计算损失（输出和正确答案的距离）
# * 将梯度反向传播给网络的参数
# * 更新网络的权重，一般使用一个简单的规则：`weight = weight - learning_rate * gradient`
# 
# 
#%% [markdown]
# ## 定义网络
#%% [markdown]
# 让我们定义这样一个网络：

#%%
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


net = Net()
print(net)

#%% [markdown]
# 我们只需要定义 `forward` 函数，`backward`函数会在使用`autograd`时自动定义，`backward`函数用来计算导数。可以在 `forward` 函数中使用任何针对张量的操作和计算。
# 
# 一个模型的可学习参数可以通过`net.parameters()`返回

#%%
params = list(net.parameters())
print(len(params))
print(params[0].size())  # conv1's .weight

#%% [markdown]
# 让我们尝试一个随机的32x32的输入。注意，这个网络（LeNet）的期待输入是32x32。如果使用MNIST数据集来训练这个网络，要把图片大小重新调整到32x32。

#%%
input = torch.randn(1, 1, 32, 32)
out = net(input)
print(out)

#%% [markdown]
# 清零所有参数的梯度缓存，然后进行随机梯度的反向传播：

#%%
net.zero_grad()
out.backward(torch.randn(1, 10))

#%% [markdown]
# >注意：
# >
# >`torch.nn`只支持小批量处理（mini-batches）。整个`torch.nn`包只支持小批量样本的输入，不支持单个样本。
# >
# >比如，`nn.Conv2d` 接受一个4维的张量，即`nSamples x nChannels x Height x Width`
# >
# >如果是一个单独的样本，只需要使用`input.unsqueeze(0)`来添加一个“假的”批大小维度。
# 
#%% [markdown]
# 在继续之前，让我们回顾一下到目前为止看到的所有类。
# 
# **复习：**
# 
# * `torch.Tensor` - A multi-dimensional array with support for autograd operations like `backward()`. Also holds the gradient w.r.t. the tensor.
# 
# 
# * `nn.Module` - Neural network module. Convenient way of encapsulating parameters, with helpers for moving them to GPU, exporting, loading, etc.
# 
# 
# * `nn.Parameter` - A kind of Tensor, that is automatically registered as a parameter when assigned as an attribute to a `Module`.
# 
# 
# * `autograd.Function` - Implements forward and backward definitions of an autograd operation. Every `Tensor` operation, creates at least a single `Function` node, that connects to functions that created a `Tensor` and encodes its history.
# 
# 目前为止，我们讨论了：
# 
# * 定义一个神经网络
# * 处理输入调用`backward`
# 
# 还剩下：
# 
# * 计算损失
# * 更新网络权重
#%% [markdown]
# ## 损失函数
#%% [markdown]
# 一个损失函数接受一对(output, target)作为输入，计算一个值来估计网络的输出和目标值相差多少。
# 
# 译者注：output为网络的输出,target为实际值
# 
# nn包中有很多不同的[损失函数](https://pytorch.org/docs/stable/nn.html)。`nn.MSELoss`是比较简单的一种，它计算输出和目标的均方误差（mean-squared error）。
# 
# 例如：

#%%
output = net(input)
target = torch.randn(10)  # a dummy target, for example
target = target.view(1, -1)  # make it the same shape as output
criterion = nn.MSELoss()

loss = criterion(output, target)
print(loss)

#%% [markdown]
# 现在，如果使用`loss`的`.grad_fn`属性跟踪反向传播过程，会看到计算图如下：
#%% [markdown]
# ```
# input -> conv2d -> relu -> maxpool2d -> conv2d -> relu -> maxpool2d
#       -> view -> linear -> relu -> linear -> relu -> linear
#       -> MSELoss
#       -> loss
# ```
#%% [markdown]
# 所以，当我们调用`loss.backward()`，整张图开始关于loss微分，图中所有设置了`requires_grad=True`的张量的`.grad`属性累积着梯度张量。
# 
# 为了说明这一点，让我们向后跟踪几步：

#%%
print(loss.grad_fn)  # MSELoss
print(loss.grad_fn.next_functions[0][0])  # Linear
print(loss.grad_fn.next_functions[0][0].next_functions[0][0])  # ReLU

#%% [markdown]
# ## 反向传播
#%% [markdown]
# 我们只需要调用`loss.backward()`来反向传播权重。我们需要清零现有的梯度，否则梯度将会与已有的梯度累加。
# 
# 现在，我们将调用`loss.backward()`，并查看conv1层的偏置（bias）在反向传播前后的梯度。

#%%
net.zero_grad()     # zeroes the gradient buffers of all parameters

print('conv1.bias.grad before backward')
print(net.conv1.bias.grad)

loss.backward()

print('conv1.bias.grad after backward')
print(net.conv1.bias.grad)

#%% [markdown]
# 现在，我们已经见到了如何使用损失函数。
#%% [markdown]
# >稍后阅读
# >
# >神经网络包包含了各种模块和损失函数，这些模块和损失函数构成了深度神经网络的构建模块。完整的文档列表见[这里](https://pytorch.org/docs/stable/nn.html)。
# >
# >现在唯一要学习的是：
# >* 更新网络的权重
#%% [markdown]
# ## 更新权重
#%% [markdown]
# 最简单的更新规则是随机梯度下降法（SGD）:
# 
# `weight = weight - learning_rate * gradient`
# 
# 我们可以使用简单的python代码来实现:

#%%
learning_rate = 0.01
for f in net.parameters():
    f.data.sub_(f.grad.data * learning_rate)

#%% [markdown]
# 然而，在使用神经网络时，可能希望使用各种不同的更新规则，如SGD、Nesterov-SGD、Adam、RMSProp等。为此，我们构建了一个较小的包`torch.optim`，它实现了所有的这些方法。使用它很简单：

#%%
import torch.optim as optim

# create your optimizer
optimizer = optim.SGD(net.parameters(), lr=0.01)

# in your training loop:
optimizer.zero_grad()   # zero the gradient buffers
output = net(input)
loss = criterion(output, target)
loss.backward()
optimizer.step()    # Does the update

#%% [markdown]
# >注意：
# >观察梯度缓存区是如何使用`optimizer.zero_grad()`手动清零的。这是因为梯度是累加的，正如前面[反向传播章节](#反向传播)叙述的那样。

#%%



