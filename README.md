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
To carry out effective Vendor Management, we have created three models :
- Vendor
- Purchase Order
- Historical Performance

### Vendor

The Vendor model represents a vendor in the system. This model captures various attributes of a vendor, including their unique code, name, contact details, address, and performance metrics. Below is a detailed explanation of each field within the Vendor model.

#### Model Fields

- **vendor_code**: 
  - **Type**: `CharField`
  - **Maximum Length**: 100 characters
  - **Attributes**: Unique, Primary Key
  - **Description**: This field stores the unique identifier for the vendor. It serves as the primary key in the database.

- **name**:
  - **Type**: `CharField`
  - **Maximum Length**: 255 characters
  - **Description**: This field stores the name of the vendor.

- **contact_details**:
  - **Type**: `TextField`
  - **Description**: This field stores the contact information of the vendor, such as phone numbers, email addresses, and any other relevant contact information.

- **address**:
  - **Type**: `TextField`
  - **Description**: This field stores the physical address of the vendor.

- **on_time_delivery_rate**:
  - **Type**: `FloatField`
  - **Default Value**: 0.0
  - **Description**: This field represents the percentage of deliveries that the vendor completes on time. This is a performance metric that helps in assessing the reliability of the vendor.

- **quality_rating_avg**:
  - **Type**: `FloatField`
  - **Default Value**: 0.0
  - **Description**: This field stores the average quality rating of the vendor's products or services, based on reviews or assessments.

- **average_response_time**:
  - **Type**: `FloatField`
  - **Default Value**: 0.0
  - **Description**: This field measures the average time it takes for the vendor to respond to inquiries or orders. It is a crucial metric for evaluating the responsiveness of the vendor.

- **fulfillment_rate**:
  - **Type**: `FloatField`
  - **Default Value**: 0.0
  - **Description**: This field represents the percentage of orders that the vendor successfully fulfills. A high fulfillment rate indicates a reliable vendor.

> [!NOTE]
> vendor_code was made into the primary key as it is a unique field.

> [!NOTE]
> Due to some logic error, Vendor instances can only be deleted after the deletion of all Historical Performance entries and Purchase Order entries related to the Vendor

### Purchase Order

The `PurchaseOrder` model is used to represent a purchase order within the system. This model details the purchasing information, including vendor details, ordered items, quantities, and the various states and dates relevant to the lifecycle of the purchase order. Here's an in-depth look at each field in the `PurchaseOrder` model:

#### Model Fields

- **po_number**:
  - **Type**: `CharField`
  - **Maximum Length**: 100 characters
  - **Attributes**: Unique, Primary Key
  - **Description**: This field holds the unique identifier for the purchase order and acts as the primary key in the database.

- **vendor**:
  - **Type**: `ForeignKey`
  - **Related Model**: `Vendor`
  - **Related Name**: `purchase_orders`
  - **On Delete**: `CASCADE`
  - **Description**: This field establishes a relationship to the `Vendor` model, indicating the vendor associated with the purchase order. It is set to delete all associated purchase orders if a vendor is deleted.

- **items**:
  - **Type**: `JSONField`
  - **Description**: This field stores a JSON object containing details about the items in the purchase order, such as item codes, descriptions, and any other relevant item-specific data.

- **quantity**:
  - **Type**: `IntegerField`
  - **Description**: This field indicates the total number of items ordered in this purchase order.

- **status**:
  - **Type**: `CharField`
  - **Maximum Length**: 100 characters
  - **Choices**: `STATUS_CHOICES` (Pending, Incomplete, Complete)
  - **Attributes**: Optional (nullable, blank allowed)
  - **Description**: This field stores the current status of the purchase order, which helps in tracking its progress through different stages.

- **quality_rating**:
  - **Type**: `FloatField`
  - **Attributes**: Optional (nullable, blank allowed)
  - **Description**: This optional field can be used to store a quality rating given to the items received in the purchase order, based on a defined assessment process.

- **order_date**:
  - **Type**: `DateTimeField`
  - **Description**: This field records the date and time when the purchase order was placed.

- **expected_delivery_date**:
  - **Type**: `DateTimeField`
  - **Description**: This field indicates the date and time when the ordered items are expected to be delivered.

- **final_delivery_date**:
  - **Type**: `DateTimeField`
  - **Attributes**: Optional (nullable, blank allowed)
  - **Description**: This field records the actual date and time when the items were delivered. It's optional and can be filled out once the delivery is completed.

- **issue_date**:
  - **Type**: `DateTimeField`
  - **Description**: This field captures the date and time when the purchase order was officially issued to the vendor.

- **acknowledgment_date**:
  - **Type**: `DateTimeField`
  - **Attributes**: Optional (nullable, blank allowed)
  - **Description**: This field is used to record the date and time when the vendor acknowledged the receipt of the purchase order.

> [!NOTE]
> po_number was made into the primary key as it is a unique field.

> [!NOTE]
> The function of delivery_date has been split into 2 fields :
> expected_delivery_date and final_delivery_date
