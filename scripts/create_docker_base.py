import yaml

print("YAYA")


with open("../docker-files/final_files/docker-compose-cli.yaml", "w") as f:
    yaml.safe_dump(base_doc, f)
