from django.db import models

# Create your models here.

#用户表
class Users(models.Model):
	# 用户id 密码 昵称   手机号  状态 头像 关注数 粉丝数 是否vip 关注人id 注册时间
	userid = models.CharField(max_length=20)
	password = models.CharField(max_length=100)
	username = models.CharField(max_length=50)
	phone = models.CharField(max_length=11)
	status = models.IntegerField(default=0)
	head_url = models.CharField(max_length=500,null=True,blank=True)
	notice = models.TextField(default=0)
	fans = models.TextField(default=0)
	vipuser = models.IntegerField(default=0)
	addtime=models.DateTimeField(auto_now_add=True)
	bgimg = models.CharField(max_length=50,null=True,blank=True)
	bghistory = models.TextField(default=0,null=True,blank=True)
	viptime = models.CharField(max_length=500,null=True,blank=True)
	score = models.CharField(max_length=100,null=True,blank=True)
	affirm_blog = models.TextField(default=0,null=True,blank=True)
	yl_1 = models.CharField(max_length=500,null=True,blank=True)
	yl_2 = models.CharField(max_length=500,null=True,blank=True)
	yl_3 = models.CharField(max_length=500,null=True,blank=True)
	yl_4 = models.CharField(max_length=500,null=True,blank=True)
	yl_5 = models.CharField(max_length=500,null=True,blank=True)


	class Meta:
		managed = True

#博客分类表
class Blogcates(models.Model):
	#标题 路由 状态 权重值
	title = models.CharField(max_length=50)
	path = models.CharField(max_length=50)
	status = models.IntegerField(default=0)
	list_order = models.IntegerField(default=0)

#博客表
class Blog(models.Model):
	# 标题 标签 状态 发布时间 阅读数 收藏数 点赞数 内容 用户表 博客分类表 分类专栏表 是否允许评论 权重
	title = models.CharField(max_length=100)
	label = models.CharField(max_length=50)
	status = models.IntegerField(default=0,null=True,blank=True)
	addtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	look = models.IntegerField(default=0,null=True,blank=True)
	collection = models.IntegerField(default=0,null=True,blank=True)
	affirm = models.IntegerField(default=0,null=True,blank=True)
	ginfo = models.TextField()
	uid = models.ForeignKey(to='Users',to_field='id',on_delete=models.CASCADE)
	bgcate = models.ForeignKey(to='Blogcates',to_field='id',on_delete=models.CASCADE)
	zlid = models.ForeignKey(to='Zhuanlan',to_field='id',on_delete=models.CASCADE)
	ifcomment = models.IntegerField(default=0,null=True,blank=True)
	list_order = models.IntegerField(default=0,null=True,blank=True)
	beforeurl = models.CharField(max_length=300,null=True,blank=True)
	yuanchuang = models.IntegerField(default=0,null=True,blank=True)
	source = models.CharField(max_length=100,null=True,blank=True)
	today_looks = models.IntegerField(default=0,null=True,blank=True)


#评论表
class Comment(models.Model):
	# 博客表id 用户表id 时间 内容 点赞数 父级id 状态
	bid = models.ForeignKey(to='Blog',to_field='id',on_delete=models.CASCADE)
	uid = models.ForeignKey(to='Users',to_field='id',on_delete=models.CASCADE)
	ginfo = models.CharField(max_length=500)
	affirm = models.IntegerField(default=0)
	parentid = models.IntegerField(default=0)
	addtime = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=0)
	applyid = models.ForeignKey(to='self',to_field='id',on_delete=models.CASCADE)
	affim_user = models.TextField(default=0,null=True,blank=True)


#分类专栏表
class Zhuanlan(models.Model):
	# 外键用户表id  是否隐藏 状态 专栏标题 权重
	uid = models.ForeignKey(to='Users',to_field='id',on_delete=models.CASCADE)
	hide = models.IntegerField(default=0)
	status = models.IntegerField(default=0)
	title = models.CharField(max_length=50,default='未命名')
	list_order = models.IntegerField(default=0)

#收藏夹表
class Collect(models.Model):
	#外键用户表id 是否公开 状态 标题 描述
	uid = models.ForeignKey(to='Users',to_field='id',on_delete=models.CASCADE)
	hide = models.IntegerField(default=0)
	status = models.IntegerField(default=0)
	title = models.CharField(max_length=30,default='未命名')
	collect_blog = models.TextField(default=0,null=True,blank=True)
	list_order = models.IntegerField(default=0)

#轮播图表
class Banner(models.Model):
	#图片地址 图片索引  状态 链接 标题 所属页面 添加时间
	pic_url = models.CharField(max_length=200)
	pic_index = models.IntegerField(blank=True, null=True)
	status = models.IntegerField(default=0)
	blog_url = models.CharField(max_length=200)
	blog_title = models.CharField(max_length=100)
	cid = models.IntegerField(default=0,blank=True, null=True)
	addtime = models.DateField(auto_now_add=True)



# 登录日志
class LoginLog(models.Model):
	ip = models.CharField(max_length=100)



