# United Nations of Hair

Welcome to the United Nations of Hair, an e-commerce platform dedicated to providing high-quality hair products and services. This repository contains the backend codebase for the platform.

## Table of Contents

* [Project Overview](#project-overview)
* [Installation](#installation)
* [Configuration](#configuration)
* [API Endpoints](#api-endpoints)

  * [User Management](#user-management)
  * [Product Management](#product-management)
  * [Order Management](#order-management)
* [Testing](#testing)
* [Contributing](#contributing)
* [License](#license)

## Project Overview

The United Nations of Hair platform offers a range of services, including:

* **User Management**: Registration, authentication, and profile management.
* **Product Management**: Browsing and purchasing hair products.
* **Order Management**: Order placement, tracking, and history.

## Installation

### Prerequisites

Ensure you have the following installed:

* Python 3.8 or higher
* pip
* virtualenv

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/kimzee23/UnitedNationsofhair.git
   cd UnitedNationsofhair
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   Create a `.env` file in the root directory and add the following:

   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=your_database_url
   ```

5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser to access the admin panel:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

   The application should now be running at `http://127.0.0.1:8000/`.

## Configuration

The project uses environment variables for configuration. Ensure the following are set in your `.env` file:

* `SECRET_KEY`: A secret key for cryptographic operations.
* `DEBUG`: Set to `True` for development, `False` for production.
* `ALLOWED_HOSTS`: A comma-separated list of allowed host/domain names.
* `DATABASE_URL`: The URL of your database.

## API Endpoints

### User Management

The Users module supports multiple account types:

* **CUSTOMER** – Default user role.
* **VENDOR** – Can sell products; must be verified.
* **INFLUENCER** – Optional role for promotion or marketing.
* **SUPER_ADMIN** – Full administrative control.

It also manages:

* User registration, login, and profile updates.
* Role upgrade applications.
* Vendor verification with certificates and government ID.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kimzee23/UnitedNationsofhair.git
cd UnitedNationsofhair
```

2. Set up a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the server:

```bash
python manage.py runserver
```

---

## Configuration

Add environment variables in a `.env` file:

```text
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your_database_url
```

---

## User Model Fields

| Field                | Type    | Description                                       |
| -------------------- | ------- | ------------------------------------------------- |
| `id`                 | UUID    | Primary key                                       |
| `username`           | String  | Unique username                                   |
| `email`              | Email   | Unique email, login identifier                    |
| `phone`              | String  | Optional, unique                                  |
| `role`               | Enum    | `CUSTOMER`, `VENDOR`, `INFLUENCER`, `SUPER_ADMIN` |
| `country`            | String  | Optional user country                             |
| `application_role`   | Enum    | Role requested for upgrade                        |
| `application_status` | Enum    | `NONE`, `PENDING`, `APPROVED`, `REJECTED`         |
| `business_name`      | String  | Optional, for vendors                             |
| `gov_id_number`      | String  | Optional, for vendors                             |
| `certificate`        | File    | Vendor certificate                                |
| `is_verified`        | Boolean | Verification status                               |

---

## API Endpoints

### Register User

* **Endpoint**: `POST /api/users/register/`
* **Request Body**:

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "phone": "08012345678",
  "country": "Nigeria"
}
```

* **Response**:

```json
{
  "id": "uuid_here",
  "username": "john_doe",
  "email": "john@example.com",
  "role": "CUSTOMER",
  "is_verified": false
}
```

---

### Login User

* **Endpoint**: `POST /api/users/login/`
* **Request Body**:

```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

* **Response**:

```json
{
  "token": "jwt_token_here",
  "user": {
    "id": "uuid_here",
    "username": "john_doe",
    "email": "john@example.com",
    "role": "CUSTOMER"
  }
}
```

---

### Get Profile

* **Endpoint**: `GET /api/users/profile/`
* **Headers**: `Authorization: Bearer <token>`
* **Response**:

```json
{
  "id": "uuid_here",
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "08012345678",
  "role": "CUSTOMER",
  "country": "Nigeria",
  "application_role": null,
  "application_status": "NONE",
  "is_verified": false
}
```

---

### Update Profile

* **Endpoint**: `PATCH /api/users/profile/`
* **Request Body**: (Optional fields)

```json
{
  "phone": "08098765432",
  "country": "Nigeria"
}
```

* **Response**: Updated profile JSON.

---

### Request Vendor Role Upgrade

* **Endpoint**: `POST /api/users/apply-vendor/`
* **Request Body**:

```json
{
  "application_role": "VENDOR",
  "business_name": "Hair Haven",
  "gov_id_number": "A1234567",
  "certificate": "file_upload_here"
}
```

* **Response**:

```json
{
  "message": "Your application has been submitted",
  "application_status": "PENDING"
}
```

---

### Admin Approve/Reject Application

* **Endpoint**: `PATCH /api/users/application/{user_id}/`
* **Request Body**:

```json
{
  "application_status": "APPROVED"
}
```

* **Response**:

```json
{
  "id": "uuid_here",
  "application_status": "APPROVED",
  "role": "VENDOR",
  "is_verified": true
}
```

---

## Testing

Run Django tests:

```bash
python manage.py test users
```

This includes tests for:

* Registration
* Login
* Profile retrieval & update
* Vendor role application and approval


* **List Products**

  Vendors to create and manage brands and products.

Categorization of products into hierarchical categories.

Users to compare products.

Admins to verify products.


Run the server:

python manage.py runserver

Models
Brand

Fields:

id (UUID)

name (string)

description (text, optional)

website (URL, optional)

country (string, optional)

owner (ForeignKey to User with role VENDOR)

Category

Fields:

id (UUID)

name (string)

slug (unique)

parent (self-referencing, optional)

Product

Fields:

id (UUID)

name (string)

price (decimal, optional)

stock (integer, default 0)

affiliate_url (URL, optional)

image_url (URL, optional)

image (file, optional)

is_verified (boolean)

brand (ForeignKey to Brand)

category (ForeignKey to Category, optional)

created_at / updated_at

ProductCompare

Fields:

user (ForeignKey to User)

products (ManyToManyField to Product)

created_at (timestamp)

API Endpoints
Brands

List Brands: GET /api/brands/

Create Brand: POST /api/brands/ (Vendors only)

{
  "name": "Hair Haven",
  "description": "Premium hair brand",
  "website": "https://hairhaven.com",
  "country": "Nigeria"
}


Brand Details: GET /api/brands/{id}/

Update Brand: PATCH /api/brands/{id}/

Delete Brand: DELETE /api/brands/{id}/

Categories

List Categories: GET /api/categories/

Create Category: POST /api/categories/

{
  "name": "Bundles",
  "slug": "bundles",
  "parent": "parent_category_id_optional"
}


Category Details: GET /api/categories/{id}/

Update Category: PATCH /api/categories/{id}/

Delete Category: DELETE /api/categories/{id}/

Products

List Products: GET /api/products/

Create Product: POST /api/products/ (Vendor only)

{
  "name": "Brazilian Hair Bundle",
  "price": 100,
  "stock": 50,
  "brand": "brand_id",
  "category": "category_id",
  "affiliate_url": "https://affiliate.com",
  "image_url": "https://image.com/image.jpg"
}


Product Details: GET /api/products/{id}/

Update Product: PATCH /api/products/{id}/

Delete Product: DELETE /api/products/{id}/

Verify Product: PATCH /api/products/{id}/verify (Admin only)

Product Comparison

Compare Products: POST /api/products/compare/

{
  "user": "user_id",
  "products": ["product_id1", "product_id2"]
}


Get User Comparisons: GET /api/products/compare/?user=user_id

Testing

Run the module tests:

python manage.py test products


Tests include:
### Order Management

* **Create Order**

  * `POST /api/orders/`

  * Request Body:

    ```json
    {
      "product_ids": [1, 2],
      "shipping_address": "123 Main St, Lagos, Nigeria"
    }
    ```

  * Response:

    ```json
    {
      "id": 1,
      "status": "pending",
      "total_price": 220
    }
    ```

* **Order Status**

  * `GET /api/orders/{id}/`
  * Response:

    ```json
    {
      "id": 1,
      "status": "pending",
      "total_price": 220,
      "shipping_address": "123 Main St, Lagos, Nigeria"
    }
    ```

## Testing

To run the project's tests:

1. Ensure your virtual environment is activated.
2. Run the tests:

   ```bash
   python manage.py test
   ```

   This will execute all the test cases and provide a summary of the results.

## Contributing

We welcome contributions to improve the United Nations of Hair platform. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Ensure tests are added or updated as necessary.
5. Submit a pull request detailing your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

If you need further assistance or have questions about the API endpoints, feel free to open an issue in the repository.


