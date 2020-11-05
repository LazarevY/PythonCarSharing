import app_context
import application.front.front

flask_app = app_context.app()

if __name__ == '__main__':
    flask_app.run()