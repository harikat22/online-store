# Online Store - Flask + MySQL + Docker + Kubernetes

## Run Locally

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

Open:
http://localhost:5000


## Docker (MySQL running locally on your system)

docker build -t store-app .

docker run -p 5000:5000 ^
  -e DB_HOST=host.docker.internal ^
  -e DB_USER=root ^
  -e DB_PASSWORD=root ^
  store-app

Open:
http://localhost:5000


## Kubernetes (Minikube)

minikube start

cd /path/to/onlinestore
eval $(minikube docker-env)
docker build -t store-app .

cd k8s
kubectl apply -f .

kubectl get pods

minikube service store-service