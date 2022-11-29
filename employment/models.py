from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



class Formateur(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    gender=models.CharField(max_length=6,choices=[('MALE','MALE'),('FEMALE',('FEMALE'))])
    nb_formation=models.CharField(max_length=20)


    def __str__(self):
        return self.user.username

class Formation(models.Model):
    author=models.OneToOneField(Formateur,on_delete=models.CASCADE)
    nom=models.CharField(max_length=100)
    date_creation=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
    date_debut=models.DateTimeField()
    date_fin=models.DateTimeField()
    prix=models.CharField(max_length=255)
    nb_participants=models.CharField(max_length=20)

    def __str__(self):
        return self.author.user.username



class DomaineFormation(models.Model):
    nom_domaine=models.CharField(max_length=50)

    def __str__(self):
        return self.nom_domaine


class AssociatDomaineFormationParCategory(models.Model):
    category=models.CharField(max_length=50)
    formation=models.OneToOneField(Formation,on_delete=models.CASCADE)
    domaine=models.ForeignKey(DomaineFormation,on_delete=models.CASCADE)

    def __str__(self):
        return self.formation.nom+" domaine : "+self.domaine.nom_domaine




class Certificat(models.Model):
    date_creation=models.DateTimeField(auto_now_add=True)
    certif= models.FileField(upload_to='media/certif/')
    formation=models.OneToOneField(Formation,on_delete=models.CASCADE)



class Condidat(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    gender=models.CharField(max_length=6,choices=[('MALE','MALE'),('FEMALE',('FEMALE'))])
    profession = models.CharField(max_length=100)
    nb_tests=models.CharField(max_length=20)


    def __str__(self):
        return self.user.username


class Test(models.Model):
    titre=models.CharField(max_length=255)
    date_creation=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
    version=models.CharField(max_length=10)
    prix=models.CharField(max_length=255)
    type=models.CharField(max_length=255,choices=[('HARD SKILLS','HARD SKILLS'),('SOFT SKILLS','SOFT SKILLS')])

    def __str__(self):
        return self.titre+" version : "+self.version


class Quiz(models.Model):
    author=models.ForeignKey(Test,on_delete=models.CASCADE)
    question=models.CharField(max_length=255)
    reponse=models.CharField(max_length=255)
    radio_name=models.CharField(max_length=255)
    score=models.CharField(max_length=255)


class Result(models.Model):
    condidat=models.ForeignKey(Condidat,on_delete=models.CASCADE)
    test_effectue=models.ForeignKey(Test,on_delete=models.CASCADE)
    score=models.CharField(max_length=20)
    date_effectue=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.condidat.user.username+" test effectue : "+self.test_effectue.titre+" score : "+self.score


class Domaine(models.Model):
    nom_domaine=models.CharField(max_length=50)

    def __str__(self):
        return self.nom_domaine


class AssociatDomaineParCategory(models.Model):
    category=models.CharField(max_length=50)
    test=models.OneToOneField(Test,on_delete=models.CASCADE,related_name="tst")
    domaine=models.ForeignKey(Domaine,on_delete=models.CASCADE,related_name="dm")

    def __str__(self):
        return self.test.titre+" domaine : "+self.domaine.nom_domaine



class Archive(models.Model):
    titre=models.CharField(max_length=255)
    id_test_archive=models.ForeignKey(Test,on_delete=models.CASCADE)
    date_creation=models.DateTimeField()
    version=models.CharField(max_length=10)
    prix=models.CharField(max_length=255)
    category=models.CharField(max_length=255)
    domaine=models.CharField(max_length=255)
    type=models.CharField(max_length=255)
    date_archive=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titre+" version : "+self.version


class QuizArchive(models.Model):
    author=models.ForeignKey(Archive,on_delete=models.CASCADE)
    question=models.CharField(max_length=255)
    reponse=models.CharField(max_length=255)


class ResultTestArchive(models.Model):
    condidat=models.ForeignKey(Condidat,on_delete=models.CASCADE)
    test_effectue=models.ForeignKey(Archive,on_delete=models.CASCADE)
    score=models.CharField(max_length=20)
    date_effectue=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.condidat.user.username+" test effectue : "+self.test_effectue.titre+" score : "+self.score
