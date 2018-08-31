#### 取自链接：[http://www.goubanjia.com](http://www.goubanjia.com/)
#### 时间：2018-08-31 19:57
## 如何使用
```
from pxy import get_proxy
proxy = get_proxy()
```
## 总结
- 该网页看起来挺容易爬取但实际上有反爬的技术手动复制简单而爬取变得困难
- 我们可以用BeatifulSoup去找到所有含有ip信息的位置的代码
```
<td class="ip">
<div style="display:inline-block;">18</div>
<div style="display:inline-block;"></div>
<span style="display:inline-block;">2.</span>
<span style="display:inline-block;">1</span>
<span style="display:inline-block;">6</span>
<div style="display:inline-block;"></div>
<div style="display:inline-block;">5.</div>
<div style="display:inline-block;"></div>
<p style="display: none;"></p>
<span></span>
<span style="display:inline-block;">17</span>
<span style="display:inline-block;">5</span>
<p style="display: none;">.4</p>
<span>.4</span>
span style="display:inline-block;">6</span>
:
<span class="port GEA">8105</span>
</td>
```
- 然后将所有的标签属性style为display: none的去掉再将所有的text()混合即可
- 难点在于这里的标签有div、span和p三者混合且会出现冗余的数据而这些情况出现的位置是随机的
