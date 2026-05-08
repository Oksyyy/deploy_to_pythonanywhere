# Program for CRUD operations on service providers and their services using Flask and SQLite
# Author: Oksana Abrosimova

import sqlite3
import dbconfig as cfg
from os import path

class ServiceProviderDAO:
    connection=""
    cursor =''
    database=   ''
    
    def __init__(self):
        self.database = cfg.sqlite['database']

    def get_cursor(self): 
        ROOT = path.dirname(path.realpath(__file__))

        self.connection = sqlite3.connect(path.join(ROOT,self.database))
        self.cursor = self.connection.cursor()
        return self.cursor

    def close_all(self):
        self.connection.close()
        #self.cursor.close()

    # PROVIDERS     
    def get_all(self):
        cursor = self.get_cursor()
        sql = """
        select p.id, p.name, p.email, p.phone, p.price_per_hour, p.service_id, s.name as service_name
        from providers p
        join services s on p.service_id = s.id
        """

        cursor.execute(sql)

        results = cursor.fetchall()
        return_array = []
        #print(results)
        for result in results:
            #print(result)
            return_array.append(self.convert_provider_with_service_to_dictionary(result))
        
        self.close_all()
        return return_array

    def find_by_id(self, id):
        cursor = self.get_cursor()
        cursor.execute("select * from providers where id = ?", (id,))
        
        result = cursor.fetchone()

        # Return None if no provider is found with the given id
        if result is None:
            self.close_all()
            return None

        return_value = self.convert_to_dictionary(result)
        self.close_all()
        return return_value

    def create_provider(self, provider):
        cursor = self.get_cursor()
        # Parameterized query to prevent SQL injection
        # https://www.datacamp.com/tutorial/sql-injection?utm_cid=23340058068&utm_aid=192632749329&utm_campaign=230119_1-ps-dscia%7Edsa-tofu%7Esql_2-b2c_3-emea_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na&utm_loc=9040163-&utm_mtd=-c&utm_kw=&utm_source=google&utm_medium=paid_search&utm_content=ps-dscia%7Eemea-en%7Edsa%7Etofu%7Etutorial%7Esql&gad_source=1&gad_campaignid=23340058068&gbraid=0AAAAADQ9WsFnuuYqMT0K3yAVZRgI5NzCC&gclid=CjwKCAjw14zPBhAuEiwAP3-EbxLK_3SM13DIdBbeg3U_zwMI6Lj1vXdORgiD3n3wdRXDegNhq-dqqBoCXOEQAvD_BwE&dc_referrer=https%3A%2F%2Fwww.google.com%2F
        sql = """insert into providers 
             (name,email,phone,price_per_hour,service_id) 
             values (?,?,?,?,?)"""
        values = (
            provider['name'],
            provider['email'],
            provider['phone'],
            provider['price_per_hour'],
            provider['service_id']
        )
        cursor.execute(sql, values)

        self.connection.commit()
        provider["id"] = cursor.lastrowid

        self.close_all()
        return provider


    def update_provider(self, id, provider):
        cursor = self.get_cursor()
        sql = """update providers 
                set name=?, email=?, phone=?, price_per_hour=?, service_id=? 
                where id=?"""
        values = (
            provider['name'],
            provider['email'],
            provider['phone'],
            provider['price_per_hour'],
            provider['service_id'],
            id
        )
        cursor.execute(sql, values)

        self.connection.commit()
        self.close_all()
        
    def delete_provider(self, id):
        cursor = self.get_cursor()
        cursor.execute("delete from providers where id = ?", (id,))

        self.connection.commit()
        self.close_all()
        
        #print("delete done")

    def convert_to_dictionary(self, result_line):
        if result_line is None:
            return None
        att_keys=['id','name','email','phone', "price_per_hour", 'service_id']
        provider = {}
        current_key = 0
        for attrib in result_line:
            provider[att_keys[current_key]] = attrib
            current_key = current_key + 1 
        return provider
    
    # SERVICES
    def get_all_services(self):
        cursor = self.get_cursor()
        sql = "select * from services"
        cursor.execute(sql)
        results = cursor.fetchall()
        return_array = []
        #print(results)
        for result in results:
            #print(result)
            return_array.append(self.convert_service_to_dictionary(result))
        
        self.close_all()
        return return_array
    
    def create_service(self, service):
        cursor = self.get_cursor()
        sql = "insert into services (name) values (?)"
        values = (service['name'],)

        cursor.execute(sql, values)

        self.connection.commit()
        service["id"] = cursor.lastrowid

        self.close_all()
        return service
    
    def convert_service_to_dictionary(self, result_line):
        if result_line is None:
            return None

        return {
            "id": result_line[0],
            "name": result_line[1]
        }
    

    def get_by_service(self, service_id):
        cursor = self.get_cursor()
        sql = """
            select p.id, p.name, p.email, p.phone, p.price_per_hour, p.service_id, s.name as service_name
            from providers p
            join services s on p.service_id = s.id
            where p.service_id = ?
        """
        cursor.execute(sql, (service_id,))
        results = cursor.fetchall()
        return_array = []
        for result in results:
            return_array.append(self.convert_provider_with_service_to_dictionary(result))
        self.close_all()
        return return_array
    
    def convert_provider_with_service_to_dictionary(self, result_line):
        if result_line is None:
            return None

        return {
            "id": result_line[0],
            "name": result_line[1],
            "email": result_line[2],
            "phone": result_line[3],
            "price_per_hour": result_line[4],
            "service_id": result_line[5],
            "service_name": result_line[6]
        }

        
serviceProviderDAO = ServiceProviderDAO()