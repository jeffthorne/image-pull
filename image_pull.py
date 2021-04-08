import os
from laceworksdk import LaceworkClient
from docker_registry_client import DockerRegistryClient
lw = LaceworkClient(account=os.getenv('LW_ACCOUNT'), api_key=os.getenv('LW_API_KEY'), api_secret=os.getenv('LW_API_SECRET'))

registry = os.getenv('REGISTRY')
nexus = DockerRegistryClient(f"https://{registry}", verify_ssl=False, username=os.getenv('REGISTRY_USER'), password=os.getenv('REGISTRY_PASSWORD'))
repos = nexus.repositories()

for name, repo in repos.items():
    tags = repo.tags()
    for tag in tags:
        scan_request = lw.vulnerabilities.initiate_container_scan(registry, name, tag)
        print(f"INITIATING SCAN FOR -> REGISTRY[{registry}] IMAGE[{name}]  TAG[{tag}] -> RequestId [{scan_request['data']['RequestId']}]")