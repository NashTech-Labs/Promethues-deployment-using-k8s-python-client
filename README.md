
### Install Kubernetes Python Client:

`pip install kubernetes`


# Python client for Promethues-deployment-using-k8s-python-client 



### Authentication to the Kubernetes Python Client in other cluster is done by: 


`configuration.api_key = {"authorization": "Bearer" + bearer_token}`

We will use here the Bearer Token which enable requests to authenticate using an access key.
Give your cluster details in prometheus_stack_deployement.py file:
```
cluster_details={
        "bearer_token":"<Your_cluster_bearer_token>",
        "api_server_endpoint":"<Your_cluster_End_Point>"
    }
```

## Run .py file

`$ python3 prometheus_stack_deployement.py`

# Get the Prometheus server URL by running these commands in the same shell: 

   `$ export POD_NAME=$(kubectl get pods --namespace default -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}")` \
   `$ kubectl --namespace default port-forward $POD_NAME 9090`

# Access prometheus server on  below url

  `http://localhost:9090`



# Get the PushGateway URL by running these commands in the same shell:

  `$ export POD_NAME=$(kubectl get pods --namespace default -l "app=prometheus,component=pushgateway" -o jsonpath="{.items[0].metadata.name}")` \
  `$ kubectl --namespace default port-forward $POD_NAME 9091`

# Access Pushgateway server on  below url

  `http://localhost:9100`
