# 从头开始写一个浏览器(1) HTML parser

对于一段html文本而言:

    sample html text.
    <a href="#" class="wrapper"> link_text. </a>
    this is a <b>strong</b> text.

 

我们假设有一个简单的浏览器, 它的渲染器可以这样的方式往画布上输出这些文本:

如果看到的是字符, 例如 `sample html text.`,它会直接在画布上打印出这些字来; 如果看到的是标签, 浏览器会首先解读标签的类型和标签的属性, 例如, `<a href="#" class="wrapper"> link_text. </a> ` 是个`a`类型的标签, 有两个属性: `href="#"` 以及`class="wrapper"`, 包含在标签内的内容是 `link_text.`.这样, 浏览器根据标签的类型, 如果遇到`a`类型, 渲染器就先切换为"输出可点击的文本"模式, 将这个标签内的内容输出到画布上, 成为可被点击的对象.

让渲染器直接从HTML文本中判断哪些部分是直接打印的, 哪些是需要转换为另一种模式绘制的, 是非常困难的. 因此我们给渲染器传入更加容易识别的程序对象, 这样渲染器才能更方便地识别这些东西. 例如, 我们希望进行如下设计, 对于HTML文本而言,

    sample html text

在送给渲染器前会被处理成`("word-element", "sample html text")`;

    <a href="#" class="wrapper"> link_text. </a>

会被处理成`("tag-element", "a", {"href"="#", class="wrapper"}, "link_text")`.

这样, 传给渲染器的都是一些python中的tuple, 渲染器只要读取tuple的第一个元素就能知道此对象是`"word-element"`还是`"tag-element"`了. 然后渲染器根据不同的元素, 切换不同的显示模式, 绘制文本于画布上. 我们则可以用这样的伪代码来实现渲染器:

    def render(element):
        if element[0] == "word-element":
            draw word content
        elif element[0] == "tag-element":
            if element[1] == "a":
                switch to "a" mode
                draw word content
                switch to normal mode
            elif element[1] == "b":
                switch to bold mode
                draw word content
                switch to normal mode
            ...
        else:
            ...

总之, 对一段HTML文本而言:

    this is a <b>strong</b> text.

我们先需要一个程序, 将其处理为一系列对象的列表再送入渲染器:


    [("word-element", "this is a"), ("tag-element", "b", {}, "strong"), ("word-element", "text.")]



这个预处理程序就是parser, 而后面的渲染器就是解释器.  

# parser

## 句法分析

我们将考虑如何将HTML文本转换为上文所述的对象列表.

不是所有的HTML文本都能转换, 有一些明显是不合法的文本, 我们应该过滤掉它. 最好的办法是, 用一系列的语法规则来描述HTML的语法是什么样子的. 然后让parser根据此语法, 扫描输入的HTML文本是否符合该语法, 如果不是则停止解析; 如果是, 则生成对象列表.

我们要用上下文无关语法来表示HTML的语法规则. 一个上下文无关语法包含若干条规则, 每条规则由左手边(LHS)和右手边(RHS)组成; 左手边和右手边都是一些符号(symbol), 符号和符号之间用空格隔开. 左手边的符号可以被改写为右手边. 例如, 以下的语法可以表示所有支持加法, 乘法和括号的四则运算式子. 它包含4条规则:

    exp -> exp + exp
    exp -> exp * exp
    exp -> ( exp )
    exp -> NUM

从第2条规则出发: `exp` 被改写成 `exp + exp`.

然后, 第一个`exp`应用第3条规则, 第二个`exp`运用第2条规则, 得到`(exp)*exp`

然后 第一个`exp`运用规则1, 第二个`exp`运用规则4, 改写为`NUM`, `NUM`其实是代表阿拉伯数字, 可取3. 得到 `(exp) * 3`.

然后对exp继续用规则1进行重写.. 可以用一颗树画出整个重写过程:

                          exp
                           |
                 ---------------------------
                 |             |            |
                 exp           *          exp
                 |                          |
          ---------------                  NUM
        (     exp        )                  3
               |
           -------------
           |           |
           exp   +    exp
           |           |
           NUM        NUM
           20          4

这就生成了一个式子`(20+4)*3`.  这里已显示出这套语法规则的惊人威力: 寥寥几条规则, 通过选取不同的rule进行重写, 就能生成相当复杂的语句. 这就是语法和语言的关系: 语法规则是有限的, 但生成的语言却是无限的.

注意到语法规则中, 有一个大写单词`NUM`, 以及`+`, `*`, `)`, 它们不能再被继续重写了. 因此叫终结符号(terminal symbol). 另外一些是非终结符号(non-terminal), 非终结符号总是可以被进一步重写.  

上面讲的是从语法生成语言, parser做的事情刚好和生成相反, 它是判断语言是否符合语法. 例如, 对于输入的文本`(20+4)*3`而言, parser的作用就是从 `(NUM + NUM) * NUM` 反着应用语法中的规则, 直到它能划归为`exp`, 而且生成那颗树, 这个过程叫做句法分析(syntactic analysis).. parse过程看起来很很简单, 但是需要很复杂的算法去解决它. 其中一种算法应用了动态规划的思想 叫做earley parser.


    初始符号: html

    1. html -> element html
    2. html -> ∈


    3. element -> WORD
    4. element -> =
    5. element -> STRING
    7. element -> < tagname tag_arguments />
    8. element -> < tagname tag_arguments > html </ tagnameend >

    9. tag_arguments -> tag_argument tag_arguments
    10. tag_arguments -> ∈

    11. tag_argument -> WORD = WORD
    12. tag_argument -> WORD = STRING

    13. tagname -> WORD
    14. tagnameend -> WORD

这14条规则基本描述了HTML的语法. 所有大写的单词, 都是终结符号, `WORD`表示任何除了空格和`<` `>`以外的字符; 例如`thi% is te$t`中有3个`WORD`; `STRING`表示任何被双引号括起来的字符, 例如`"wrapper"`; `∈` 表示空字符.

现在可以人肉parse一下, 例如对于文本

    this is a <b class="em">strong</b> text.

而言, 用那套语法的规范, 可以表示为:

    WORD WORD WORD < WORD WORD = STRING > WORD </ tagnameend >

反向应用规则, 规约:

    element element element < tagname tag_artuments > html </ tagnameend >

再次规约:

    element element element element

    element element element element html

    element html

最后得到

    html

因此parse通过. parse tree就不画出来了.

前面讲过, 除了判断文本是否符合语法, 并给出parse tree以外, parser还有一个很重要的功能, 就是往解释器中传递处理好的对象! 事实上, 这个功能也是在生成parse tree的时候同时完成的. 还是那段文本:

    this is a <b class="em">strong</b> text.

生成好的对象是:

    [('word-element', 'this'), ('word-element', 'is'), ('word-element', 'a'),
     ('tag-element', 'b', {'class': 'em'}, [('word-element', 'strong')], 'b'),
     ('word-element', 'text.')]

可以画成一个树形的结构:
                             root
       ----------------------------------------------------------------
    word-ele           word-ele       word-ele      tag-ele        word-ele
       |                   |             |             |               |
       this              is            a          -------------       text
                                                |    |         |
                                              b     class:em   word-ele
                                                               |
                                                               strong

这和parse tree还有相当大的区别. parse tree中包含着许多条规则, 我们可以这样设计: 当满足规则的时候, 就让
程序生成一个tuple.

例如, , `element -> WORD`这条规则时, 就生成一个tuple: `("word-element", WORD)`;
当满足`element -> < tagname tag_arguments > html </ tagnameend >` 这个规则时, 就生成这样的tuple:
`('tag-element', tagname, {WORD: WORD}, html, tagnameend)`.

## 词法分析

在parser的最后, 还有一个重要的技术问题. 我们曾在语法规则中用`NUM`表示任意的数字, 而且它是一个终结符号. `NUM`可以是`1`, `-998`
, `2912.1212`等. parser是怎么知道那些数字都是`NUM`? 答案就是正则表达式. 给定一个正则表达式, 它能表示一个字符串集合. 例如python中的正则表达式

    NUM = r'-?[0-9]+(\.[0-9]*)?'

能匹配输入中所有的数字, 例如`13`, `-13`, `13.` `13.000001`. `WORD`和`STRING`也都是用正则表达式指定的. 实际上, 语法中所有的终结符都是用正则表达式指定的, 例如`</` 的正则表达式是`r'</'`, 取名为`LANGLESLASH`, 等等. 这样在考虑语法规则的时候, 所有的数字都可以用`NUM`表示了.

在用扫描文本生成parse tree之前, parser还要做一项重要的工作, 那就是把所有的非终结符找出来. 这个过程叫做词法分析(lexical analysis), 词法分析的程序也叫做词法分析器(Tokenizer). 结束后, 文本会变成一串由token组成的序列, 这才是句法分析的起点.

对`this is a <b class="em">strong</b> text.`的词法分析结果如下:

    (WORD,'this')
    (WORD,'is')
    (WORD,'a')
    (LANGLE,'<')
    (WORD,'b')
    (WORD,'class')
    (EQUAL,'=')
    (STRING,'em')
    (RANGLE,'>')
    (WORD,'strong')
    (LANGLESLASH,'</')
    (WORD,'b')
    (RANGLE,'>')
    (WORD,'text.')

其实就是`WORD WORD WORD LANGLE WORD WORD EQUAL STRING RANGLE WORD LANGLESLASH WORD RANGLE WORD`.

# 总结

总结起来, parser的功能如下:

对于输入的文本, 第一步是词法分析, 得到tokens的序列, 第二步是句法分析, 从tokens的序列出发, 根据语法规则反向进行规约, 直到得到语法规则的起始符号. parse成功后, 根据parse tree生成要给解释器用的对象列表.

后面的文章会具体介绍parser和解释器的细节.
