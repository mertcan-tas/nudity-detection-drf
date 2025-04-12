# Nudity Detection DRF 

A Django REST Framework (DRF) API for nude detection in images, using Celery, Redis, and NudeNet.


## Features

- Asynchronous image processing with Celery and Redis
- Nude detection using NudeNet
- Simple JSON responses with detection confidence scores

## Getting Started

### Prerequisites
- Docker ([Installation Guide](https://docs.docker.com/engine/install/))
- Docker Compose ([Installation Guide](https://docs.docker.com/compose/install/))
- Python 3.12+ (Optional, for local development)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/mertcan-tas/nudity-detection-drf.git
cd nudity-detection-drf
```


2. Run the script to generate the .env file:

```
python genenv.py .env-copy > .env
```

3. Running the Project

```bash
docker-compose up --build
```

## API Endpoints

### Authentication

- `POST /api/auth/login/`: Log in to authenticate and obtain a token.
- `POST /api/auth/register/`: Register to create an account and receive an authentication token.

### Detection

- `POST /api/app/detect/`: Submit an image URL for nudity detection.
- `GET /api/app/task/{task-uuid}/`: List all the user's nudity detection requests.
- `GET /api/app/results/`: Retrieve details of a specific detection request.
- `GET /api/app/results/{task-id}/`: Get the result of a specific detection request.

### Using the API

```bash
# Submitting an image URL for nude detection (with token)
curl -X POST http://localhost:8000/api/app/detect/ \
     -H "Authorization: Bearer your_token_here" \
     -H "Content-Type: application/json" \
     -d '{"image_url": "https://picsum.photos/512/512"}'

# Checking result
curl -X GET http://localhost:8000/api/app/task/{task-uuid}/ \
     -H "Authorization: Bearer your_token_here"
```

### Response Format

Task Status:
```json
{
  "task_id": "abd1f15b-75a4-4ced-8b49-df50961e8579",
  "status": "completed",
  "celery_status": "SUCCESS",
  "result": {
    "score": 0.8331286311149597,
    "raw_result": [
      {
        "box": [
          383,
          284,
          138,
          135
        ],
        "class": "FEMALE_BREAST_COVERED",
        "score": 0.7866050004959106
      },
      {
        "box": [
          276,
          329,
          127,
          137
        ],
        "class": "FEMALE_BREAST_COVERED",
        "score": 0.7466063499450684
      },
    ]
  }
}
```
