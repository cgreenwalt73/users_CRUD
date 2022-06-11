# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the user table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    
    # class method to obtain a single user
    @classmethod
    def get_one_user_by_id(cls, id):
        data= {'id' : id}
        query="""
        SELECT * FROM users 
        WHERE id = %(id)s
        ;"""
        result= connectToMySQL('users_schema').query_db(query, data)
        return cls(result[0])

    # class method to obtain user id by email
    @classmethod
    def get_id_by_email(cls, email):
        query="""
        SELECT id FROM users
        WHERE email = %(email)s
        ;"""
        result= connectToMySQL('users_schema').query_db(query, email)
        return result[0]

    # create a class method to append users to the db
    @classmethod
    def save(cls, new_user):
        query='INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, NOW(), NOW() );'
        # a dictionary containing the new users info is passed to the db
        return connectToMySQL('users_schema').query_db(query, new_user)
    
    # create a class method to update existing users
    @classmethod
    def update_by_id(cls, user_data):
        query="""
        UPDATE users
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        return connectToMySQL('users_schema').query_db(query, user_data)

    # create a class method to delete users from the db
    @classmethod
    def delete_by_id(cls, id):
        data= {'id' : id}
        query="""
        DELETE FROM users 
        WHERE users.id= %(id)s
        ;"""
        return connectToMySQL('users_schema').query_db(query, data)
