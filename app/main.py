from app.modules import lembretes
from app.config import BOT_TOKEN, GROUP_ID


def validate_runtime_config():
    return {
        "has_token": bool(BOT_TOKEN),
        "has_group_id": bool(GROUP_ID),
    }


def run():
    cfg = validate_runtime_config()
    print(f"[totodile] config has_token={cfg['has_token']} has_group_id={cfg['has_group_id']}")
    return lembretes.send_due_reminders()


if __name__ == "__main__":
    run()
