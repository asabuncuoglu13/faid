import pkg_resources
import prettytable
import pandas as pd

def get_pkg_license(pkg):
    try:
        lines = pkg.get_metadata_lines('METADATA')
    except:
        lines = pkg.get_metadata_lines('PKG-INFO')

    for line in lines:
        if line.startswith('License:'):
            return line[9:]
    return '(License not found)'

def print_packages_and_licenses():
    t = prettytable.PrettyTable(['Package', 'License'])
    packages = []
    licenses = []
    
    for pkg in sorted(pkg_resources.working_set, key=lambda x: str(x).lower()):
        package_name = str(pkg)
        license_name = get_pkg_license(pkg)
        t.add_row((package_name, license_name))
        packages.append(package_name)
        licenses.append(license_name)
    
    print(t)
    
    # Create a DataFrame and save to Excel
    df = pd.DataFrame({'Package': packages, 'License': licenses})
    df.to_excel('./docs/package_info.xlsx', index=False)

if __name__ == "__main__":
    print_packages_and_licenses()