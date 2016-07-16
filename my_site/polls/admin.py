from django.contrib import admin
from polls.models import Choice,Question,UserProfile

class ChoiceInLine(admin.TabularInline):
	model = Choice
	extra = 3
	

class QuestionAdmin(admin.ModelAdmin):
	#fields = ['pub_date' , 'question' , ]
	fieldsets = [(None, {'fields':['question']}) ,
		 ('Date information' , {'fields':['pub_date'],'classes' : ['collapse']}),]
	inlines=[ChoiceInLine]
	list_display = ('question' , 'pub_date' , 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question']
	ordering = ['-pub_date']

admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile)


# Register your models here.
