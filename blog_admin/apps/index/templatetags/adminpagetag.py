from django import template

register = template.Library()


@register.filter(is_safe=True)
def floattostr(value, value2=''):
    return str(value) + str(value2)


# 自定义过滤器
@register.filter
def kong_upper(val):
    # print ('val from template:',val)
    return val.upper()


# 自定义分页优化标签
from django.utils.html import format_html


@register.simple_tag
def cheng(var1, var2):
    res = float(var1) * float(var2)

    return '%.2f' % res


@register.simple_tag
def PageShow(count, request):
    p = int(request.GET.get('page',1))
    begin = p-4
    end = p+5

    # 页码超出总页数-5  显示最后十页
    if p > count-5:
        begin = p-9
        end = count
    # 当前页码不到5  显示前十页
    if p < 5:
        begin = 1
        end = 10
    # 总页数不足十页  显示全部页
    if count < 10:
        begin = 1
        end = count

    url = request.path
    print(url)

    # 生成地址栏除了？page之外的其他参数组成的字符串
    # 因为Page在下边拼接的时候再传入
    args = ''
    for k,v in request.GET.items():
        if k != 'page':
            args += '&'+k+'='+v


    s = ''
    # 先拼接首页
    s +="""
    <li class="previous">
       <a href="{url}?page={v}{args}" class="waves-effect"><span aria-hidden="true">&larr;</span> 开始</a>
    </li>
    """.format(v=1,url=url,args=args)

    # 拼接上一页
    # 若是第一页则上一页不能点
    if p ==1:
        s+="""
        <li>
            <a href="#" class="waves-effect">
                <i class="material-icons">chevron_left</i>
            </a>
        </li>
        """
    else:
        s+="""
        <li>
            <a href="{url}?page={v}{args}" class="waves-effect">
                <i class="material-icons">chevron_left</i>
            </a>
        </li>
        """.format(url=url,v=p-1,args=args)

    # 拼接中间所显示页码
    for i in range(begin,end+1):
        if i ==p :
            s+="""
                <li><a href="{url}?page={v}{args}" class="waves-effect" style="color:red">{v}</a></li>
            """.format(v=i,url=url,args=args)
        else:
            s+="""
                 <li><a href="{url}?page={v}{args}" class="waves-effect" >{v}</a></li>
            """.format(v=i,url=url,args=args)

    # 拼接下一页
    if p==count:
        s+="""
            <li>
            <a href="#" class="waves-effect">
                <i class="material-icons">chevron_right</i>
            </a>
        </li>
        """
    else:
        s+="""
        <li>
            <a href="{url}?page={v}{args}" class="waves-effect">
                <i class="material-icons">chevron_right</i>
            </a>
        </li>
        """.format(url=url,v=count,args=args)

    # 拼接结束页
    s+="""
    <li class="next">
        <a href="{url}?page={v}{args}" class="waves-effect">结束 <span aria-hidden="true">&rarr;</span></a>
    </li>
    """.format(v=count,url=url,args=args)

    # 返回拼接好的 s
    return format_html(s)




'''
    # 首页
    <li class="previous">
       <a href="{url}?page={v}{args}" class="waves-effect"><span aria-hidden="true">&larr;</span> 开始</a>
    </li>

    # 判断上一页
        <li>
            <a href="{url}?page={v}{args}" class="waves-effect">
                <i class="material-icons">chevron_left</i>
            </a>
        </li>

    # 循环页码数
    <li><a href="{url}?page={v}{args}" class="waves-effect" style="color:red">{v}</a></li>

    # 判断下一页
        <li>
            <a href="{url}?page={v}{args}" class="waves-effect">
                <i class="material-icons">chevron_right</i>
            </a>
        </li>

    # 总页数
    <li class="next">
        <a href="{url}?page={v}{args}" class="waves-effect">结束 <span aria-hidden="true">&rarr;</span></a>
    </li>
'''

