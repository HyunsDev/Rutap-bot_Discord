class Settings:
    def __init__(self):
        self.token = "" # 봇의 토큰을 적어주세요.
        self.prefix = "/" # 봇의 접두사를 적어주세요. 두글자 이상으로 할 시, main.py 전체를 수정하셔야 합니다. 경고의 경우 main.py에서 수동으로 수정 해 주세요.
        self.owner_id = "" # 봇 관리자의 아이디를 적어주세요.
        self.log_file = "msg_log" # 채팅 로그를 입력할 파일을 입력하세요. >>해당 파일이 존재해야 합니다<<
        self.version = "" # 봇의 버전을 적어주세요.
        # 이 아래는 아직 준비중입니다.
        self.sql_ip = ""
        self.sql_id = ""
        self.sql_pw = ""
        self.sql_db = ""
