import unittest
from unittest.mock import patch

from app.callbacks import agenda_callback, academia_callback, remedios_callback, tarefas_callback
from app.callbacks.router import dispatch


class CallbackTest(unittest.TestCase):
    def test_router_dispatches_every_supported_prefix(self):
        cases = (
            ("prep_ok", remedios_callback),
            ("tarefa_cama", tarefas_callback),
            ("academia_done", academia_callback),
            ("agenda_hoje", agenda_callback),
            ("aniversarios_hoje", agenda_callback),
            ("rotina_tarefas_painel", agenda_callback),
            ("menu_ajuda", agenda_callback),
        )

        for data, module in cases:
            callback = {"id": "cb1", "data": data}
            with self.subTest(data=data):
                with patch.object(module, "handle", return_value={"ok": True}) as handle:
                    result = dispatch(callback)

                self.assertTrue(result["ok"])
                handle.assert_called_once_with(callback)

    def test_agenda_callbacks_answer_and_call_expected_sender(self):
        cases = (
            ("agenda_hoje", "send_daily_events"),
            ("agenda_semana", "send_week_events"),
            ("aniversarios_hoje", "send_daily_birthdays"),
            ("aniversarios_semana", "send_week_birthdays"),
        )

        for data, sender_name in cases:
            with self.subTest(data=data):
                with patch.object(agenda_callback, "_answer_safe") as answer:
                    with patch.object(agenda_callback.lembretes, sender_name) as sender:
                        result = agenda_callback.handle({"id": "cb1", "data": data})

                self.assertTrue(result["ok"])
                answer.assert_called_once_with("cb1")
                sender.assert_called_once()

    def test_unknown_callback_answers_when_possible(self):
        with patch("app.callbacks.router.answer_callback_query", return_value={"ok": True}) as answer:
            result = dispatch({"id": "cb1", "data": "sem_rota"})

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "unhandled_callback")
        answer.assert_called_once_with("cb1", "ação não reconhecida")

    def test_unknown_task_does_not_save_state(self):
        with patch("app.callbacks.tarefas_callback.load_state", return_value={"cama": "❌"}):
            with patch("app.callbacks.tarefas_callback.save_state") as save_state:
                with patch("app.callbacks.tarefas_callback.answer_callback_query", return_value={"ok": True}):
                    result = tarefas_callback.handle({"id": "cb1", "data": "tarefa_invalida"})

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "unknown_task")
        save_state.assert_not_called()

    def test_task_callback_without_chat_does_not_crash_or_edit(self):
        with patch.object(tarefas_callback, "GROUP_ID", None):
            with patch.object(tarefas_callback, "load_state", return_value={"cama": "❌"}):
                with patch.object(tarefas_callback, "save_state"):
                    with patch.object(tarefas_callback, "answer_callback_query", return_value={"ok": True}):
                        with patch.object(tarefas_callback, "edit_message") as edit_message:
                            result = tarefas_callback.handle(
                                {"id": "cb1", "data": "tarefa_cama", "message": {"message_id": 10}}
                            )

        self.assertTrue(result["ok"])
        self.assertFalse(result["edited"])
        edit_message.assert_not_called()

    def test_remedio_callback_without_chat_does_not_crash_or_edit(self):
        state = {"status_hoje": "pendente", "estoque_atual": 1}
        with patch.object(remedios_callback, "GROUP_ID", None):
            with patch.object(remedios_callback, "load_state", return_value=state):
                with patch.object(remedios_callback, "save_state"):
                    with patch.object(remedios_callback, "answer_callback_query", return_value={"ok": True}):
                        with patch.object(remedios_callback, "edit_message") as edit_message:
                            result = remedios_callback.handle(
                                {"id": "cb1", "data": "prep_ok", "message": {"message_id": 10}}
                            )

        self.assertTrue(result["ok"])
        self.assertFalse(result["edited"])
        edit_message.assert_not_called()

    def test_academia_callback_without_chat_does_not_crash_or_edit(self):
        state = {"proximo_treino": "treino a", "streak": 0, "ultimo_treino": "-"}
        with patch.object(academia_callback, "GROUP_ID", None):
            with patch.object(academia_callback, "load_state", return_value=state):
                with patch.object(academia_callback, "save_state"):
                    with patch.object(academia_callback, "answer_callback_query", return_value={"ok": True}):
                        with patch.object(academia_callback, "edit_message") as edit_message:
                            result = academia_callback.handle(
                                {"id": "cb1", "data": "academia_done", "message": {"message_id": 10}}
                            )

        self.assertTrue(result["ok"])
        self.assertFalse(result["edited"])
        edit_message.assert_not_called()


if __name__ == "__main__":
    unittest.main()
