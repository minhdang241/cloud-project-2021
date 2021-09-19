# How to run

## Run docker

```
# 1. Install docker

# 2. Build image
docker build -t mindang241/cloud-2021-backend .

# 3. Run docker-compose
docker compose up
```

## Run local

Refer to (https://docs.conda.io/en/latest/miniconda.html#linux-installers) to set up conda.

```
# 1. Create or use exist virtual environment using conda
conda create --name cloud python=3.7
or
conda activate slsops 

# 2. Install requirements.txt 
pip install -r requirements.txt

# 3. Install torch
pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

# 4. Install transformer
pip install sentence-transformers

# 5. Run the main.py to start the backend
python app/main.py

```

**Note:** To run the project, we need .env file

# Features

Endpoint documentation is available in `/docs` or `/redoc` (eg. `https://backend.slsops.athenka.com/docs`)

# Authentication

Auth scheme: HTTPBearer

Token is verified using Amazon Cognito.

There are two roles: User and Admin

# Codebase Structure

```
.   
├── app  
│   ├── api                 // API-related folder
│   │   ├── dependencies    // service layer - including application business logic. Group by web features which each is located in a seperate file
│   │   ├── endpoints       // controller layer - listing endpoints. Group by web features which each is located in a seperate file
│   │   └── errors          // error handler. Definition of returned message when error occurs
│   ├── core                // application configs and env parameters
│   ├── crud                // data access layer - CRUD files to interact with DB
│   │   ├── crud_base.py    // base crud methods: get by id, get by multiple fields, update, create, delete, 
│   │   └── ... some custom crud files    // CRUD files for each specific DB entity
│   ├── db                  // DB-related folders: setup and schemas
│   │   ├── postgres        // entity layer - Postgres set up and table schemas 
│   │   └── setup_hbase.py  // Hbase connection pool set up
│   ├── resources           // util functions and constants  
│   ├── schemas             // pydantic schemas 
│   │   ├── crud_postgres   // create and update schemas for Postgres entities
│   │   ├── k8s             // k8s-related folder
│   │   │   ├── env         // env var schema to input into K8s container
│   │   │   └── job         // schema to input into method that creates K8S job
│   │   └── others          // DTO specified for each feature. Store request body inputted to and response model returned from endpoints  
│   └── main.py             // FastAPI application creation and configuration
├── env                     
│   ├── .env                // hidden env file
│   └── env.example         // example env variables 
├── tests                   // folder contains test files (not yet available)
├── .dockerignore      
├── .gitignore
├── .isort.cfg              // import sort config
├── .pre-commit-config.yaml // precommit config
├── .pylintrc               // pylint config
├── docker-compose.yaml  
├── Dockerfile  
├── entrypoint.sh           // file to run in container
├── logging.ini             // logging config           
├── postgres_schema.sql     // database schema
├── pytest.ini              // file setup pytest  
├── README.md  
└── requirements.txt        // necessary packages

```

# Development instruction

## API writing flow

**0. Create necessary files/folders for new feature**

- In folder `app/api/endpoint`, create a file with the feature name to store list of endpoints
- In folder `app/api/dependencies`, also create a file with the feature name to write application logic
- In file `app/api/api.py`, add route definition which references to created endpoint file
- (Optional) In folder `app/schemas`, create a folder with the feature name to store request and response model (DTO)

**1. Write endpoint definition**

- In _endpoint_ file (`app/api/endpoints/<feature_name>`), declare endpoint stuffs such as request path, params or body,
  response model and dependencies
  (authentication, database, ...). An endpoint should call a same-name method in its corresponding _dependencies_ file
- In _dependencies_ file (`app/api/dependencies/<feature_name>`), methods contain business logic. These methods access
  DB by calling CRUD methods in _crud_ file

**2. Write CRUD methods**

Each CRUD class corresponds to a table entity.

To inherit CRUD base class, we need 3 things: table model class (declared in `app/db/postgres/models.py`), creat and
update schema class (declared in _`app/schemas/crud_postgres`_)

There are two ways to define a CRUD class:

- If does not need to custom methods, define CRUD class directly in `app/crud/__init__.py`
- If need to custom methods, create a separate file named `crud_<entity_name>` and define your CRUD class in it. Then,
  import CRUD class in `app/crud/__init__.py` for easier access.

**Note:** the create and update schema defines which fields/variables are required or optional when creating or updating
an entity record

**3. Write request, response model for endpoints (if needed)**

- Write request body model in `app/schemas/<feature_name>/request.py`
- Write response model in `app/schemas/<feature_name>/response.py`

These models should be imported in its corresponding _endpoint_ and _dependencies_ file

## Database update flow (to be updated...)

**1. Modify entities**

- table model: go to `app/db/postgres/models.py`
- type: go to `app/db/postgres/type.py`

**2. Migrate database ??**

....

**Note:** Postgres table name and id are auto generated based on the model class name. By default, table name
is `<model_name>s`, table id is `<model_lowercase_name>_id`
For example, model class named "Comment" --> table name "Comments", table id "comment_id"

# Code convention

### utils vs dependencies vs crud methods

- utils: general-purpose function, does not interact with crud methods
- dependencies: contains logic flow, interact with crud methods
- crud methods: directly access to database (query, update, etc)

# ER Diagram

To be updated

# Libraries

- pydantic: a validation and parsing library which maps your data to a Python class.
