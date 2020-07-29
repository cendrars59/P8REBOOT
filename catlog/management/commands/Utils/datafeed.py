# -*- coding: Utf-8 -*
import requests
from .Params.feedParams import params
import datetime


def feed(domain, request, table, conn):
    """
    Generic Function to feed the masters data -> Store , Brand, Category
    :param conn: object of type connection
    :param domain: object of type string . type of import
    :param request: request to get the master data .Type string
    :param table: Type string . table name to request into
    """
    print("{0} feed is starting!".format(domain))
    query_for_check = ("SELECT COUNT(*) FROM {0} WHERE code=%s".format(table))
    query_for_inserting = ("INSERT INTO {0} (code, name, url, active) VALUES(%s,%s,%s,True)".format(table))
    items_list = request  # Gathering data for api

    for item in items_list:
        cursor_ck = conn.cursor()
        cursor_ck.execute(query_for_check,(item['id'],))
        ckresult = cursor_ck.fetchall()
        cursor_ck.close()
        # if the code doesn't already exit, we can proceed to insert
        if int(ckresult[0][0]) == 0:
            cursor_in = conn.cursor()
            cursor_in.execute(query_for_inserting, (item['id'], item['name'], item['url']))
            conn.commit()
            cursor_in.close()

    print("{0} feed has been done!".format(domain))


def feed_data_set(product_id, items_list, data_set, ref_table, id_ref_table, conn):
    """
    Generic Function to feed the data set used for feed the junction table
    :param conn: object of type connection
    :param product_id: product id. Type integer
    :param data_set: set of data to insert into ref table. Type set
    :param ref_table: destination table to insert. Type string
    :param items_list: potentials items to filter. Type list
    :param id_ref_table: Type integer
    """
    for item in items_list:
        if item != '':
            query_n = ("SELECT {0} FROM {1} WHERE {1}.name = %s".format(id_ref_table, ref_table))
            cursor_n = conn.cursor()
            cursor_n.execute(query_n, (item,))
            ids = cursor_n.fetchall()
            cursor_n.close()
            if len(ids) != 0:
                for Id in ids:
                    data_set.add((product_id, Id[0]))


def insert_into_junction(data_set, table, dest1, dest2, conn):
    """
    Generic Function to feed the junction tables
    :param conn: object of type connection
    :param data_set: object of type set
    :param table: string destination table
    :param dest1: string fields to insert
    :param dest2: string fields to insert
    """
    for item in data_set:
        query_i = ("INSERT INTO {0} ({1},{2}) VALUES(%s,%s)".format(table, dest1, dest2))  # Inserting into the table
        cursor_i = conn.cursor()
        cursor_i.execute(query_i, (item[0], item[1]))
        conn.commit()
        cursor_i.close()


def feed_products(conn):
    """
    Function to feed the products into the database according the category
    :param conn: object of type connection
    """

    product_category = set()
    
    NUMBER_OF_CATEGORIES = 6 

    #Removing the non french categories 
    query = "DELETE FROM catlog_category WHERE code NOT LIKE 'fr:%' "
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()

    query = "DELETE FROM catlog_category WHERE id in (SELECT id FROM catlog_category ORDER BY id desc LIMIT 4900)"
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()

    #Gathering the first 6 french active categories into DB.
    query = "SELECT id, code, name FROM catlog_category WHERE active = True FETCH first 7 rows only"

    cursor = conn.cursor()
    cursor.execute(query)
    categories = cursor.fetchall()
    cursor.close()
    print("The products loading will be performed for {0} active categories".format(str(len(categories))))
    print("products loading is starting. It could take a while...Have a break :-) ")
    for category in categories:
        print('loading products for the category : {}'.format(category[2]))
        payload = {
            "search_terms2": category[2],
            "search_tag": "categories",
            "sort_by": "unique_scans_n",
            "page": 1,
            "page_size": 1000,
            "action": "process",
            "json": 1}
        # API request to gather products according the given payload
        response = requests.get(params['product']['url'], params=payload, headers=params['product']['headers'])
        products = response.json()

        # for each active category, gathering from Open food facts products
        for product in products['products']:

            # verify if the product already exists into the database the search is by open fact food id <-> code into db
            if 'id' in product:
                query_for_check = ("SELECT COUNT(*) FROM catlog_product WHERE catlog_product.code = '{0}'".format(product['id']))
                cursor_ck = conn.cursor()
                cursor_ck.execute(query_for_check)
                ckresult = cursor_ck.fetchall()
                cursor_ck.close()
                # Filtering products having only a valid structure and where the label and id are not empty and 
                # the product doesn't exist into the database and the grade level is not empty.
                if ('brands' in product and 'stores' in product and 'product_name' in product and 'url' in product
                        and 'ingredients_text' in product and 'nutrition_grade_fr' in product and 'quantity' in product and 'image_front_url' in product
                        and product['product_name'] != '' and product['id'] != ''
                        and product['nutrition_grade_fr'] != '' and 'ingredients_text_with_allergens_fr' in product and ckresult[0][0] == 0
                        and product['url'] != None and product['image_front_url'] != '' and product['ingredients_text_with_allergens_fr'] != None):

                    query1 = "INSERT INTO catlog_product (code, name, nutrition_grade_fr, quantity,ingredients_text,ingredients_text_with_allergens_fr, url, url_images, active)" \
                             " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,True)"  # Inserting the product
                    cursor1 = conn.cursor()
                    cursor1.execute(query1, (product['id'], product['product_name'], product['nutrition_grade_fr'], product['quantity'],
                                             product['ingredients_text'], 
                                             product['ingredients_text_with_allergens_fr'],product['url'], product['image_front_url']))
                    conn.commit()
                    cursor1.close()

                    # get the product id just inserted
                    query2 = ("SELECT MAX(id) FROM catlog_product where code = '{0}' ".format(product['id']))
                    cursor2 = conn.cursor()
                    cursor2.execute(query2)
                    product_id = cursor2.fetchall()
                    cursor2.close()

                    # feeding dataset in order to insert into table product has category
                    product_category.add((product_id[0][0], category[0]))


    # inserting into the junction table 
    insert_into_junction(product_category, 'catlog_product_categories', 'product_id', 'category_id', conn)

    print("Products loading is finished")
    

def feed_application(conn):
    """
    Function to feed the database :
    - Category
    - Product
    - and the junction tables
    :param conn: object of type connection
    """
    
    feed(params["category"]["type"], requests.get(params["category"]["url"]).json()['tags'], params["category"]["table"]
         , conn)
    feed_products(conn)
