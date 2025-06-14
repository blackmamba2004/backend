class LinkerService:
    def __init__(self):
        self.base_url = "https://domain"

    def create_verify_link(self, token: str):
        return f"{self.base_url}/verify-email?data={token}"
    
    def create_reset_password_confirm_link(self, token: str):
        return f"{self.base_url}/reset-password/confirm?data={token}"
    
    def create_user_invite_link(self, broker_uuid: str):
       return f"{self.base_url}/users/invite?ref={broker_uuid}"
    