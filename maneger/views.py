from django.shortcuts import render

from django.http import HttpResponse

from .models import Project, Client, Plan, Finance

import datetime

def index(request):
    q = Project.objects.all()
    pk = []
    for i in q:
        pk.append(i.pk)
    return HttpResponse(q)

def fup(request,  from_year, from_month, from_day, to_year, to_month, to_day):
    #p = print(str(year),str(month))
    #@#$%^&*()
    #projects_list = Project.objects.all().order_by('client')
    projects_list = Project.objects.filter(plan__gt=0).distinct().order_by("client").all()


   # r =str(from_year)+ "----"  + str(from_month)+"<br>"+ 'id ---->name + --++  +  total_progress +    ++-- + client name + <br>'
    r=""
    info =[]
    for project in projects_list:
       
        year_pudjet_set = Plan.objects.filter(project = project, year = from_year)
        if len(year_pudjet_set) == 0:
        # yb year budget
            yb = 0
        else:
            yb = year_pudjet_set[0].cash
       
        # last years budget
        l_year_pudjet_set = Plan.objects.filter(project = project,year__lt = from_year)
        if len(l_year_pudjet_set) == 0:
            lb = 0
        else:
            lb = sum([x.cash for x in l_year_pudjet_set])
        
       
       
       
       
       
       
        #spent tell now
       # spent_before_from_date = str(sum([x.cash for x in Finance.objects.all().filter(project=project ,pub_date__lt = "{0}-{1}-{2}".format(from_year,from_month,from_day))]))
        if from_month in [7,8,9,10,11,12]:
            starting_fiscal_year = from_year
        else:
            starting_fiscal_year = from_year - 1
        spent_before_from_date = str(sum(x.cash for x in Finance.objects.filter(project = project ).filter(pub_date__lt = datetime.date(starting_fiscal_year,7,1) )))

        #spent tell now
        #spent_between_date = str(sum([x.cash for x in Finance.objects.all().filter(project=project ,pub_date__gte = "{0}-{1}-{2}".format(from_year,from_month,from_day)).filter(project=project ,pub_date__lte = "{0}-{1}-{2}".format(to_year,to_month,to_day))]))
        
        spent_between_date = str(sum(x.cash for x in Finance.objects.filter(project = project ).filter(pub_date__gte = datetime.date(starting_fiscal_year,7,1) ).filter(pub_date__lt = datetime.date(to_year, to_month, to_day))))
       
       #~!@#$%^&*(wrong in more than in the past reports)_+
        total_spent = str(sum(x.cash for x in Finance.objects.filter(project = project )) )

        #finance progress
        if to_month in [1,2,3,4,5,6]:
            prog_year = to_year
        else:
            prog_year = to_year + 1

        #planned prog
        years_nuber = Plan.objects.filter(project = project).count()
        starting_year =min( [x.year for x in Plan.objects.filter(project = project)])
        planned_prog = datetime.timedelta(days=(to_day+(to_month + 6)*31)+(prog_year - starting_year)*365)/ datetime.timedelta(days=years_nuber * 365)
       
     

        
        try:
            finance_progress =str( float( total_spent) / float(Plan.objects.filter(project_id = project.id).filter(year = prog_year)[0].cash))
        except:
            finance_progress = '0'
        total_finance_budget = str( float( total_spent) / float( project.total_budget))

        r +="id:-> "+ str(project.pk) + " client:-> " + project.client.name +" name:-> " +project.name + ' total money:-> '+  project.total_progress +' plan:-> ' + project.plans +' total budget:-> '+ project.total_budget+' year budget:-> '+ str(yb)  +' last years budge:-> '+ str(lb)+" spent before:-> "+spent_before_from_date  +" spent in between:-> "+  spent_between_date +" curnt year finance progress: "+finance_progress +"total finance progress: "+ total_finance_budget  +"planned prog:-%> "+str(planned_prog) +"actual prog:->" +str(project.total_progress)+'<br>-----------------------------------------------------<br>'
        data = dict(
                id = str(project.pk),
                client=project.client.name,
                project_name=project.name,
                plan=project.plans ,
                total_budget=project.total_budget,
                year_budget=str(yb),
                lybudget=str(lb),
                spent_before=spent_before_from_date,
                between= spent_between_date,
                cyf=finance_progress,
                tfp=total_finance_budget,
                pp=str(planned_prog),
                ap=str(project.total_progress),
                from_year = from_year,
                from_month = from_month,
                from_day = from_day,
                to_year = to_year,
                to_month = to_month,
                to_day = to_day
                )

        info.append(data)
    table_headers =[
            'id',
            'factory',
            'project name',
            'plan',
            'total budget',
            'year budget',
            'last years budge',
            'spent before',
            'spent in between',
            'current year finance progress',
            'total finance progress',
            'planned progress',
            'actual progess'
            ]




    rd = dict(from_year = from_year,
                from_month = from_month,
                from_day = from_day,
                to_year = to_year,
                to_month = to_month,
                to_day = to_day
                )


    context = {'table_headers': table_headers, 'info':info, 'rd':rd }

    #return HttpResponse(r)
    return render(request,'maneger/fup.html',context)


# Create your views here.
