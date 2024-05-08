# Vendor Management System 

This API offers comprehensive functionality for vendor and purchase order management. It facilitates tasks including vendor creation, updating, and deletion, along with purchase order creation, updating, and acknowledgment.

## Table of Contents
- Requirements
- Authentication
- Models
- Endpoints
- Logic
- Final words

## Requirements
The Vendor Management Application requires the following frameworks:

- Django
- Django REST Framework
- Django Filters

Install them straight from the command using pip:
```sh
pip install django
```
```sh
pip install djangorestframework
```
```sh
pip install django-filter
```

Once installed, make sure to add them to the **INSTALLED_APPS** section of *settings.py* in the project folder.

## Authentication
The API Endpoints are protected through Session Authentication that can be created by creating a Super User and logging in for the session. Then until the user logs out, they can interact with all calls.

![image](https://github.com/SentinelError/Vendor/assets/71810497/c109a561-8f66-403c-8188-4f7f1093ece5)

You can find the above code segment at the bottom of the models.py file.


## Models
