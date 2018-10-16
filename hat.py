'''module to import and read follow up update generated by excell
    into list alaa zak  23-092018'''

import csv
import sys
from datetime import datetime

from maneger.models import Project, Client, ProjectClass, Comment, Finance, Achievement, Plan, Contractor
from django.utils import timezone

#tables = [ Project, Client,  Comment, Finance, Achievement, Plan, Contractor]
#for table in tables:
  #  PO = table.objects.all().delete()
PO = Project.objects.all().delete()
PO = Client.objects.all().delete()
PO = ProjectClass.objects.all().delete()
PO = Finance.objects.all().delete()
PO = Comment.objects.all().delete()
PO = Finance.objects.all().delete()
PO = Achievement.objects.all().delete()
PO = Plan.objects.all().delete()
PO = Contractor.objects.all().delete()
#PO.save()




file = [sys.argv[1],'follow.csv']
file = file[1]

if file == None:
    raise 'Please provide file as first argument'


buffer_client = ''
buffer_plan = ''
skippers = ['اجمالى','الاجمالي','']
followandplanning_text = 'مشروعات تخطيط ومتابعه'
followandplanning = 'تخطيط ومتابعه'
mashro3at = 'مشروعات'
handasiyya = ['هندسيه','هندسية']
armant = ['ارمنت','أرمنت']
handasy = 'هندسي'
handasy_text = 'ق.هندسيه'
projects_list = []
def hat():
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
        
            if row[1] in skippers:
                continue
        
            if row[3] in [0,'']:
                continue
        
            if row[0] != '':
                buffer_client = row[0]


        # item = f'{row[3]} -- {row[1]} --counting {len(row[1])}'
        # print(item)
        
            one_project = dict(
                ettimad_no=row[3],
                client=buffer_client,
                name=row[1],
                plan_year=row[2],
                total_budjet=row[4],
                current_year_budget=row[5],
                past_years_budjet=row[6],
                past_total_spent=row[7],
                current_year_spent=row[8],
                achivement_progress=row[13],
                contractors=row[14],
                status=row[15],
                )

            projects_list.append(one_project)

    
#print(projects_list,'---\n', len(projects_list))
    for project in projects_list:
    
        
        #client handling
        try: 
            if project['client'] in armant:
                project['client'] = armant[0]
            c  = Client.objects.get(name=project['client'].strip())
            print('found')
        except Client.DoesNotExist:
            c = Client.objects.create(name=project['client'].strip())
            print('created')
       
       # Project.objects.creare(name=project['name'], client=c,pub_date=timezone.now(), description='------',   
    #contractors handling
        contractors = project['contractors'].split('+')
        for contractor in contractors:
            if followandplanning in contractor:
                    contractor = followandplanning_text
            elif mashro3at in contractor and followandplanning not in contractor:
                contractor = mashro3at

            elif handasy in contractor:

                contractor = handasy_text

            elif contractor in ['',' ']:
                continue
            try:
                con = Contractor.objects.get(name=contractor.strip())
                print('found',contractor.strip())
            except Contractor.DoesNotExist:
                con = Contractor.objects.create(name=contractor.strip())
                print('created',contractor.strip())
    
        try:
            cl = ProjectClass.objects.get(text='normal')
            print('found')
        except ProjectClass.DoesNotExist:
            cl = ProjectClass.objects.create(text='normal')
            print('created')
        p = Project.objects.create(name=project['name'], client=c,pub_date=timezone.now(), description='------', project_class=cl)
        
        #handling plans
        
        if (project['plan_year'].strip()) != '':
            plantext = project['plan_year'].strip()
        plan_yers_array = plantext.split('/')
        print(plan_yers_array,project['name'])
        # replace 0 with one 2018-1015
        plan_year = int(plan_yers_array[1].strip())
        cash = float(project['current_year_budget'].strip()) 
        pl = Plan.objects.create(project=p, cash=cash, year=plan_year)

        #tentaitive past and future plans
        # keys: total_budjet  past_years_budjet
        past_years_budjet = int(project['past_years_budjet'].strip())
        total_budjet = int(project['total_budjet'].strip())
        #current_year_budget
        current_year_budget = int(project['current_year_budget'].strip())
        if past_years_budjet > 0:
            prev_pl = Plan.objects.create(project=p, cash=past_years_budjet, year=plan_year-1)
        future_budget = total_budjet - past_years_budjet - current_year_budget

        if future_budget > 0:
            future_pl = Plan.objects.create(project=p, cash=future_budget, year=plan_year+1)

        #handeling past spent
        # key: past_total_spent
        past_total_spent = float(project['past_total_spent'].strip())
        if past_total_spent > 0:
            pf = Finance.objects.create(project=p, title='past spent', cash=past_total_spent,pub_date='2017-5-1', comment='-----')

        #handeling current year spent
        # key: current_year_spent
        current_year_spent =  float(project['current_year_spent'].strip())
        ###    
        #if current_year_spent > 0:
        cf = Finance.objects.create(project=p, title='current year spent', cash=current_year_spent,pub_date='2017-9-1', comment='-----')

         #handeling achievment
        # key: achivement_progress
        achivement_progress =  float(project['achivement_progress'].strip())
        ###
        #if current_year_spent > 0:
        achi = Achievement.objects.create(project=p, title='Achievement tilldate', percent=achivement_progress, pub_date=datetime(2018,9,1), comment='-----')
        
         #handeling status
        # key: status
        status = project['status']
        sta = Comment.objects.create(project=p, text=status, pub_date=str(plan_year)+'-9-1')




        




        
    """
     p = Project.create(
            name=project[name],
            client=
    """
