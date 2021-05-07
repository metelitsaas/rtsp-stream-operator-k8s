#### Run minikube
```
minikube start --vm-driver=virtualbox --cpus 2
eval $(minikube docker-env)
```

#### Deploy RTSP Stream Operator
```
DOCKER_BUILDKIT=1 docker build \
    --tag rtsp-stream-operator:0.1.0 \
    --file docker/rtsp-stream-operator.dockerfile . 

kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/authorization/service_account.yaml
kubectl apply -f kubernetes/authorization/cluster_role.yaml
kubectl apply -f kubernetes/authorization/cluster_role_binding.yaml
kubectl apply -f kubernetes/deployment.yaml
```