# Changes on the Services

## 11/25/2025

### auth_service
- added to verify token thru cookies or bearer headers

### user_service
- added dependency to verify tokens from the cookie

### resolves
- n/a

### issues
- observe how can you just the gateways to verify tokens and auth

### lookahead
- test the routes then proceed in integrating the message brokers

## 11/21/2025

### user_service, auth_service
- removed the ```/create_user``` route from the endpoint. added it to the ```auth_services``` as ```/register``` auth will handle the creation of the users

### gateway
- added a dynamic route endpoint to accept any method request then forward to appropriate services 

### resolves
- string manipulation on the forward urls

### issues
- n/a

### lookahead
- build a proper JSON structure for responses
- authentication on the gateway before having access on the services
- add protected routes services, then continue to report_services, crud of the reports


## 11/20/2025

### user_service
- test the protected routes using auth_service to validate tokens in ```/health``` and ```/get-all/```
- added a connection to the auth_service to send request using httpx, note that the url in the containers will be like auth_service:8000/auth/users/me.
- for development purpose the auth will be just simple auth using jwt for now

### auth_services
- added the ```get_current_user``` this will validate the tokens received from the authorization
- added a test route ```/users/me```

### resolves
- uses the httpx to make the containers communicate to each other
- use pyjwt to generate the tokens, since jose is abandoned?

### issues
- n/a

### lookahead
- add protected routes for the user_services, then continue to report_services

## 11/18/2025

### user_service
- restructure folders and imports
- rename folder from ```common``` to ```core```
- added ```init.sh``` to initialize db
- revise creation of db, instead of creating multiple db, just create multiple schemas.
- compose revised

### auth_services
- first init
- created routes, operations for auth

### resolves
- n/a

### issues
- to services to communicate with each other, auth_service and user_service container to container

## 11/15/2025

### user_service
- added the deleted route and logic
- updated the schema model for pydantic
- updade the data model for table that have relationship
    - added ```passive_deletes=True```
    - added ```cascade="all, delete-orphan"```
        - do not used the delete orphan in the xref scenario only use the passive_delete
- added get_user or get_all users routes and logic
    - used Query for Fastapi to paginate the query ```.../users/get-all?page=1&size=10```
    - by default page is 1 then size = 10
    - offset (page - 1) * size
    
### issue
- n/a

### resolves
- n/a


## 11/14/2025

### user_service
- added the update route and logic
- updated the BaseModel, trying inheritance in the pydantics. Used UserBase for common detials

### issue
- n/a

### resolves
- fixed the async session on the db
- resolved issue on the greenlet spawn using ***relationship(back_populates="profile", lazy="selectin")*** the lazy arg then selectin. not sure why the "joined" is causing an error. For used the "selectin"
    
## 11/11/2025

### user_service
Data Models
- added new data models UserRoleModels, UserJunctionModel, UserProfileModel
- added relationship for UserModel & UserProfileModel 1=1
- added relationship for UserRoleModels, UserJunctionModel & UserModel
- added is_active field in the UserModel

DB Session
- removed get_session() function from the db_init.py
- added asynccontextmanager in the get_db() function
- added create_dim_table() function in the db_init.py

API
- added await function for create_dim_table()
    - note: to sync the task use await individually, if you use the asyncio.gather task will run in concurrent

### issue
- issue on the asynccontextmanager - returns the object "In the route itself <contextlib._AsyncGeneratorContextManager object at 0x7f972b710190>" while using Depends, based on docs Fastapi should be able to handle the generator and context manager
- meaning ```python async with get_db() as db: ``` is implemented
    - try: creating the session the crud itself instead from the FastApi Depends 
- greetlet spawn

## 11/10/2025

### user_service
- created init-db for the services
- added /health endpoint to check connection to db
- modify the session files
- added Dockerfile
- added the user_service on the docker-compose.yml
    -   Added the enviroment variables in the compose file


