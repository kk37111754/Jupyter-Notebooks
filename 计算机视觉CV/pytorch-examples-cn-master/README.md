# 用例子学习PyTorch

> [Learning PyTorch with Examples](https://pytorch.org/tutorials/beginner/pytorch_with_examples.html) 中文翻译版，翻译不对的地方拜托大家指出~

>**对PyTorch感兴趣的童鞋欢迎看这个**-->[PyTorch教程、例子和书籍合集](https://github.com/bat67/pytorch-tutorials-examples-and-books)

[TOC]

## 1、简介
这个repo通过自洽的示例介绍了PyTorch的基本概念。

PyTorch主要是提供了两个核心的功能特性：

* 一个类似于numpy的n维张量，但是可以在GPU上运行
* 搭建和训练神经网络时的自动微分/求导机制

我们将使用全连接的ReLU网络作为运行示例。该网络将有一个单一的隐藏层，并将使用梯度下降训练，通过最小化网络输出和真正结果的欧几里得距离，来拟合随机生成的数据。

## 2、环境

* PyTorch版本0.4及以上（PyTorch 1.0 **稳定版**已经发布，还有什么理由不更新呢~）

## 3、目录

### 3.1、张量(Tensors)

* [热身：使用NumPy](./热身%EF%BC%9A使用NumPy)
* [PyTorch：张量(Tensors)](./PyTorch%EF%BC%9A张量(Tensors))

### 3.2、自动求导(Autograd)

* [PyTorch：自动求导(Autograd)](./PyTorch%EF%BC%9A自动求导(Autograd))
* [PyTorch：定义自己的自动求导函数](./PyTorch%EF%BC%9A定义自己的自动求导函数)
* [TensorFlow：静态图](./TensorFlow%EF%BC%9A静态图)

### 3.3、`nn`模块(`nn` module)

* [PyTorch：神经网络模块nn](./PyTorch%EF%BC%9A定制神经网络nn模块)
* [PyTorch：优化模块optim](./PyTorch%EF%BC%9A优化模块optim)
* [PyTorch：定制神经网络nn模块](./PyTorch%EF%BC%9A定制神经网络nn模块)
* [PyTorch：控制流和参数共享](./PyTorch%EF%BC%9A控制流和参数共享)


## 4、类似项目

* [PyTorch 教程、例子和书籍](https://github.com/bat67/pytorch-tutorials-examples-and-books)
* [PyTorch 深度学习：60分钟入门与实战](https://github.com/bat67/Deep-Learning-with-PyTorch-A-60-Minute-Blitz-cn)
* [用例子学习 PyTorch](https://github.com/bat67/pytorch-examples-cn)


## 5、版权信息

除非额外说明，本仓库的所有公开文档均遵循[署名-非商业性使用-相同方式共享 4.0 国际 (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)许可协议。

您可以自由地：

* 共享 — 在任何媒介以任何形式复制、发行本作品
* 演绎 — 修改、转换或以本作品为基础进行创作

惟须遵守下列条件：

* 署名 — 您必须给出适当的署名，提供指向本许可协议的链接，同时标明是否（对原始作品）作了修改。您可以用任何合理的方式来署名，但是不得以任何方式暗示许可人为您或您的使用背书。
* 非商业性使用 — 您不得将本作品用于商业目的。
* 相同方式共享 — 如果您再混合、转换或者基于本作品进行创作，您必须基于与原先许可协议相同的许可协议 分发您贡献的作品。