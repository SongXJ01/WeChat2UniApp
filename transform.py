import re

res = []  # 转换结果


# 使用正则表达式替换 wxml 中的内容
def convert(line):
    res_line = line
    # 匹配 bindchange="bindPickerClassTypeChange" --> @change="bindPickerClassTypeChange"
    ret = re.match(r'(.*)bind([\w|_]*?)="([\w|_]*?)"(.*)', res_line)
    if ret:
        res_line = line.replace('bind' + ret.group(2) + '="' + ret.group(3),
                                '@' + ret.group(2) + '="' + ret.group(3))
        print(res_line)

    # 匹配 wx:if="{{imgList.length<4}}" --> v-if="imgList.length<4"
    ret = re.match(r'(.*)(wx:if=\"{{)(.*)(}}\")(.*)', line)
    if ret:
        res_line = res_line.replace(ret.group(2) + ret.group(3), 'v-if="' + ret.group(3)).replace(
            ret.group(3) + ret.group(4), ret.group(3) + "\"")
        # print(res_line)

    # 匹配 wx:for="{{imgList}}" --> v-for="(item,index) in imgList"
    ret = re.match(r'(.*)(wx:for=\"{{)(.*?)(}}\")(.*)', res_line)
    if ret:
        res_line = res_line.replace(ret.group(2) + ret.group(3), 'v-for="(item,index) in ' + ret.group(3)).replace(
            ret.group(3) + ret.group(4), ret.group(3) + "\"")
        # print(res_line)

    # 匹配 wx:key="{{index}}" --> v-bind:key="item.id"
    ret = re.match(r'(.*)(wx:key=\"{{)(.*?)(}}\")(.*)', res_line)
    if ret:
        res_line = res_line.replace(ret.group(2) + ret.group(3) + ret.group(4), 'v-bind:key="item.id"')
        # print(res_line)

    # 匹配 data-id="{{item._id}}" --> :data-id="item._id"
    ret = re.match(r'(.*)data-(.*?)(\"{{)(.*?)(}}\")(.*)', res_line)
    while ret:  # 一行可能出现多个
        res_line = res_line.replace("data-" + ret.group(2) + ret.group(3) + ret.group(4) + ret.group(5),
                                    ":data-" + ret.group(2) + '"' + ret.group(4) + '"')
        ret = re.match(r'(.*)data-(.*?)(\"{{)(.*?)(}}\")(.*)', res_line)

    # 匹配 value="{{identity_index}}" --> :value="identity_index"
    ret = re.match(r'(.*)value="{{(.*?)}}"(.*)', res_line)
    if ret:
        res_line = res_line.replace('value="{{' + ret.group(2) + '}}"', ':value="' + ret.group(2) + '"')
        # print(res_line)

    # 匹配 range="{{identity_list}}" --> :range="identity_list"
    ret = re.match(r'(.*)range="{{(.*?)}}"(.*)', res_line)
    if ret:
        res_line = res_line.replace('range="{{' + ret.group(2) + '}}"', ':range="' + ret.group(2) + '"')

    # 匹配 class="cu-modal {{modal=='ModalEdit'?'show':''}}" --> :class="'cu-modal'+[modal=='ModalEdit'?'show':'']"
    ret = re.match(r'(.*)class="([^"]*?){{(.*?)}}(.*?)"', res_line)
    if ret:
        res_line = res_line.replace('class="' + ret.group(2) + '{{' + ret.group(3) + '}}' + ret.group(4) + '"',
                                    ':class="\'' + ret.group(2) + '\'+[' + ret.group(3) + ']' + ret.group(4) + '"')

    # 匹配 style="animation-delay: {{(index+1)*0.1}}s;" --> :style="[{animationDelay: (index + 1)*0.1 + 's'}]"
    res_line = res_line.replace('style="animation-delay: {{(index+1)*0.1}}s;"',
                                ':style="[{animationDelay: (index + 1)*0.1 + \'s\'}]"')

    return res_line


# 打开需要转换的 .wxml
with open("WeChat.wxml", "r", encoding='utf-8') as f:  # 打开文件
    data = f.readlines()  # 读取文件
    for line in data:
        opLine = line.replace('isBack="{{true}}"', ':isBack="true"').replace('bindtap', '@click')
        opLine = convert(opLine)
        res.append(opLine)

# 将转换结果写入
with open("uniApp.vue", "w", encoding='utf-8') as f:
    f.write("<template>\n\t<view>\n")  # Vue 头部内容
    for line in res:
        f.write(line)
    f.write(
        "\n\n\t</view>\n</template>\n\n<script>\nexport default {\n\tdata() {\n\t\treturn {\n\t\t}\n\t},\n\tmethods: {"
        "\n\t}\n}\n</script>\n\n<style>\n</style> ")  # Vue 尾部内容
