from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import BASE_DE_DATOS

class Join:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.band_id = data["band_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create_join(cls, user_id, band_id):
        query = """
            INSERT INTO joins (user_id, band_id)
            VALUES (%(user_id)s, %(band_id)s);
        """
        data = {
            'user_id': user_id,
            'band_id': band_id
        }
        join_id = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        return join_id

    @classmethod
    def get_joins_by_user(cls, user_id):
        query = """
            SELECT *
            FROM joins
            WHERE user_id = %(user_id)s;
        """
        data = {
            'user_id': user_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        joins = []
        for row in result:
            join = Join(row)
            joins.append(join)
        return joins

    @classmethod
    def get_joins_by_band(cls, band_id):
        query = """
            SELECT *
            FROM joins
            WHERE band_id = %(band_id)s;
        """
        data = {
            'band_id': band_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        joins = []
        for row in result:
            join = Join(row)
            joins.append(join)
        return joins

    @classmethod
    def get_joins_by_band_id(cls, band_id):
        from flask_app.models.model_users import User
        query = """
            SELECT users.*
            FROM users
            JOIN joins ON joins.user_id = users.id
            WHERE joins.band_id = %(band_id)s;
        """
        data = {
            'band_id': band_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        joins = []
        for row in result:
            join = User(row)
            joins.append(join)
        return joins
    
    @classmethod
    def is_joined(cls, user_id, band_id):
        query = """
            SELECT *
            FROM joins
            WHERE user_id = %(user_id)s AND band_id = %(band_id)s;
        """
        data = {
            'user_id': user_id,
            'band_id': band_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        return len(result) > 0
    
    @classmethod
    def remove_join(cls, user_id, band_id):
        query = """
            DELETE FROM joins
            WHERE user_id = %(user_id)s AND band_id = %(band_id)s;
        """
        data = {
            'user_id': user_id,
            'band_id': band_id
        }
        connectToMySQL(BASE_DE_DATOS).query_db(query, data)