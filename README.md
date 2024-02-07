# Vendor Machine REST API

## Project Overview

The Vendor Machine project is a REST API designed using Python and Django framework. It simulates the functionality of a vending machine, allowing users with different roles to interact with it. Users with a "seller" role can manage products (add, update, remove), while users with a "buyer" role can deposit coins into the machine and make purchases. The vending machine only accepts 5, 10, 20, 50, and 100 cent coins.

## How to Run the Project

Follow these steps to run the project on your local machine:

1. Install [Python 3.11](https://www.python.org/downloads/release/python-3110/). 
2. Create a virtual environment on your machine and activate it.
   ```
   python3 -m venv myenv
   source myenv/bin/activate  # On macOS/Linux
   myenv\Scripts\activate      # On Windows
   ```
4. Install project dependencies by running `pip install -r requirements.txt`.
5. Navigate to the project directory in your terminal.
6. Apply database migrations by running `python manage.py makemigrations` followed by `python manage.py migrate`.
7. Create a superuser account by running `python manage.py createsuperuser` and follow the prompts to create a user with administrative privileges.
8. Start the development server by running `python manage.py runserver`.

## Endpoints

- **POST /api/signup/**: Allows users to sign up.
- **POST /api/auth/login/**: Allows users to log in.
- **POST /api/auth/logout/**: Allows users to log out.
- **GET /api/products/**: Lists all products and allows creation of a new product.
- **GET /api/products/product_id/**: Retrieves the product with id=product_id, allowing modification or deletion.
- **POST /api/deposit/**: Allows users to make a deposit.
- **POST /api/reset/**: Allows users to reset the deposit.
- **POST /api/buy/**: Allows users to buy a product.
- **GET /api/users/**: Lists all users.

## Usage

- Sign up for an account using the `/api/signup/` endpoint.
- Log in using the `/api/auth/login/` endpoint.
- Use the appropriate endpoints based on your role:
  - Sellers: Manage products using `/api/products/` endpoints.
  - Buyers: Deposit coins, buy products, and reset deposit using `/api/deposit/`, `/api/buy/`, and `/api/reset/` endpoints respectively.
- Log out using the `/api/auth/logout/` endpoint when done.


**Note:** Ensure that you have appropriate permissions to access certain endpoints based on your role (seller/buyer).
