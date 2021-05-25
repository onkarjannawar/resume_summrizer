from django.shortcuts import render
from .models import myuploadfile
from django.http import HttpResponse
import spacy
import os
import fitz
import re
import tools


# Create your views here.
def resume_view(request):
    return render(request,'resume\home.html')

def send_files(request):
    if request.method=="POST":
        myfile=request.FILES.getlist("uploadfoles")
        if (len(myfile))==0:
            return render(request,'resume/resumenotselected.html')

        else:    
            for f in myfile:
                myuploadfile(myfiles=f).save()
               
                return render(request,'resume/result.html')

def return_home_view(request):
    return render(request,'resume\home.html')    

def Resume_Summarizer():
  """This function will summarize the resume by making a dictionary which contains labels as key and the corresponding text as 
  values provide a path at the given path vatriable which will be directory where all the resumes are stored"""

  path = r"C:\Users\DELL\Desktop\resume_screener\resume_summarizer\media"  #provide a path where the directory contains all the resume e.g-->"C:\django project\media"  #provide a path where the directory contains all the resume e.g-->"C:\django project\media"
  summary = {"NAME":"","EMAIL":"","LOCATION":"","SKILLS":"","DEGREE":"","COMPANIES WORKED AT":"","DESIGNATION":""}
  model = spacy.load(r"C:\Users\DELL\Desktop\resume_screener\resume_summarizer\resume\resume_model")
  file_1 = [os.path.join(path,x) for x in os.listdir(path)]
  file_2 = [os.path.getmtime(x) for x in file_1]
  file_ = {i:j for i,j in zip(file_1,file_2)}
  file_ = dict(sorted(list(file_.items()),key=lambda x:x[1],reverse=True))
  file_ = list(file_.keys())[0]
  doc = fitz.open(file_)
  text = ""
  for page in doc:
      text = text + str(page.getText())
  tx = " ".join(text.split('\n')) 
  tx = re.sub("[^A-Za-z1-9@.]"," ",tx)
  emails = re.findall(r"[a-zA-Z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", tx)
  emails = "".join(emails)
  tx = re.sub("[^A-Za-z]"," ",tx)

  try: 
    doc = model(tx)
    summary["EMAIL"] = emails
    for ent in doc.ents:
      if ent.label_ =="Name":
        summary[ent.label_.upper()] = ent.text        
      elif ent.label_ == "Location":
        summary[ent.label_.upper()] = ent.text
      elif ent.label_ == "Skills":
        summary[ent.label_.upper()] = ent.text
      elif ent.label_ == "Degree":
        summary[ent.label_.upper()] = ent.text
      elif ent.label_ == "Companies worked at":
        summary[ent.label_.upper()] = ent.text
      elif ent.label_ == "Designation":
        summary[ent.label_.upper()] = ent.text
      else:
        pass
  except Exception as e:
      print(e)
      pass
  return summary    

def show_view(request):
    result=Resume_Summarizer()
    return render(request,'resume/show.html',{'results':result})
            
                   
                
        
               
        

       

