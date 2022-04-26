dev:
	@python manage.py runserver localhost:8000

migrate:
	@python manage.py makemigrations
	@python manage.py migrate

admin:
	@python manage.py createsuperuser