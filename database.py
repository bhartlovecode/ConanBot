# Handles Database Operations and Connection
from crypt import decrypt, encrypt
import firebase_admin
from decouple import config
from firebase_admin import credentials
from firebase_admin import firestore
from helpers import pretty_print

def dbinit():
  # Use the application default credentials
  cred = credentials.Certificate("creds.json")
  firebase_admin.initialize_app(cred,{
    'projectId': config('PROJECT_ID'),
  })
  #cred = credentials.ApplicationDefault()
  ##firebase_admin.initialize_app(cred, {
  #  'projectId': config('PROJECT_ID'),
  #})

def chkown(name, requester):
  db = firestore.client()
  doc = db.collection(u'conan_servers').document(str(name))

  server = doc.get()
  if server.exists:
    values = server.to_dict()
    if values["owner"] == str(requester):
      return True
    return False

def dbread():
  db = firestore.client()

  servers = db.collection(u'conan_servers')
  docs = servers.stream()
  
  output = ""
  for doc in docs:
    values = doc.to_dict()
    sorted_values=sorted(values.keys(), key=lambda x:x.lower())
    for key in sorted_values:
      if(key == "ip" or key == "password"):
        values[key] = decrypt(values[key])
    output += pretty_print(values, sorted_values)
  return output

def dbadd(name, ip, password, user):
  db = firestore.client()
  doc_ref = db.collection(u'conan_servers').document(str(name))
  doc_ref.set({
    u'owner': str(user),
    u'ip': bytes(ip),
    u'password': bytes(password),
    u'name': str(name)
  })

def dbget(name):
  db = firestore.client()
  doc = db.collection(u'conan_servers').document(str(name))

  values = {}
  server = doc.get()
  sorted_values = []
  if server.exists:
    values = server.to_dict()
    sorted_values=sorted(values.keys(), key=lambda x:x.lower())
    output = ""
    for key in sorted_values:
      if(key == "ip" or key == "password"):
        values[key] = decrypt(values[key])
    output += pretty_print(values, sorted_values)
    return True, output, values, sorted_values
  else:
    output = "This server does not exist!"
    return False, output, values, sorted_values

def dbdelete(name, requester):
  db = firestore.client()
  if (chkown(name, requester)):
    db.collection(u'conan_servers').document(str(name)).delete()
    return True
  return False


def dbupdate(name, args):
  db = firestore.client()

  doc = db.collection(u'conan_servers').document(str(name))
  server = doc.get()

  if server.exists:
    for arg in vars(args):
      if str(getattr(args, arg)) != None:
        if (str(getattr(args, arg)) == "ip" or str(getattr(args, arg)) == "password"):
          encMessage = encrypt(str(getattr(args, arg)))
          print(encMessage)
          doc.update({str(arg): encMessage})
        else:
          doc.update({str(arg): str(getattr(args, arg))})


  



