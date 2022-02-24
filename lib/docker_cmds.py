import os
from lib import config, args_helper
def get_docker_compose_file():
    docker_compose_file = (args_helper.is_production() and 'docker-compose-pro.yml') or 'docker-compose.yml'
    return docker_compose_file

def docker_compose_run_cmd(full_tag, args_for_docker=[]):
    uid = os.getuid()
    gid = os.getgid()
    cwd = os.getcwd()
    args = ["docker-compose", '-f', get_docker_compose_file(), "run", "--rm", "--user", f'{uid}:{gid}',
        "-v", f'{cwd}:/app:rw', "-e", "HOME=/app", "-w", "/app"] + args_for_docker + [full_tag]
    return args

def docker_compose_exec_cmd(full_tag, args_for_docker=[]):
    uid = os.getuid()
    gid = os.getgid()
    cwd = os.getcwd()
    args = ["docker-compose", '-f', get_docker_compose_file(), "exec", "--user", f'{uid}:{gid}',
        "-e", "HOME=/app"] + args_for_docker + [full_tag]

    return args

def docker_base_cmd(full_tag, args_for_docker=[]):
    uid = os.getuid()
    gid = os.getgid()
    cwd = os.getcwd()
    args = ["docker", "run", "--rm", "-it","--user", f'{uid}:{gid}',
        "-v", f'{cwd}:/app:rw', "-e", "HOME=/app", "-w", "/app"] + args_for_docker + [full_tag]
    return args

def docker_project_base_cmd(full_tag, prject_dir,args_for_docker=[]):
    uid = os.getuid()
    gid = os.getgid()
    args = ["docker", "run", "--rm", "-it","--user", f'{uid}:{gid}',
        "-v", f'{prject_dir}:/app:rw', "-e", "HOME=/app", "-w", "/app"] + args_for_docker + [full_tag]
    return args


def docker_compose_up_cmd(services=[]):
    if isinstance(services, str):
        services = [services]
    return ['docker-compose', '-f', get_docker_compose_file(), 'up', *services]

def build_image(rails_base_tag, image_tag, project_dir):
    tag = config.get_project_tag(image_tag, project_dir)
    return ['docker', 'build', '-t', tag, project_dir]

