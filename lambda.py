import requests
import json
import boto3
import os

client = boto3.client('ssm')
response = client.get_parameter(Name='k8s-bear-token')
url = os.environ['k8s_cluster']+'/apis/apps/v1/namespaces/default/deployments/example-deployment'
headers = {'Content-Type':'application/json', 'Authorization':'Bearer '+response['Parameter']['Value']}
body = {
	"apiVersion": "apps/v1",
	"kind": "Deployment",
	"metadata": {
		"name": "example-deployment",
		"labels": {
			"app": "example"
		}
	},
	"spec": {
		"replicas": 2,
		"selector": {
			"matchLabels": {
				"app": "example"
			}
		},
		"template": {
			"metadata": {
				"labels": {
					"app": "example"
				}
			},
			"spec": {
				"containers": [
					{
						"name": "example-container",
						"image": "busybox",
						"command": [
							"sh",
							"-c",
							"echo ${DEMO_GREETING} && sleep 3600"
						],
						"env": [
							{
								"name": "DEMO_GREETING",
								"value": "Another Hello Kubernetes!"
							}
						]
					}
				]
			}
		}
	}
}
body = json.dumps(body)

def lambda_handler(event, context):
	r = requests.put(url, headers=headers,verify=False,data=body)
	return r