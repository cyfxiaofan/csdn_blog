# - * - coding:utf-8 - * -
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

'''
<div class="ui-paging-container">
    <ul>
        <li class=" ui-pager ui-pager-disabled">上一页</li>
        <li data-page="1" class="ui-pager focus">1</li>
        <li data-page="1" class="ui-pager">2</li>
        <li data-page="1" class="ui-pager">3</li>
        <li  class="ui-paging-ellipse">...</li>
        <li data-page="1" class="ui-pager">22</li>
        <li class="js-page-action ui-pager">下一页</li>
    </ul>
</div>
'''

@register.simple_tag
def PageShow(count, request):
    #若总页数是 1 那么不显示页码
    if int(count) == 1:
        return format_html('')
    #接受页码
    p = int(request.GET.get('page',1))

    #正常情况
    begin = p-1
    end = p+1


    #如果总页码小于6
    if p<4:
        begin=1
        end=4
    #p 超出了总页数-5
    if p>count-3:
        begin = p-1
        end = count

        # 总页码少于10
    if count < 6:
        begin = 1
        end = count

    url = request.path

    args = ''
    for k,v in request.GET.items():
        if k != 'page':
            args+=k+'='+v+'&'

    s= ''

    # 拼接上一页
    if p == 1:
        s+="""
           <li class=" ui-pager ui-pager-disabled">上一页</li>
        """
    else:
        s+="""
             <li href="{url}?{args}page={v}" class="js-page-action ui-pager">上一页</li>
        """.format(url=url,args=args,v=p-1)

    # 拼接中间页   思路：第一页和 必然显示的  倒数第一页是必然显示的
    '''
    情况1 ： 第一页 ...  中间页 ... 最后一页
    情况2 ： 不足6页 ，显示全部页  不显示 ...
    情况3：  当前页在后3页 ， 显示后3页 只显示前边的... 
    情况4：  当期页在前3页，显示1-4， 只显示后边的 ...
    '''
    if p<4 and count>=6:
        for i in range(begin,end+1):
            if i != p:
                s+="""
                    <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
                """.format(url=url,args=args,v=i)
            else:
                s+="""
                    <li  data-page="{v}" class="ui-pager focus">{v}</li>
                """.format(v=i)
        s+="""
             <li  class="ui-paging-ellipse">...</li>
        """
        s+="""
                <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager">{v}</li>
            """.format(url=url,args=args,v=count)
    elif count<6:
        for i in range(begin,end+1):
            if i != p:
                s+="""
                    <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
                """.format(url=url,args=args,v=i)
            else:
                s+="""
                   <li  data-page="{v}" class="ui-pager focus">{v}</li>
                """.format(v=i)
    elif p >count-3:
        s += """
                   <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
               """.format(url=url, args=args, v=1)
        s += """
                <li  class="ui-paging-ellipse">...</li>
            """
        for i in range(begin, end+1):
            if i != p:
                s+="""
                    <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
                """.format(url=url,args=args,v=i)
            else:
                s+="""
                    <li data-page="{v}" class="ui-pager focus">{v}</li>
                """.format(v=i)

    else:
        s += """
            <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
           """.format(url=url, args=args, v=1)
        s += """
                <li  class="ui-paging-ellipse">...</li>
           """
        for i in range(begin, end+1):
            if i != p:
                s+="""
                    <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
                """.format(url=url,args=args,v=i)
            else:
                s+="""
                    <li data-page="{v}" class="ui-pager focus">{v}</li>
                """.format(v=i)

        s += """
              <li  class="ui-paging-ellipse">...</li>    
            """
        s += """
               <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
            """.format(url=url, args=args, v=count)

    #下一页
    if p == count:
        s += """
                  <li class="js-page-action ui-pager ui-pager-disabled ">下一页</li>
               """
    else:
        s += """
            <li href="{url}?{args}page={v}" class="js-page-action ui-pager">下一页</li>
               """.format(url=url, args=args, v=p +1)


    return format_html(s)



@register.simple_tag
def PageShowRight(count, request):
    #若总页数是 1 那么不显示页码
    if int(count) == 1:
        return format_html('')
    #接受页码
    p = int(request.GET.get('page',1))

    #正常情况
    begin = p-1
    end = p+1


    #如果总页码小于6
    if p<4:
        begin=1
        end=4
    #p 超出了总页数-5
    if p>count-3:
        begin = p-1
        end = count

        # 总页码少于10
    if count < 6:
        begin = 1
        end = count

    comment_type = int(request.GET.get('comment_type',''))

    url = request.path

    args = ''
    for k,v in request.GET.items():
        if k != 'page':
            args+=k+'='+v+'&'

    s= ''

    if comment_type == 1:
        # 拼接上一页
        if p == 1:
            s+="""
               <li class=" ui-pager ui-pager-disabled">上一页</li>
            """
        else:
            s+="""
                 <li href="{url}?{args}page={v}" class="js-page-action ui-pager">上一页</li>
            """.format(url=url,args=args,v=p-1)
    else:
            s+="""
               <li class=" ui-pager ui-pager-disabled">上一页</li>
            """


    # 拼接中间页   思路：第一页和 必然显示的  倒数第一页是必然显示的
    '''
    情况1 ： 第一页 ...  中间页 ... 最后一页
    情况2 ： 不足6页 ，显示全部页  不显示 ...
    情况3：  当前页在后3页 ， 显示后3页 只显示前边的... 
    情况4：  当期页在前3页，显示1-4， 只显示后边的 ...
    '''
    if p<4 and count>=6:
        for i in range(begin,end+1):
            if i != p:
                s+="""
                    <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
                """.format(url=url,args=args,v=i)
            else:
                s+="""
                    <li  data-page="{v}" class="ui-pager focus">{v}</li>
                """.format(v=i)
        s+="""
             <li  class="ui-paging-ellipse">...</li>
        """
        s+="""
                <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager">{v}</li>
            """.format(url=url,args=args,v=count)
    elif count<6:
        for i in range(begin,end+1):
            if i != p:
                s+="""
                    <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
                """.format(url=url,args=args,v=i)
            else:
                s+="""
                   <li  data-page="{v}" class="ui-pager focus">{v}</li>
                """.format(v=i)
    elif p >count-3:
        s += """
                   <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
               """.format(url=url, args=args, v=1)
        s += """
                <li  class="ui-paging-ellipse">...</li>
            """
        for i in range(begin, end+1):
            if i != p:
                s+="""
                    <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
                """.format(url=url,args=args,v=i)
            else:
                s+="""
                    <li data-page="{v}" class="ui-pager focus">{v}</li>
                """.format(v=i)

    else:
        s += """
            <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
           """.format(url=url, args=args, v=1)
        s += """
                <li  class="ui-paging-ellipse">...</li>
           """
        for i in range(begin, end+1):
            if i != p:
                s+="""
                    <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
                """.format(url=url,args=args,v=i)
            else:
                s+="""
                    <li data-page="{v}" class="ui-pager focus">{v}</li>
                """.format(v=i)

        s += """
              <li  class="ui-paging-ellipse">...</li>    
            """
        s += """
               <li href="{url}?{args}page={v}" data-page="{v}" class="ui-pager ">{v}</li>
            """.format(url=url, args=args, v=count)

    #下一页
    if comment_type == 1:
        if p == count:
            s += """
                      <li class="js-page-action ui-pager ui-pager-disabled ">下一页</li>
                   """
        else:
            s += """
                <li href="{url}?{args}page={v}" class="js-page-action ui-pager">下一页</li>
                   """.format(url=url, args=args, v=p +1)
    else:
        s += """
            <li href="{url}?{args}page={v}" class="js-page-action ui-pager">下一页</li>
               """.format(url=url, args=args, v=2)


    return format_html(s)
