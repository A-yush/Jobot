#fb_jokebot views.py
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
import json,requests,random,re

#constants
PAGE_ACCESS_TOKEN="EAAID2VtwGVIBAMOTBywyEL6ZAHjUoGntTikOGwsetAmvmqoCcnaHc0ZCfAZAaN7sQcRQvM6pGZCD1B2AlpVUaBeP8VFm61moyjoXih09bFeWlsV5KtBVyBBaznFZAaOKZBb4rijT31lZAoYXxIj5fZCmlyZBcPtunO7swQwqATgL9GAZDZD"
VERIFY_TOKEN="654321"

#joke dictionary

QA = { "A little girl kicks a soccer ball. It goes 10 feet and comes back to her. How is this possible?":"gravity", 
         "A is the father of B. But B is not the son of A. How’s that possible?":"daughter",
         "How can a man go eight days without sleep?":"night",
         "Some months have 31 days, others have 30 days. How many have 28 days?":"all",
         "What goes up and down  but still remains in the same place?":"stairs",
         "What gets wetter & wetter the more it dries?":"towel"}
seq=('hy','hello','heya','hey','hi')
greet="hey sisi sup wanna play? Ill ask you 3 questions. U in?"
dict=dict.fromkeys(seq,greet)

#choice=random.choice(list(QA.keys()))
#print (choice)
#print (QA.get(choice))




#ques="1. What is  "
#print(str(dict))

#jokes={**jokes,**dict}

#pprint (str(jokes))



# Create your views here.
class jokeview(generic.View):
 ques=random.choice(list(QA.keys()))
 ans=QA.get(ques)
 count=0


 def get(self,request,*args,**kwargs):
  if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
   return HttpResponse(self.request.GET['hub.challenge'])
  else:
   return HttpResponse('Error,invalid token')
    


 @method_decorator(csrf_exempt)
 #csrf_exempt
 def dispatch(self,request,*args,**kwargs):
  return generic.View.dispatch(self,request,*args,**kwargs)

 #post function to handle Fb messages
 def post(self,request,*args,**kwargs):
    #converts the text payload into python dictionary
  incoming_mssgs=json.loads(self.request.body.decode('utf-8'))
    #fb recommends going through every entry since they might send 
    #multiple mssgs in a single call during high load
  for entry in incoming_mssgs['entry']:
   for message in entry['messaging']:
            #check to make sure that received call is a message call
    if 'message' in message:
     #print message to terminal
     pprint(message)
     msg=message['message']['text']
     post_facebook_message(message['sender']['id'],msg,jokeview.ques,jokeview.ans)    
   return HttpResponse()



# This function should be outside the BotsView class
def post_facebook_message(fbid, recevied_message,ques,ans):    
    #remove all punctuations, lowercase the text and split it based on space\
    joke_text=''
    tokens=re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split() 
    flag=None
    for token in tokens: 
     if token in dict:
      joke_text=dict[token]
      break
     list1=['sure','definitely','yeah','yes','yup']
     if token in list1:
      joke_text=ques
       #post_response_message(fbid,joke_text)
      break
     elif token == ans:
        #joke_text="thats correct"
        #print ("the value of flag is: %d"%flag)
      jokeview.ques=random.choice(list(QA.keys()))
      answer=jokeview.ques
      jokeview.ans=QA.get(answer)
      joke_text="correct answer. The next question is: \n"+ jokeview.ques
      jokeview.count+=1
      print (jokeview.count)
      if jokeview.count >=3:
       joke_text="correct answer. Congrats you passed"
      break
     elif token != ans:
      joke_text="wrong ans. I will repeat the question \n"+ques
      break
     #print(flag)
    post_response_message(fbid,joke_text)

def post_response_message(fbid,joke_text):
 post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    #if ans == ques:
 response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
 status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    #pprint(status.json())
