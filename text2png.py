# http://blog.felixc.at/2011/05/python-text-to-png/

# note: for install pil (Image lib), use:
# pip install pil 
# pil does not suppot python 3.

def text2png(text):
    # Configurations:
    adtexts = [u'---------------', u'广告太多是不对的!']
    textcolor = "#000000"
    adcolor = "#FF0000"
    
    # Don't touch the code below
    import Image, ImageDraw, ImageFont, uuid
    
    # Build rich text for ads
    ad = []
    for adtext in adtexts:
        ad += [(adtext.encode('gbk'), adcolor)]
    
    # Wrap line for text
    #   Special treated Chinese characters
    #   Workaround By Felix Yan - 20110508
    wraptext = [""]
    l = 0
    for i in text.decode('utf-8'):
        fi = i.encode('gbk')
        delta = len(fi)
        if i == '\n':
            wraptext += [""]
            l = 0
        elif l + delta > 40:
            wraptext += [fi]
            l = delta
        else:
            wraptext[-1] += fi
            l += delta
            
    # Format wrapped lines to rich text
    wrap = [(text, textcolor) for text in wraptext]
    wrap += ad
    
    # Draw picture
    i = Image.new("RGB", (330, len(wrap) * 17 + 5), "#FFFFFF") # create a new img obj.
    d = ImageDraw.Draw(i)
    f = ImageFont.truetype("YaHeiYt.ttf", 16)
    for num, (text, color) in enumerate(wrap):
        d.text((2, 17 * num + 1), text.decode('gbk'), font = f, fill = color)
    
    # Write result to a temp file
    filename = uuid.uuid4().hex + ".png" 
    with open("/tmp/" + filename, "wb") as s:
        i.save(s, "PNG") # call image obj's save method. 
    return "/tmp/" + filename    # it's a string!

if __name__ == "__main__":
    text2png(r'''郁孤台①下清江水，
中间多少行人②泪。
西北望长安③，可怜无数山。
青山遮不住，毕竟东流去。
江晚正愁余④，山深闻鹧鸪⑤。''')
