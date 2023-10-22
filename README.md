## Video to MP3 converter

This tool is built using Python, Kubernetes, RabbitMQ, MongoDB, and MySQL.
All the containers will be handles and "deployed" locally inside a minikube cluster.

More specifically used:
- Python (3.10)
- mysql
- Docker
- Kubernetes
- k9s
- Minikube (Allows us to have a kubernetes cluster on our own machine to build a microservices 
             architecture locally without having to deploy it to some production server)

File functions:
- init.sql: Create a user and database and assign user to that database.