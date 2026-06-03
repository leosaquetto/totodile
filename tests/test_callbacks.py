import unittest
from unittest.mock import patch

from app.callbacks.router import dispatch
from app.callbacks import tarefas_callback


class CallbackTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
