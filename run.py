#############
## Imports ##
#############

import uvicorn  # import uvicorn for running the ASGI application
from app import app  # import the ASGI application object from the app module

#####################
## Run Application ##
#####################
if __name__ == "__main__":

    # listen on all network interfaces (0.0.0.0) and port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
