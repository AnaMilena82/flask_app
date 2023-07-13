from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app,BASE_DE_DATOS
from flask_app.models.model_joins import Join
from flask import flash


class Bands:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.band_name = db_data['band_name']
        self.music_genre = db_data['music_genre']
        self.home_city = db_data['home_city']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.joins = []
        self.user_joined = False
    
    @classmethod
    def new_band(cls,data):
        query = """INSERT INTO bands (band_name,music_genre,home_city,user_id)
                 VALUES (%(band_name)s,%(music_genre)s,%(home_city)s, %(user_id)s);"""
        id_band = connectToMySQL(BASE_DE_DATOS).query_db(query,data)
        return id_band

    @classmethod
    def get_allbands_with_user(cls):
        from flask_app.models.model_users import User
        from flask import session
        query = """
                SELECT * 
                FROM bands b JOIN users u
                ON b.user_id = u.id;    
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query)
        list_bands = []
        for row in result:
            band = Bands(row)
            user_id = session.get('id')
            if user_id:
                band.user_joined = Join.is_joined(user_id, band.id)
            data_user = {
                "id":row['u.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at":row['u.created_at'],
                "updated_at":row['u.updated_at']
            }
            user = User(data_user)
            band.user = user
            list_bands.append(band)
        return list_bands

    @classmethod  
    def show_one_band(cls, data):
        query = """
                SELECT * 
                FROM bands 
                WHERE id = %(id)s;     
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        band = Bands (result [0])
        return band

    @classmethod
    def show_one_band_with_user(cls, data):
        from flask_app.models.model_users import User
        query = """
                SELECT * 
                FROM bands b JOIN users u
                ON b.user_id = u.id
                WHERE b.id = %(id)s;     
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        row = result [0]
        band = Bands (row)
        data_user = {
                "id":row['u.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at":row['u.created_at'],
                "updated_at":row['u.updated_at']
        }
        band.user = User(data_user)
        return band 

    @staticmethod
    def get_bands_by_user_id(user_id):
        query = """
                SELECT *
                FROM bands
                WHERE user_id = %(user_id)s;
                """
        data = {
            'user_id': user_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        bands = []
        for row in result:
            band = Bands(row)
            bands.append(band)
        return bands
 

    @staticmethod
    def get_user_id_by_band_id(band_id):
        query = """
                SELECT user_id
                FROM band
                WHERE id = %(band_id)s;
                """
        data = {
            'band_id': band_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        if result:
            return result[0]['user_id']
        return None


    @classmethod
    def delete_one_band(cls, data):
        # query_delete_joins = """
        #     DELETE FROM joins
        #     WHERE band_id = %(id)s;
        # """
        # connectToMySQL(BASE_DE_DATOS).query_db(query_delete_joins, data)

        query = """
                DELETE 
                FROM bands 
                WHERE id = %(id)s;    
                """
        return connectToMySQL(BASE_DE_DATOS).query_db(query, data)

    @classmethod
    def get_one_band(cls, data):
        query = """
            SELECT *
            FROM bands
            WHERE id = %(id)s;
        """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        if len(result) == 0:
            return None
        else:
            return cls(result[0])

    @classmethod  
    def edit_one_band(cls, data):
        query = """
                UPDATE bands 
                SET band_name = %(band_name)s,music_genre = %(music_genre)s,home_city = %(home_city)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        


    @staticmethod
    def validate_band(data):
        is_valid = True

        if len( data['band_name'] ) < 2:
            is_valid = False
            flash( "Band Name should be at least 2 characters.", "error_band_name" )
        if len( data['music_genre'] ) < 2:
            is_valid = False
            flash( "Music Genre should be at least 2 characters long.", "error_music_genre" )
        if len( data['home_city'] ) < 2:
            is_valid = False
            flash( "Home City should be at least 2 characters long.", "error_home_city" )
       
        return is_valid
    
    def get_joins(self):
        from flask_app.models.model_users import User
        query = """
            SELECT u.*
            FROM users AS u
            JOIN joins AS j ON u.id = j.user_id
            WHERE j.band_id = %(band_id)s;
        """
        data = {
            'band_id': self.id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        joins = []
        for row in result:
            join = User(row)
            joins.append(join)
        self.joins = joins

    def add_join(self, user_id):
        from flask_app.models.model_users import User
        query = """
            INSERT INTO joins (user_id, band_id)
            VALUES (%(user_id)s, %(band_id)s);
        """
        data = {
            'user_id': user_id,
            'band_id': self.id
        }
        connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        self.get_joins()

    def remove_join(self, user_id):
        query = """
            DELETE FROM joins
            WHERE user_id = %(user_id)s AND band_id = %(band_id)s;
        """
        data = {
            'user_id': user_id,
            'band_id': self.id
        }
        connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        self.get_joins()

    @classmethod
    def get_allbands_user_joined(cls, user_id):
        from flask_app.models.model_users import User
        query = """
            SELECT b.id, b.band_name, b.music_genre, b.home_city, b.user_id, b.created_at, b.updated_at, u.first_name, u.last_name, u.email, u.password, u.created_at,u.updated_at
            FROM bands AS b
            JOIN joins AS j ON b.id = j.band_id
            JOIN users AS u ON b.user_id = u.id
            WHERE j.user_id = %(user_id)s;
        """
        data = {
            'user_id': user_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        bands = []
        for row in result:
            band_data = {
                'id': row['id'],
                'band_name': row['band_name'],
                'music_genre': row['music_genre'],
                'home_city': row['home_city'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            user_data = {
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            band = Bands(band_data)
            band.user = User(user_data)
            bands.append(band)
        return bands
