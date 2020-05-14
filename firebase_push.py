from firebase import firebase
firebase = firebase.FirebaseApplication('https://mktrs-7ac29.firebaseio.com/', None)
result = firebase.get('/',None)
print(result['test2'])
# firebase = firebase.FirebaseApplication('https://mktrs-7ac29.firebaseio.com/', None)
new_user = {'Ozgur Vatansever':'person'}

result = firebase.post('/apple', key=new_user)
print(result)
