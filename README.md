
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e4b1b30fcd784291a315cac009ea40dc)](https://app.codacy.com/app/mkibuuka/store_manager_api_v1?utm_source=github.com&utm_medium=referral&utm_content=mkibuuka/store_manager_api_v1&utm_campaign=Badge_Grade_Settings)
## Store Manager_API_V1  [![Maintainability](https://api.codeclimate.com/v1/badges/c4b765fc3ef09ddeadf2/maintainability)](https://codeclimate.com/github/mkibuuka/store_manager_api_v1/maintainability) [![Build Status](https://travis-ci.org/mkibuuka/store_manager_api_v1.svg?branch=fetch_sale_by_id)](https://travis-ci.org/mkibuuka/store_manager_api_v1) [![Coverage Status](https://coveralls.io/repos/github/mkibuuka/store_manager_api_v1/badge.svg?branch=fetch_sale_by_id)](https://coveralls.io/github/mkibuuka/store_manager_api_v1?branch=fetch_sale_by_id)

Store manager API provides an interface for accessing and manupilating product store resources.

### This repo includes store manager_API_v1 source code files for
* Endpoints
* Unittests/pytests
* Flask
* Product Models
* Sales Models

### Requirements
* Python 3x and up
* Flask python web framework

## Development
```
$ create a python virtualenv
$ source/bin/activate
$ pip install flask
```

### Usage

```python
git clone https://github.com/mkibuuka/store_manager_api_v1.git
cd store_manager_api_v1
python run.py
```

### Product Models:
These represent a product that could be created by a user on the app platform. The product object takes four required attributes (name, category, quantity, price).
A **url** to post a product could take a **POST** request to an endpoint with a format such as **api/v1/products**.

A user product could be formatted and posted as below:
```json
{
	"name": "macbook air",
	"category": "laptops",
	"quantity": 2,
	"price": 1499.0
}
```
And the response could be as below:
```json
{
    "category": "laptops",
    "name": "macbook air",
    "p_id": 1,
    "price": 1499,
    "quantity": 2,
    "sales": 0
}
```
A **url** to fetch a single product by **id** could take a **GET** request to an endpoint with a format such as **api/v1/products/1** and the response could be formatted as below:
```json

    {
    "category": "laptops",
    "name": "macbook air",
    "p_id": 1,
    "price": 1499,
    "quantity": 2,
    "sales": 0
}

```
A **url** to fetch all products could take a **GET** request to an endpoint with a format such as **api/v1/products** and the response could be formatted as below:
```json
{

    "products": [
        {
            "P_id": 1,
            "category": "laptops",
            "name": "macbook air",
            "price": 1499,
            "quantity": 2
        },
        {
            "P_id": 2,
            "category": "Utensils",
            "name": "cups",
            "price": 9,
            "quantity": 10
        }
    ],
    "status": "successful"
}
}
```

### Sale Models:
These represent a sale that could be posted by a user on the app platform. Every sale is mapped to a product/products and an attendant that makes the sale .
A sale could be formatted and posted as below:
```json

{
	"attendant": "michael"
}
```

response:
```json
{
    "attendant": "michael",
    "products": [
        {
            "P_id": 1,
            "category": "laptops",
            "name": "macbook air",
            "price": 1499,
            "quantity": 2
        }
    ],
    "sale_id": 1,
    "status": "successful"
}
```
