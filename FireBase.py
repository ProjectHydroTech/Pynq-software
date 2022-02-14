config = {
  'apiKey': "AIzaSyDn4YF2b3DbJbpZBVBObbNA-_MJSxXrag4",
  'authDomain': "pynq-1de4e.firebaseapp.com",
  'databaseURL': "https://pynq-1de4e-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "pynq-1de4e",
  'storageBucket': "pynq-1de4e.appspot.com",
  'messagingSenderId': "152275918965",
  'appId': "1:152275918965:web:e2f9fc792da594d55d183c",
  'measurementId': "G-5EGTQTWWW9",
  'serviceAccount': "key.json"
};
    
firebase = pyrebase.initialize_app(config)

db = firebase.database()
storage = firebase.storage()

auth = firebase.auth()
user = auth.sign_in_with_email_and_password("test@gmail.com", "password")

data = {"name": "Mortimer 'Morty' Smit"}
db.child("users").child("user").set(data)
