from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name 


class Contractor(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name





class ProjectClass(models.Model):
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text 

        




class Project(models.Model):
    name = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contractors = models.ManyToManyField(Contractor, null=True)
    pub_date = models.DateTimeField('date published')
    description = models.TextField()
    project_class = models.ForeignKey(ProjectClass, on_delete=models.CASCADE)
    #plan = models.ManyToManyField(Plan)
    def __str__(self):
        return self.name

    @property
    def total_progress(self):
        "Returns the person's full name."
        return str(sum([x.percent for x in self.achievement_set.all()]))

    @property
    def plans(self):
        "Returns the person's full name."
        return ' - '.join( [str(y.year) for y in self.plan_set.all()])


    @property
    def total_budget(self):
        "Returns the person's full name."
        return str((sum( [y.cash for y in self.plan_set.all()])))




class Plan(models.Model):
    # project = models.ManyToManyField(Project)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    year = models.IntegerField()
    cash = models.FloatField()
    def __str__(self):
        return str(self.year) 
    class Meta:
        unique_together = (("project", "year"),)







class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.text[:30] 







class Finance(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cash = models.FloatField()
    pub_date = models.DateTimeField('date published')
    comment = models.TextField()
    def __str__(self):
        return self.title 

class Achievement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    percent = models.FloatField()
    pub_date = models.DateTimeField('date published')
    comment = models.TextField()
    def __str__(self):
        return self.title 


    

    
