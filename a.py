import pkg_resources

# Iterate over all installed packages
for dist in pkg_resources.working_set:
    print(dist.project_name, dist.version)
