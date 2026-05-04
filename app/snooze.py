from app.modules import lembretes


def run():
    return lembretes.send_snoozed_agenda_reminders()


if __name__ == "__main__":
    run()
