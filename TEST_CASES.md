# Test Cases

This document lists the main test scenarios used to verify the Box Selection System.

## Product API

| Test Case | Expected Result |
|---|---|
| Create valid product | Product created successfully |
| Get all products | Returns product list |
| Get product by ID | Returns requested product |
| Update product using PUT | Product updated successfully |
| Update product using PATCH | Selected field updated |
| Delete product | Product deleted successfully |
| Create product with invalid dimensions | `400 Bad Request` |
| Get non-existing product | `404 Not Found` |

## Box API

| Test Case | Expected Result |
|---|---|
| Create valid box | Box created successfully |
| Get all boxes | Returns box list |
| Get box by ID | Returns requested box |
| Update box using PUT | Box updated successfully |
| Update box using PATCH | Selected field updated |
| Delete box | Box deleted successfully |
| Create box with invalid dimensions | `400 Bad Request` |
| Get non-existing box | `404 Not Found` |

## Order API

| Test Case | Expected Result |
|---|---|
| Create order | Order created successfully |
| Get all orders | Returns order list |
| Get order by ID | Returns requested order |
| Add product to order | Order item created |
| Add same product again | Existing quantity is increased |
| Add non-existing product | `400 Bad Request` |
| Add zero quantity | `400 Bad Request` |
| Get non-existing order | `404 Not Found` |

## Box Recommendation

| Test Case | Expected Result |
|---|---|
| Recommend box for a valid order | Suitable box returned |
| Recommend box for multiple product quantities | Suitable box calculated using total quantity |
| Recommend box for empty order | `400 Bad Request` |
| Recommend box when no box is suitable | `400 Bad Request` |
| Repeat recommendation request | Cached recommendation can be returned |
| Update order items | Recommendation cache is invalidated |

## Automated Tests

The Django automated test suite covers the application's main functionality.

Latest local test result:

```text
Found 29 test(s).

Ran 29 tests

OK