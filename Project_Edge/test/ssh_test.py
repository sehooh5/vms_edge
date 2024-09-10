import paramiko

# SSH 연결을 위한 정보
hostname = '192.168.0.1'  # 원격 서버 IP 주소
port = 22                 # SSH 포트, 기본적으로 22
username = 'your_username'  # 원격 서버의 사용자 이름
password = 'your_password'  # 사용자 비밀번호

# 파일 경로
docker_config_path = '/etc/docker/daemon.json'
containerd_config_path = '/etc/containerd/config.toml'

# 변경할 내용
new_docker_config = '''
{
    "insecure-registries" : ["192.168.0.4:5000"]
}
'''

new_containerd_config = '''
[plugins."io.containerd.grpc.v1.cri".registry.configs."192.168.0.4:5000".auth]
  username = "sehooh5"
  password = "@Dhtpgh1234"
[plugins."io.containerd.grpc.v1.cri".registry.configs."192.168.0.4:5000".tls]
  insecure_skip_verify = true
'''

def change_file_content(client, file_path, new_content):
    sftp = client.open_sftp()
    with sftp.open(file_path, 'w') as file:
        file.write(new_content)
    sftp.close()

try:
    # SSH 클라이언트 초기화 및 서버에 연결
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)

    # /etc/docker/daemon.json 파일 수정
    change_file_content(client, docker_config_path, new_docker_config)

    # /etc/containerd/config.toml 파일 수정
    change_file_content(client, containerd_config_path, new_containerd_config)

    print("파일이 성공적으로 업데이트되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # SSH 연결 종료
    client.close()
