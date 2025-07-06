broker = "Брокер"
admin = "Админ"
user = "Клиент"

auth = "Авторизация"
reg = "Регистрация"
serv = "Сервисы"

log_broker_tags = f"{auth} | {broker}"
log_broker_user_tags = f"{auth} | {user} / {broker} / {admin}"
log_user_tags = f"{auth} | {user}"

reg_broker_tags = f"{reg} | {broker}"
reg_broker_user_tags = f"{reg} | {user} / {broker}"
reg_user_tags = f"{reg} | {user}"

serv_admin_tags = f"{serv} | {admin}"
serv_common_tags = f"{serv} | {admin} / {broker} / {user}"