from django.contrib import admin

from .models import Project, Client, ProjectClass, Comment, Finance, Achievement, Plan, Contractor


class PlanInline(admin.TabularInline):
    model = Plan
    extra = 3



class ProjectAdmin(admin.ModelAdmin):
    # ...


    list_display = ('name', 'client','pub_date','project_class')
    list_filter = ['pub_date','client','plan__year','project_class']
    search_fields = ['name','client','pub_date','project_class','description']
    inlines = [PlanInline]
class FinanceAdmin(admin.ModelAdmin):
    # ...


    #list_display = ('question_text', 'pub_date')
    list_filter = ['project','pub_date']
    search_fields = ['project','name','client']
    list_display = ('project', 'title', 'cash','pub_date','comment')



class PlanAdmin(admin.ModelAdmin):
    # ...
    list_display = ('project', 'year', 'cash')
    


admin.site.register(Project, ProjectAdmin)
admin.site.register(Client)
admin.site.register(ProjectClass)
admin.site.register(Comment,)
admin.site.register(Finance,FinanceAdmin)
admin.site.register(Achievement)
admin.site.register(Plan,PlanAdmin)
admin.site.register(Contractor)



# Register your models here.
