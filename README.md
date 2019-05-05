# Stereopsis-correlation

### Depth map estimation using a correlation approach to stereopsis

A common approach to stereopsis accomplished using correlation metric to find the closest match in the other image.

Correlation is defined as the product of two normalized vectors divided by their norm.

### Prerequisites
---

* Python 3
* Rectified Stereo Images

### Dataset
---

Test set of Flickr1024, **[dataset](https://yingqianwang.github.io/Flickr1024/)**.

### Usage

Run the following command

```
python correlation.py
```

### Results
---
<img src="dataset/109_L.png" width="33%" /> <img src="dataset/109_R.png" width="33%" /> <img src="dataset/109_result.png" width="33%" /> 

<img src="dataset/104_L.png" width="33%" /> <img src="dataset/104_R.png" width="33%" /> <img src="dataset/104_result.png" width="33%" /> 

<img src="dataset/069_L.png" width="33%" /> <img src="dataset/069_R.png" width="33%" /> <img src="dataset/069_result.png" width="33%" /> 

<img src="dataset/024_L.png" width="33%" /> <img src="dataset/024_R.png" width="33%" /> <img src="dataset/024_result.png" width="33%" /> 
