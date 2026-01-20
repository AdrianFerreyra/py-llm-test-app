from src.application import ApplicationService


class TestApplicationService:
    def test_run_returns_hello_world(self):
        app = ApplicationService()

        result = app.run()

        assert result == "hello world"
