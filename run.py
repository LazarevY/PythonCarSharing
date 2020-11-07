import app_context
import application.pages.front

flask_app = app_context.app()

if __name__ == '__main__':
    flask_app.run()