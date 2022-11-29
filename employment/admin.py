from django.contrib import admin
from django.contrib.auth.models import User, Group
from admin_interface.models import Theme
from .models import *
from django.contrib.auth.admin import UserAdmin


class ManyQuiz(admin.TabularInline):

    model = Quiz
    fields = ['question','reponse','radio_name','score']



class PostAdmin(admin.ModelAdmin):
        inlines = [ManyQuiz,]

class ManyQuizArchie(admin.TabularInline):

    model = QuizArchive
    fields = ['question','reponse',]



class PostAdminArchive(admin.ModelAdmin):
        inlines = [ManyQuizArchie,]

admin.site.register(Archive,PostAdminArchive)
admin.site.register(Formateur)
admin.site.register(Formation)
admin.site.register(ResultTestArchive)
admin.site.register(Certificat)
admin.site.register(DomaineFormation)
admin.site.register(AssociatDomaineFormationParCategory)
admin.site.register(Domaine)
admin.site.register(AssociatDomaineParCategory)
admin.site.register(Condidat)
admin.site.register(Result)
admin.site.register(Test,PostAdmin)
admin.site.unregister(Theme)
