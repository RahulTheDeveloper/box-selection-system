# AI-Assisted Box Selection System

A Django REST API that recommends the most suitable shipping box for an ecommerce order based on product dimensions, weight, box capacity, and cost.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Docker
- Docker Compose
- GitHub Actions

## Features

- Product CRUD APIs
- Box CRUD APIs
- Order CRUD APIs
- Add products to orders
- Automatic quantity update for duplicate products
- Shipping box recommendation
- Product dimension rotation support
- Order weight validation
- Order volume validation
- Redis-based recommendation caching
- Cache invalidation when order items change
- Automated Django tests
- GitHub Actions CI
- Dockerized development environment

## Architecture

```text
Client / Postman
       |
       v
Django REST API
       |
       +-----------------> PostgreSQL
       |                   Products
       |                   Boxes
       |                   Orders
       |                   Order Items
       |
       +-----------------> Redis
                           Recommendation Cache



Recommendation Logic

The system calculates the total weight and volume of the order and checks available boxes.

1. Total Order Weight

For each product:

Product Weight × Quantity

The total weight must not exceed the box's maximum supported weight.

2. Total Order Volume

For each product:

Length × Width × Height × Quantity

The total order volume must fit within the box volume.

3. Dimension Fitting

The system checks whether every product can fit inside the box in at least one possible orientation.

For example, a product can be rotated so that its length, width, and height are matched against different box dimensions.

4. Box Selection

Among all suitable boxes, the system selects:

The box with the smallest volume.
If volumes are equal, the box with the lower cost.
API Endpoints
Products
GET     /api/products/
POST    /api/products/
GET     /api/products/<id>/
PUT     /api/products/<id>/
PATCH   /api/products/<id>/
DELETE  /api/products/<id>/
Boxes
GET     /api/boxes/
POST    /api/boxes/
GET     /api/boxes/<id>/
PUT     /api/boxes/<id>/
PATCH   /api/boxes/<id>/
DELETE  /api/boxes/<id>/
Orders
GET     /api/orders/
POST    /api/orders/
GET     /api/orders/<id>/
DELETE  /api/orders/<id>/
POST    /api/orders/<order_id>/items/
Box Recommendation
POST    /api/boxes/recommend/<order_id>/
Example Recommendation Response
{
    "order_id": 1,
    "recommended_box": {
        "id": 1,
        "name": "Small Box",
        "length": "30.00",
        "width": "20.00",
        "height": "10.00",
        "max_weight": "5.00",
        "cost": "50.00"
    }
}
Redis Caching

Recommendation results are cached using Redis.

Cache key:

order_recommendation:<order_id>

Cache duration:

300 seconds

When order items are created or updated, the recommendation cache for that order is invalidated.

Docker Setup

The project uses Docker Compose with three services:

Django
PostgreSQL
Redis

Start the project:

docker compose up --build

Run migrations:

docker compose exec web python manage.py migrate

The API runs at:

http://localhost:8000/
Running Tests

Run the complete test suite:

docker compose exec web python manage.py test

The project includes automated tests for:

Product APIs
Box APIs
Order APIs
Recommendation logic
Recommendation API
Redis caching

Current local test result:

Found 29 test(s).

Ran 29 tests

OK
GitHub Actions

GitHub Actions automatically runs the Django test suite on pushes and pull requests.

The workflow starts:

Push / Pull Request
        |
        v
GitHub Actions
        |
        v
Python 3.12
        |
        +------ PostgreSQL
        |
        +------ Redis
        |
        v
Django Check
        |
        v
Automated Tests
Project Structure
box-selection-system/
│
├── boxes/
│   ├── migrations/
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── orders/
│   ├── migrations/
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── products/
│   ├── migrations/
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── manage.py
├── AI_USAGE.md
└── README.md
Assumptions and Limitations

The current recommendation algorithm uses:

Aggregate order volume
Aggregate order weight
Individual product dimension fitting
Product rotation/orientation

It does not implement full 3D bin-packing optimization for arbitrary placement of multiple products inside a box.

You can view the automated test runs in the [GitHub Actions](../../actions) section of this repository.
Testing and Verification

The project has been tested locally using Django's automated test framework.


GitHub Actions is also configured to run the tests automatically in a clean environment containing PostgreSQL and Redis.

## GitHub Actions

GitHub Actions automatically runs the Django test suite on pushes and pull requests.

You can view the automated test runs in the [GitHub Actions](../../actions) section of this repository.