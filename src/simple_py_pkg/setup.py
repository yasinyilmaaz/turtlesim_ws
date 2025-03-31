from setuptools import find_packages, setup

package_name = 'simple_py_pkg'

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
    entry_points={ 
        'console_scripts': [
            "py_node = simple_py_pkg.simple_py_node:main",
            "counter_node = simple_py_pkg.counter_node:main",
            "channel_node = simple_py_pkg.channel_node:main",
            "remote_controller_node = simple_py_pkg.remote_controller_node:main",
            "add_two_ints_server_node = simple_py_pkg.add_two_ints_server:main",
            "add_two_ints_client_node = simple_py_pkg.add_two_ints_client:main",
            "add_two_ints_client_oop_node = simple_py_pkg.add_two_ints_client_oop:main",
            "components_status_publisher_node = simple_py_pkg.components_status_publisher:main",
            "multiply_two_ints_server_node = simple_py_pkg.multiply_two_ints_server:main",
            "multiply_two_ints_client_node = simple_py_pkg.multiply_two_ints_client_oop:main",
            "robot_command_publish = simple_py_pkg.robot_command:main",
        ],
    },
)
