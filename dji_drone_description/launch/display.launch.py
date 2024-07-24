from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ld = LaunchDescription()

    package_path = FindPackageShare('dji_drone_description')
    default_model = 'mini3'
    default_rviz_config_path = PathJoinSubstitution([package_path, 'config', 'urdf.rviz'])

    # These parameters are maintained for backwards compatibility
    ld.add_action(DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher_gui'))

    ld.add_action(DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                     description='Absolute path to rviz config file'))

    ld.add_action(DeclareLaunchArgument(name='model', default_value=default_model,
                                        description='DJI drone model name'))

    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('urdf_launch'), 'launch', 'display.launch.py']),
        launch_arguments={
            'urdf_package': 'dji_drone_description',
            'urdf_package_path': [PathJoinSubstitution(['urdf', LaunchConfiguration('model')]), '.urdf'],
            'rviz_config': LaunchConfiguration('rvizconfig'),
            'jsp_gui': LaunchConfiguration('gui')}.items()
    ))

    return ld