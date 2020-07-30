# -*- coding: Utf-8 -*
# Required parameters to perform the feeding of th database

params = {

    'category': {

        'type': 'category',
        'table': 'catlog_category',
        'url': 'https://fr.openfoodfacts.org/products/categories.json'
    },

    'product': {

        'type': 'product',
        'table': 'Product',
        'url': 'https://fr.openfoodfacts.org/cgi/search.pl?',
        'headers': {'User-Agent': 'Cyril-59, Mozilla, Version 1.0'},
    }



}
