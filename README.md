### 依赖  
如果是直接运行Python程序的话需要PIL, numpy。如果用pillow2.0以上的话就不需要`alpha_composite`方法了，进而也就不需要numpy，用`Image.alpha_composite`代替就好，之所以造了个`alpha_composite`的轮子是因为pillow 2.0以下或者原生PIL不提供此方法...  

## 使用说明  
`pic_raw`为源图片存放目录，里边必须要有`original.png`作为原始图片，其他元素图片随意（可以以子文件夹形式存放）。 

运行`fig_composite.py`或是相应打包好的exe文件(需与`pic_raw`同一目录)后即可在当前目录下看到处理好的`pic_composite`文件夹，里边的文件即是混合之后的图片。
