# Online Store Management System

A modular web-based Online Store Management System developed using Component-Based Software Engineering (CBSE) principles.

The project provides a simple online shopping experience where users can browse and search products, manage favorites, add products to a shopping cart, and complete a simulated payment process.

## Project Overview

The system follows a client-server architecture and separates the application into independent logical components.

The frontend is responsible for the user interface and user interactions, while the backend provides REST API services and communicates with the SQLite database.

The main components of the system are:

* Product Component
* Cart Component
* Payment Component
* Database Component
* REST API Component
* User Interface Component

This modular structure improves separation of responsibilities, maintainability, testability, and future extensibility.

## Technologies

### Frontend

* React
* Vite
* JavaScript
* HTML
* CSS

### Backend

* Python
* Flask
* Flask-CORS
* REST API

### Database

* SQLite

### Testing

* PyTest
* Postman

## Main Features

### Product Management

* View available products
* Search products
* View product information
* Create products through the REST API
* Update products through the REST API
* Delete products through the REST API
* Product validation
* Product images
* Product ratings
* Stock management

The database contains 200 product records used by the application.

### Favorites

Users can add products to their favorites and remove them from the favorites list.

Favorite information is stored in the browser using Local Storage.

### Shopping Cart

Users can:

* Add products to the cart
* View cart items
* Manage product quantities
* View product prices
* View subtotals
* View the total cart amount
* Remove products from the cart

### Simulated Payment

The application includes a simulated payment process.

After a successful payment:

1. The payment record is stored in the database.
2. Product stock quantities are decreased.
3. The shopping cart is cleared.
4. The user is shown a payment success result.

No real payment gateway is connected to the system.

## Project Structure

```text
OnlineStoreManagementSystem/
│
├── backend/
│   ├── components/
│   │   ├── product/
│   │   ├── cart/
│   │   └── payment/
│   │
│   ├── database/
│   ├── routes/
│   ├── tests/
│   ├── venv/
│   ├── app.py
│   └── seed_products.py
│
└── frontend/
    ├── src/
    ├── public/
    ├── package.json
    └── vite.config.js
```

## Backend API

The backend runs on:

```text
http://127.0.0.1:5000
```

The frontend communicates with the backend through REST API endpoints.

Main API operations include:

* Product listing
* Product creation
* Product updating
* Product deletion
* Cart operations
* Payment processing
* Payment records

The API uses standard HTTP methods such as:

* GET
* POST
* PUT
* DELETE

## Database

SQLite is used for persistent data storage.

The main database tables are:

### products

Stores:

* Product ID
* Name
* Description
* Price
* Stock
* Category
* Image URL
* Rating

### cart_items

Stores:

* Cart item ID
* Product ID
* Quantity

### payments

Stores:

* Payment ID
* Total amount
* Payment status
* Creation date

## Installation

### 1. Clone the Repository

```bash
git clone [YOUR_GITHUB_REPOSITORY_URL]
cd OnlineStoreManagementSystem
```

### 2. Backend Setup

Open a terminal in the backend directory:

```bash
cd backend
```

Create and activate a virtual environment if necessary:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install flask flask-cors pytest
```

Start the backend:

```bash
python app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at the address shown by Vite, normally:

```text
http://localhost:5173
```

## Testing

The project uses PyTest for backend testing and Postman for REST API verification.

The tested functionality includes:

* Product creation
* Product retrieval
* Product updating
* Product deletion
* Cart operations
* Payment processing
* Stock updates
* Cart clearing
* Payment records
* Product validation
* Error handling

Postman was used to verify successful and invalid API requests.

## Component-Based Architecture

The general communication flow of the system is:

```text
User
  ↓
React + Vite User Interface
  ↓
Flask REST API
  ↓
┌───────────────┬───────────────┬────────────────┐
│ Product       │ Cart          │ Payment        │
│ Component     │ Component     │ Component      │
└───────────────┴───────────────┴────────────────┘
  ↓
Database Component
  ↓
SQLite Database
```

Each component has a specific responsibility and communicates with other parts of the system through defined interfaces.

## Future Improvements

Possible future improvements include:

* User registration and authentication
* User-specific shopping carts
* Order history
* Product category filtering
* Admin dashboard
* Real payment gateway integration
* Additional payment methods
* Improved security and authentication
* PostgreSQL or MySQL database support
* Automated deployment
* Additional automated tests
* Load and performance testing

## Project Purpose

This project was developed to demonstrate the principles of Component-Based Software Engineering in a practical web application.

The project focuses on:

* Modularity
* Separation of responsibilities
* Encapsulation
* Reusability
* Maintainability
* Testability
* REST-based communication

## License

This project was developed for educational purposes.
