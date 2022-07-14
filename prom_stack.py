from kubernetes import client
import yaml
from os import path



def deploy_clusterrole(cluster_details,manifest_path="/Yaml_manifest/",namespace="default"):
    configuration = client.Configuration()
    configuration.host = cluster_details["api_server_endpoint"]
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + cluster_details["bearer_token"]}
    client.Configuration.set_default(configuration)
    #SERVICE_ACCOUNT
    service_account_api=client.CoreV1Api()
    service_account=("alert-manager-serviceaccount.yaml","kube-metrics-serviceaccount.yaml","node-exporter-serviceaccount.yaml","prometheus-server-serviceaccount.yaml","pushgateway-serviceaccount.yaml")
    for i in service_account:
        service_account_file_path="{}/{}".format(manifest_path,i)
        with open(path.join(path.dirname(__file__), service_account_file_path)) as f:
            yaml_file = yaml.safe_load(f)
            service_account_api.create_namespaced_service_account(body=yaml_file,namespace=namespace)
    #CONFIGMAPS
    k8s_apps_v1  = client.CoreV1Api()
    daemonset=("alert-manager-cm.yaml","prometheus-server-cm.yaml")
    for i in daemonset:
        daemonset_file_path="{}/{}".format(manifest_path,i)
        with open(path.join(path.dirname(__file__), daemonset_file_path)) as f:
            yaml_body= yaml.safe_load(f)
            k8s_apps_v1.create_namespaced_config_map(body=yaml_body,namespace="default")
    #PVC        
    pvc = ("alert-manager-pvc.yaml","prometheus-server-pvc.yaml")
    for i in pvc:
        pvc_file_path="{}/{}".format(manifest_path,i)
        with open(path.join(path.dirname(__file__), pvc_file_path)) as f:
            yaml_file = yaml.safe_load(f)
            k8s_apps_v1.create_namespaced_persistent_volume_claim(body=yaml_file,namespace=namespace)
            
    # CLUSTERROLE
    rbac_api = client.RbacAuthorizationV1Api()
    clusterrole=("alert-manager-clusterrole.yaml","kube-metrics-clusterrole.yaml","prometheus-server-clusterrole.yaml","pushgateway-clusterrole.yaml")
    for i in clusterrole:
        clusterrole_file_path="{}/{}".format(manifest_path,i)
        with open(path.join(path.dirname(__file__), clusterrole_file_path)) as f:
            yaml_file = yaml.safe_load(f)
            rbac_api.create_cluster_role(yaml_file)
    #CLUSTEROLE_BINDING
    clusterrole_binding=("alert-manager-clusterrolebinding.yaml","kube-metrics-clusterrolebinding.yaml","prometheus-server-clusterrolebinding.yaml","pushgateway-clusterrolebinding.yaml")
    for i in clusterrole_binding:
        clusterrolebinding_file_path="{}/{}".format(manifest_path,i)
        with open(path.join(path.dirname(__file__), clusterrolebinding_file_path)) as f:
            yaml_file = yaml.safe_load(f)
            rbac_api.create_cluster_role_binding(yaml_file)
    #SERVICE
    service_client_api = client.CoreV1Api()
    service=("kube-metrics-service.yaml","alert-manager-service.yaml","node-exporter-service.yaml","pushgateway-service.yaml",)
    for i in service:
        service_file_path="{}/{}".format(manifest_path,i)
        with open(path.join(path.dirname(__file__), service_file_path)) as f:
            yaml_file = yaml.safe_load(f)
            service_client_api.create_namespaced_service(body=yaml_file,namespace=namespace)
    # #DAEMONSET
    k8s_apps_v1  = client.AppsV1Api()
    daemonset=("node-exporter-daemonset.yaml")
    daemonset_file_path="{}/{}".format(manifest_path,daemonset)
    with open(path.join(path.dirname(__file__), daemonset_file_path)) as f:
        yaml_body= yaml.safe_load(f)
        k8s_apps_v1.create_namespaced_daemon_set(body=yaml_body,namespace="default")
    
    #DEPLOYMENT
    k8s_apps_v1  = client.AppsV1Api()
    deployment=("kube-metrics-deployment.yaml","alert-manager-deployment.yaml","prometheus-server-deployment.yaml","pushgateway-deployment.yaml")
    for i in deployment:
        deployment_file_path="{}/{}".format(manifest_path,i)
        with open(path.join(path.dirname(__file__), deployment_file_path)) as f:
           yaml_body= yaml.safe_load(f)
           k8s_apps_v1.create_namespaced_deployment(body=yaml_body,namespace="default")

       
if __name__ == '__main__':
    cluster_details={
        "bearer_token": "<YOUR_BEARER_TOKEN>",
        "api_server_endpoint":"<YOUR_API_ENDPOINT>"
    }
    deploy_clusterrole(cluster_details)