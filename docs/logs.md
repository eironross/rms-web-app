# Changes on the Services

## 11/10/2025

### user_service
- created init-db for the services
- added /health endpoint to check connection to db
- modify the session files
- added Dockerfile
- added the user_service on the docker-compose.yml
    -   Added the enviroment variables in the compose file
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
- issue on the asynccontextmanager - returns the object "In the route itself <contextlib._AsyncGeneratorContextManager object at 0x7f972b710190>" whil;e using Depends, based on docs Fastapi should be able to handle the generator and context manager
- meaning ```python async with get_db() as db: ``` is implemented
    - try: craeeting the session the crud itself instead from the FastApi Depends 
- greetlet spawn

## 11/14/2025

### user_service
- added the update route and logic
- updated the BaseModel, trying inheritance in the pydantics. Used UserBase for common detials

### issue
- n/a

### resolves
- fixed the async session on the db
- resolved issue on the greenlet spawn using ***relationship(back_populates="profile", lazy="selectin")*** the lazy arg then selectin. not sure why the "joined" is causing an error. For used the "selectin"
    
