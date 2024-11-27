# URL Shortener API

A simple Flask-based URL shortener API that allows you to create, read, update, and delete shortened URLs. The API provides endpoints to manage URLs and track the number of times each shortened URL has been accessed.

## Features

- Create shortened URLs with automatically generated short codes
- Retrieve individual and list all shortened URLs
- Update original URLs
- Delete URLs
- Track access counts for each shortened URL
- Timestamps for creation and updates

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| POST | `/urls/` | Create a new shortened URL |
| GET | `/urls/` | List all URLs |
| GET | `/urls/<short_code>` | Get details of a specific URL |
| PATCH | `/urls/<url_id>` | Update an existing URL |
| DELETE | `/urls/<url_id>` | Delete a URL |

## API Usage Examples

### Create a New Short URL
```bash
curl -X POST http://localhost:5000/urls/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very-long-url"}'
```

### Get All URLs
```bash
curl http://localhost:5000/urls/
```

### Get Specific URL Details
```bash
curl http://localhost:5000/urls/abc123
```

### Update URL
```bash
curl -X PATCH http://localhost:5000/urls/1 \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://new-example.com"}'
```

### Delete URL
```bash
curl -X DELETE http://localhost:5000/urls/1
```

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
flask run
```
