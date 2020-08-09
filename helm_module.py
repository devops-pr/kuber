import subprocess

# helm install walmart-hackathon --namespace=walmart-hackathon  --set image.repository=devopspr/walmart_hackathon,image.tag=latest --set container.port=5000,service.type=NodePort  kuber-chart-template
# helm list --all-namespace
# helm status walmart-hackathon --namespace=walmart-hackathon
# helm history walmart-hackathon --namespace=walmart-hackathon
# helm template walmart-hackathon --namespace=walmart-hackathon  --set image.repository=devopspr/walmart_hackathon,image.tag=latest --set container.port=5000,service.type=NodePort,service.port=5000  kuber-chart-template
subprocess.run(["helm", "version"])
