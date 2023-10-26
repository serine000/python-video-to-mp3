## Explanation

What the authentication service does here is authenticate the user logging in to check if their credentials
are present in the database.

The `init.sql` initializes the `auth` database with a `user` table and inserts within it a customer user we created in that script.
Commands used:
- To initialize: `mysql -u root -p < init.sql`
- Access mysql: `mysql -u root -p` [and insert your password]
- Display databases: `show databases;`
- Pick a specific database to work with: `use [database name];`
- Display tables in specific database: `show tables;`

## Building docker image
docker build .

## Deploying service to cluster
0. Make sure docker is running.
1. `cd` into the manifests directory of your service.
2. Upload the service as it is to the kubernetes cluster (`k9s`)
3. deploy it into a minikube (`minikube start`)
4. Check that your minikube pod is running within the kube system namespace
5. `kubectl apply -f ./` for our files to interact with the API to create our service and its corresponding resource.