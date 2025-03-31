from setuptools import find_packages, setup

package_name = 'turtlesim_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yasin',
    maintainer_email='yasin@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    # node değişken olarak tanımlandı
    entry_points={
        'console_scripts': [
            "vel_contoller = turtlesim_py_pkg.vel_controller:main",
            "go_to_loc = turtlesim_py_pkg.go_to_loc:main",
            "spawn_turtle = turtlesim_py_pkg.spawn_turtle:main"
        ],
    },
)
