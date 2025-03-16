# functions and pages design for the front end

【问题：有什么成熟的网站模板可以套用不？】

## 1.开始页面+产品类别页面：
当server被run的时候，我希望进入一个默认页面，前端应该显示“start building”，点击进入“/api/component-types/”得到所有组件类别
【需要在urls文件里增加这个开始页面的url】

## 2.获取某个类别下面的所有产品的页面：
用户点击某个大类，可以进入一个列出这个类别下所有产品的页面
【问题：如果产品特别多，如何分页？】

## 3.获取某个产品的详细规格的页面：
用户点击某个产品，可以进入一个列出这个产品的规格的页面

## 4.查看当前pclist的页面：
用户的页面应该始终有一个链接可以跳转当前的pclist
当前的pclist储存在session里面

## 5.添加产品到pclist
对于每个产品，用户点击“add to pclist”按钮，后端进行兼容性检查后决定是否加入pclist。
前端应展示后端返回信息。

## 6.移除产品出pclist
对于每个产品，用户点击“remove from pclist”按钮，pclist移除该产品。
前端应展示后端返回信息。

## 7.保存pclist 
在查看pclist的链接旁添加一条保存pclist的链接，用户点击该链接后，若已经pclist已经完整，则成功，否则失败。
前端应展示后端返回信息。





