# CRM-system

Do uruchomienia aplikacji wymagane jest zainstalowane środowisko virtualenv. Kolejne kroki opisują uruchomienie aplikacji:
1.	env\Scripts\activate – uruchomienie środowiska,
2.	pip install -r requirements.txt – zainstalowanie niezbędnych bibliotek
3.	$env:READ_DOT_ENV_FILE = "True" – zmienne środowiskowe dla trybu debug,
4.	python manage.py runserver – uruchomienie servera,
5.	Aplikację można znaleźć pod adresem: http://127.0.0.1:8000/.

W celu załadowanie danych do aplikacji a następnie przyporządkowania kontaktom ocen należy użyć komend:
1.	python manage.py populate_leads,
2.	python manage.py update_lead_scores.
