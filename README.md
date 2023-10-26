## Video to MP3 converter

This tool is built using Python, Kubernetes, RabbitMQ, MongoDB, and MySQL.
All the containers will be handles and "deployed" locally inside a minikube cluster.

More specifically used:
- Python (3.10)
- mysql
- Docker
- Kubernetes
- k9s
- Minikube (Allows us to have a local kubernetes cluster on our own machine to build a microservices 
             architecture locally without having to deploy it to some production server. - This allows you to simulate a multi-node Kubernetes environment 
              in a single-node cluster, which is useful for testing and development.)

File functions:
- init.sql: Create a user and database and assign user to that database.

## How it works:
- Clients will query requests from outside our Kubernetes cluster where our distributed system resides via our system's gateway.
- The gateway service is going to be the entry-point of our application which will receive requests from the client and communicate with
    the necessary internal services to fulfil the client's request.
- The gateway is also where we define the application's functionalities and what the client can request from it. Here we define the endpoints
  of these functionalities.
- We allow clients to submit requests to be processed by our system even if it's placed within a private network by using an authentication service
  to validate the credentials we give to them.
- Basic authentication is having the client provide their credentials in the header field of their request 
  in the form authorization basic credentials `base64(username:password)`. If these credentials are found in our database, we return a Json Web Token (JWT)
  to the client which they will use for subsequent request to our gateway.
- A JWT is composed of 2 formatted strings and a signature which consists of 3 parts, each part being base64 encoded. All 3 parts are merged together 
  separated by a single dot.
- The first part is a key value pair containing the signing algorithm and the type of token (in this case, a JWT). The second part contains the user's data
  (claims). The last part of the token is the signature which is created by taking the base64 encoded header the encoded payload and our private key
 and signing them using the signing algorithm.
- The goal of giving the client a JWT is to make sure that their incoming request contains a JWT that was signed with our private key and our signing algorithm.
    This also helps us determine the client's access level (e.g. an admin claim can be true or false).