# 二维卷积示例 

## 卷积
|                 步长 s = 1                 |                 步长 s = 2                 |
| :--------------------------------------: | :--------------------------------------: |
| <img width="250px" src="cnn-in_5_out_3_p_0_s_0.gif"> | <img width="250px" src="cnn-in_5_out_4_p_2_s_2.gif"> |
|           m = 3, p = 0 ,s = 1            |           m = 3, p = 2 ,s = 2            |
| <img width="250px" src="cnn-in_3_out_5.gif"> | <img width="250px" src="cnn-in_9_out_5.gif"> |
|           m = 3, p = 2 ,s = 1            |            m=5, p = 2 ,s = 2             |

 m表示卷积核大小，p 表示零填充大小（zero-padding）， s 表示步长（stride）。



图片修改自： Vincent Dumoulin, Francesco Visin - [A guide to convolution arithmetic
for deep learning](https://arxiv.org/abs/1603.07285)