mkdir backup
# python manage.py dumpdata contacts > backup/contact.json
# python manage.py dumpdata fcm_notification > backup/fcm_notification.json
# python manage.py dumpdata transactions > backup/transactions.json
# python manage.py dumpdata feedback > backup/feedback.json
# python manage.py dumpdata users > backup/users.json


# Uncomment following to restore data
python manage.py loaddata backup/users.json
python manage.py loaddata backup/contact.json
python manage.py loaddata backup/transactions.json
python manage.py loaddata backup/fcm_notification.json
python manage.py loaddata backup/feedback.json
