from tastypie import fields
from tastypie.resources import ModelResource
from models import Post, Comment, Tag
from django.contrib.auth.models import User
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash
from django.conf.urls import url

class UserResource(ModelResource):
	posts=fields.ToManyField('blog.api.mePostResource','post_set', null=True, full=True)
	comments=fields.ToManyField('blog.api.CmtResource','comment_set', null=True, full=True)
	class Meta:
		queryset= User.objects.all()
		resource_name='user'
		authentication=Authentication()
        authorization=Authorization()
        always_return_data=True


class PostResource(ModelResource):

	user=fields.ForeignKey(UserResource, 'user')
	comments=fields.ToManyField('blog.api.CmtResource','comment_set', null=True, full=True)
	tags=fields.ToManyField('blog.api.TagResource', 'tags', null=True, full=True)
	class Meta:
		queryset = Post.objects.all()
		resource_name = 'post'
		#fields= ['title']
		authentication=Authentication()
		authorization=Authorization()
		always_return_data=True

class CmtResource(ModelResource):
	user=fields.ToOneField(UserResource,'user')
	post=fields.ToOneField(PostResource,'post')
	replyTo=fields.ForeignKey('self','comm', null=True)
	replies=fields.ToManyField('self','comm_set',null=True)

	class Meta:
		queryset = Comment.objects.all()
		resource_name='comment'
		authentication=Authentication()
		authorization=Authorization()
		always_return_data=True

class TagResource(ModelResource):
	post=fields.ToManyField(PostResource, 'post_set', null=True)
	
	class Meta:
		queryset=Tag.objects.all()
		resource_name='tag'

class SearchResource(ModelResource):
    class Meta:
        authorization=Authorization()
        authentication=Authentication()

    def prepend_urls(self):
        return[url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),]

    def get_search(self, request, **kwargs):
        reqdata=request.GET.get('q','')
        results=[]
        posttitle=Post.objects.filter(title__contains=reqdata)
        postbody=Post.objects.filter(content__contains=reqdata)
        tag=Tag.objects.filter(name__contains=reqdata)
        posttag= Post.objects.filter(tags=tag)
        results.append({'posttitle':posttitle})
        results.append({'postbody':postbody})
        results.append({'tag':posttag})
        return self.create_response(request, results)