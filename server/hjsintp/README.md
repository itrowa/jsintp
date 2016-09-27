# HTML and Javascript Interpreter

render HTML and Javascript output in a img file. support basic HTML tags.


# 组成

分为3部分：

1. tokens定义

`htmltokens` 和 `htmltokens_test` 用于定义和测试HTML token的设计. 
`jstokens` 和 `jstokens_test` 用于定义和测试JavaScript token的设计.

2. cfg语法定义

`htmlgrammar` & `htmlgrammar_test` 用于定义和测试html语法. 
`jsgrammar` 和 `jsgrammar_test` 用于定义和测试JavaScript 语法的设计.


以上定义均使用lex库.

3. JavaScript的解释由jsintp完成。jsintp_test用于测试。js的解释结果作为字符串替换到HTML中。HTML不需要解释器，但需要一个渲染器将HTML
文本渲染为图像。