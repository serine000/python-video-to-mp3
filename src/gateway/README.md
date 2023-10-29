## Building the gateway service

1. Running `docker build .`
2. Tagging the image with `docker tag <SHA256 of image> dockerhub_username/name`

## Kubernetes Ingress
An Ingress Controller for our Kubernetes cluster consists of (1) a load balancer that's going to act as 
the entrypoint of our cluster and (2) a set of rules. Those rule define which request go to which clusters (the service cluster)
we have in our overall Kubernetes cluster.

Nginx will be the load balancer of our ingress in this project.
The `sedmp3converter.com` address will be routed to localhost using the minikube ingress tunnel functionality.
Once we link the url to our localhost using `sudo vim /etc/hosts` tunnel will make sure that when this url is called
it will be mapped to the service cluster mentioned in our ingress which in our case is gateway.