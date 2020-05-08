#!/bin/bash

if [[ ! -z $1 ]]; then
  # shellcheck disable=SC2027
  SETTING_MODULE="CS_AppsStore.settings.$1_settings"
  echo "$SETTING_MODULE"
  python manage.py makemigrations --settings="$SETTING_MODULE"
  python manage.py migrate --settings="$SETTING_MODULE"
  python manage.py collectstatic --no-input --settings="$SETTING_MODULE"
  create_superuser() {
    local username=$APPSTORE_DJANGO_USERNAME
  local email=""
    local password=$APPSTORE_DJANGO_PASSWORD
  cat <<EOF | python manage.py shell --settings="$SETTING_MODULE"
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="$username").exists():
    User.objects.create_superuser("$username", "$email", "$password")
else:
    print('User "{}" already exists, not created'.format("$username"))
EOF
}
create_superuser
  python manage.py addingwhitelistedsocialapp --settings="$SETTING_MODULE"
  python manage.py runserver --settings="$SETTING_MODULE" 127.0.0.1:8000
else
  echo "please provide setting module name"
fi
