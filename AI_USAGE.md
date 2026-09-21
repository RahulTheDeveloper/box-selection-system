# AI Usage Documentation

This project was developed with the assistance of AI during the planning, implementation, debugging, documentation, and testing stages.

## 1. AI Tools Used

- ChatGPT

ChatGPT was used as a development assistant for:
- Project architecture and planning
- Django REST API implementation guidance
- Recommendation logic discussion
- Docker and Docker Compose guidance
- Redis caching implementation guidance
- Automated test development
- Debugging errors
- README and project documentation guidance

The final implementation was reviewed and tested before being accepted into the project.

---

## 2. Prompts Used

The AI was used through multiple development-focused conversations.

Examples of tasks given to the AI included:

### Project Planning

The AI was asked to help design a Django-based box selection system for an ecommerce order, including products, boxes, orders, and box recommendation logic.

### Recommendation Logic

The AI was asked to help design logic that considers:

- Product dimensions
- Product weight
- Box dimensions
- Maximum box weight
- Order quantity
- Box volume
- Product rotation/orientation
- Box selection based on suitability and cost

### Redis and Caching

The AI was asked for guidance on implementing Redis caching for box recommendation results and invalidating the cache when order items change.

### Docker

The AI was asked to explain and guide the Dockerfile and Docker Compose setup containing:

- Django
- PostgreSQL
- Redis

### Testing

The AI was asked to help create automated Django tests for:

- Product APIs
- Box APIs
- Order APIs
- Recommendation logic
- Recommendation API
- Redis caching

### Debugging

The AI was also used to help identify and fix implementation issues encountered during development, including missing model imports and test failures.

---

## 3. Accepted AI Output

AI suggestions were reviewed before being used.

Examples of accepted guidance included:

- Separating recommendation logic into `boxes/services.py`
- Using a dedicated recommendation service instead of placing all business logic inside the API view
- Using Redis for recommendation caching
- Using a cache key based on the order ID
- Invalidating recommendation cache when order items change
- Using automated Django tests
- Using GitHub Actions for continuous test execution
- Using Docker Compose for Django, PostgreSQL, and Redis

The final implementation was adapted to the project's actual requirements.

---

## 4. Rejected or Modified AI Output

AI-generated suggestions were not copied blindly.

Some suggestions were modified based on the project's requirements and implementation decisions.

Examples include:

- The recommendation logic was adapted to the assignment's specific box selection requirements.
- The project uses Redis for caching rather than introducing unnecessary background-processing components.
- The recommendation algorithm was kept intentionally simpler than a complete industrial 3D bin-packing solution.
- API and project structure decisions were adjusted while implementing and testing the actual project.
- Documentation was reviewed and modified to accurately describe the final implementation.

---

## 5. Mistakes Made by AI

During development, some AI-generated guidance required correction.

Examples included:

- Missing model imports in views during implementation.
- Some suggested implementation details required adjustment after running the actual code.
- Test failures helped identify cases where the implementation and imports needed correction.
- Documentation suggestions sometimes needed to be aligned with the actual project structure.

These issues were identified through actual development and testing rather than being accepted without verification.

---

## 6. How the Final Code Was Verified

The final implementation was verified using multiple methods.

### Local Testing

The Django automated test suite was executed locally.

Result:

    Found 29 test(s).

    Ran 29 tests

    OK

The test suite covers the main API and recommendation functionality.

### Docker Verification

The application was run using Docker Compose with:

- Django
- PostgreSQL
- Redis

### Redis Verification

Redis caching was tested through the Django application and recommendation endpoint.

### API Verification

The REST APIs were tested using Postman.

### GitHub Actions

GitHub Actions was configured to run:

- Django system checks
- Automated Django tests
- PostgreSQL service
- Redis service

This provides an additional clean-environment verification of the project.

---

## 7. Human Decisions and Validation

AI was used as an assistant during development, but the final implementation was reviewed and validated by the developer.

The final code was:

- Implemented in the project
- Run locally
- Tested through API requests
- Tested using Django automated tests
- Tested with PostgreSQL and Redis
- Verified using Docker
- Configured with GitHub Actions

AI suggestions were treated as guidance rather than automatically trusted output.