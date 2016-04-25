from django.contrib import admin

# Register your models here.

from commonblog.models import CommonBlog

class CommonBlogAdmin(admin.ModelAdmin):
	list_display = ['student','content','timestamp']
	search_fields = ['student.username']
	class Meta:
		model = CommonBlog


admin.site.register(CommonBlog,CommonBlogAdmin)

