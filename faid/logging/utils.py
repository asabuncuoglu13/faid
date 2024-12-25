import sys
import pkg_resources
import os

def get_imported_libraries():
    # Get all imported modules
    imported_modules = [m.__name__ for m in sys.modules.values() if m]
    # include only modules that are not in the standard library
    imported_modules = [m for m in imported_modules if m not in sys.builtin_module_names]
    # remove module submodules
    imported_modules = [m.split('.')[0] for m in imported_modules]
    # remove duplicates
    imported_modules = list(set(imported_modules))
    
    # Get the version of each imported module if available
    modules_with_versions = {}
    for module_name in imported_modules:
        # if module_name does not start with _
        if module_name.startswith('_'):
            continue
        try:
            version = pkg_resources.get_distribution(module_name).version
            modules_with_versions[module_name] = version
        except pkg_resources.DistributionNotFound:
            pass
    
    return sorted(modules_with_versions.items())

def get_package_licenses():
    import importlib.metadata
    root = os.getcwd()
    with open(os.path.join(root, 'requirements.txt'), 'r') as f:
        packages = f.read().splitlines()
        packages = [pkg.split('==')[0] for pkg in packages if pkg]
        try:
            licenses = []
            for package in packages:
                metadata = importlib.metadata.metadata(package)
                license = metadata.get('License')
                if not license:
                    license = metadata.get('Classifier', [])
                    license_info = [line for line in license if line.startswith('License')]
                    license = license_info[0] if license_info else 'License information not found'
                licenses.append((package, license))
        except importlib.metadata.PackageNotFoundError:
            licenses.append((package, "Package not found")) 
    return licenses
