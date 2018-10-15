'''module to import and read follow up update generated by excell
    into list alaa zak  23-092018'''

import csv
import sys

from maneger.models import Project, Client, ProjectClass, Comment, Finance, Achievement, Plan, Contractor
from django.utils import timezone

file = [sys.argv[1],'follow.csv']
file = file[1]

if file == None:
    raise 'Please provide file as first argument'


buffer_client = ''
skippers = ['اجمالى','الاجمالي','']
followandplanning_text = 'مشروعات تخطيط ومتابعه'
followandplanning = 'تخطيط ومتابعه'
mashro3at = 'مشروعات'
handasiyya = ['هندسيه','هندسية']
armant = ['ارمنت','أرمنت']
projects_list = []

def import():
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
        if project[client] in armant:
            project[client] = armant[0]
        c = Client.objects.get(name=project['client'].strip())
        print('found')
    except Client.DoesNotExist:
        c = Client.objects.create(name=project['client'].strip())
        print('created')
    
    #contractors handling
    contractors = project['contractors'].split('+')
    for contractor in contractors:
        if followandplanning in contractor:
                contractor = followandplanning_text
        elif mashro3at in contractor and followandplanning not in contractor:
            contractor = mashro3at
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
        clProjectClass = ProjectClass.objects.create(text='normal')
        print('created')
        
    """
     p = Project.create(
            name=project[name],
            client=
    """