# API Documentation

This document provides detailed information about the ChatApp REST API.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

The API uses session-based authentication. Users must be logged in to access the API endpoints.

### Login

To authenticate, visit `/login/` in your browser and log in with your credentials.

## Endpoints

### Messages

#### List Messages

Get a list of messages for the authenticated user.

**Endpoint:** `GET /api/messages/`

**Query Parameters:**
- `target` (optional): Filter messages by target username

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/messages/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "alice"
      },
      "recipient": {
        "id": 2,
        "username": "bob"
      },
      "timestamp": "2024-01-01T12:00:00Z",
      "body": "Hello, Bob!"
    }
  ]
}
```

#### Get Specific Message

Retrieve a specific message by ID.

**Endpoint:** `GET /api/messages/{id}/`

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "alice"
  },
  "recipient": {
    "id": 2,
    "username": "bob"
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "body": "Hello, Bob!"
}
```

#### Send Message

Send a new message.

**Endpoint:** `POST /api/messages/`

**Request Body:**
```json
{
  "recipient": 2,
  "body": "Hello, how are you?"
}
```

**Response:**
```json
{
  "id": 2,
  "user": {
    "id": 1,
    "username": "alice"
  },
  "recipient": {
    "id": 2,
    "username": "bob"
  },
  "timestamp": "2024-01-01T12:05:00Z",
  "body": "Hello, how are you?"
}
```

**Status Codes:**
- `201 Created`: Message sent successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not authorized to send message

### Users

#### List Users

Get a list of all users except the authenticated user.

**Endpoint:** `GET /api/users/`

**Response:**
```json
[
  {
    "id": 2,
    "username": "bob",
    "first_name": "Bob",
    "last_name": "Smith"
  },
  {
    "id": 3,
    "username": "charlie",
    "first_name": "Charlie",
    "last_name": "Johnson"
  }
]
```

## WebSocket API

### Connection

Connect to the WebSocket endpoint for real-time notifications.

**Endpoint:** `ws://localhost:8000/ws/`

### Message Format

When a new message is sent, the server broadcasts a notification:

```json
{
  "type": "recieve_group_message",
  "message": "123"
}
```

**Fields:**
- `type`: Always "recieve_group_message"
- `message`: The ID of the new message

### Client Implementation

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/');

// Handle connection open
ws.onopen = function() {
    console.log('WebSocket connected');
};

// Handle incoming messages
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'recieve_group_message') {
        // Fetch the new message using the API
        fetchMessage(data.message);
    }
};

// Handle connection close
ws.onclose = function() {
    console.log('WebSocket disconnected');
};

// Handle errors
ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};
```

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message here"
}
```

### Common Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently, there is no rate limiting implemented. In production, consider implementing rate limiting to prevent abuse.

## Pagination

List endpoints use pagination with a default page size of 100 items (or 15 for messages).

**Pagination Parameters:**
- `limit`: Number of results per page
- `offset`: Number of results to skip

**Example:**
```
GET /api/messages/?limit=10&offset=20
```

## Best Practices

1. **Always check authentication** before making API requests
2. **Handle WebSocket reconnection** in case of connection loss
3. **Validate data** before sending to the API
4. **Handle errors gracefully** on the client side
5. **Use HTTPS** in production environments

## Examples

### JavaScript Example

```javascript
// Send a message
async function sendMessage(recipientId, messageBody) {
    const response = await fetch('/api/messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            recipient: recipientId,
            body: messageBody
        })
    });

    if (response.ok) {
        const message = await response.json();
        console.log('Message sent:', message);
    } else {
        console.error('Failed to send message');
    }
}

// Fetch messages with a user
async function fetchMessages(username) {
    const response = await fetch(`/api/messages/?target=${username}`);
    const data = await response.json();
    return data.results;
}
```

### Python Example

```python
import requests

# Login
session = requests.Session()
session.post('http://localhost:8000/login/', {
    'username': 'alice',
    'password': 'password123'
})

# Send a message
response = session.post('http://localhost:8000/api/messages/', json={
    'recipient': 2,
    'body': 'Hello from Python!'
})

if response.status_code == 201:
    message = response.json()
    print(f"Message sent: {message['id']}")
```

## Support

For API-related questions or issues:

1. Check this documentation
2. Review the [codebase](https://github.com/ankur-roy-byte/Chat-bot)
3. Open an [issue](https://github.com/ankur-roy-byte/Chat-bot/issues)
