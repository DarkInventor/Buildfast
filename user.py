from firebase_admin import firestore
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, is_active=True, has_paid=False):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.is_active = is_active
        self.has_paid=has_paid
        
    def get_id(self):   
        return str(self.id)

    # @property
    # def is_active(self):  # getter for is_active property
    #     return self._is_active

    # @is_active.setter
    def is_active(self, value):  
        self._is_active = value
        
    def has_paid(self, value):  
        self.has_paid = value
        
    @staticmethod
    def get(id):
        db = firestore.client()
        user_ref = db.collection('users').document(id)
        user = user_ref.get()
        if user.exists:
            user_data = user.to_dict()
            has_paid = user_data['has_paid'] if 'has_paid' in user_data else False
            return User(user_data['id'], user_data['name'], user_data['email'], user_data['profile_pic'], has_paid=has_paid)
        else:
            return None

    @staticmethod
    def create(id_, name, email, profile_pic, has_paid=False):
        db = firestore.client()
        user_ref = db.collection('users').document(id_)
        user_ref.set({
            'id': id_,
            'name': name,
            'email': email,
            'profile_pic': profile_pic,
            'has_paid': has_paid
        })

    def activate(self):
        db = firestore.client()
        user_ref = db.collection('users').document(self.id)
        user_ref.set({
            'has_paid': True
        }, merge=True)