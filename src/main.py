'''import os

from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path
from django.core.wsgi import get_wsgi_application

# Configuration minimale de Django
settings.configure(
    DEBUG=True,
    SECRET_KEY='a-very-secret-key',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
    ],
)
def home(request):
    return HttpResponse("Hello, Django!")

urlpatterns = [
    path('', home),
]

application = get_wsgi_application()

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
'''

import sys
from PyQt6.QtWidgets import QApplication, QWidget
from ui.software_ui import Ui_sofware_ui

class MainWindow(QWidget) :
    def __init__(self):
        super().__init__()

        self.ui = Ui_sofware_ui()
        self.ui.setupUi(self)

        from pages.home_page import HomePage
        self.homepage = HomePage(self)

        # from pages.login_page import
        #self.login =

        # from pages.sign_in_page import
        #self.signin =

        # from pages.event_page import
        #self.event =

        # from pages.task_page import
        #self.task =

        #initialisation à la première page du logiciel : homepage
        self.ui.pages_logiciel.setCurrentIndex(0)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    sofware_ui = MainWindow()
    sofware_ui.show()
    sys.exit(app.exec())
