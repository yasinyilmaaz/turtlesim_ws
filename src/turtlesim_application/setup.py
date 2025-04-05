from setuptools import find_packages, setup

package_name = 'turtlesim_application'

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
    maintainer_email='yasn.866644@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "draw_triangle_node = turtlesim_application.draw_triangle:main",
            "triangle_corner_node = turtlesim_application.triangle_corner:main",
            "spawn_turtles_node = turtlesim_application.spawn_turtle:main",
            "go_to_location_node = turtlesim_application.go_to_loc:main",
            'coordinate_info_server_node = turtlesim_application.coordinate_info_server:main',
            "coordinate_draw_node = turtlesim_application.coordinate_draw:main",
        ],
    },
)
