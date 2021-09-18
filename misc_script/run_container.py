import docker

client = docker.from_env()
print(client.containers.run("hello-world", detach=True))



