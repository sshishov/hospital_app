# Create initial data

from hospital import models as hospital_models
from django.contrib.auth import models as auth_models

EXAMPLE_CHOICES = ('Таблетка', 'Порошок', 'Пилюля', 'Сироп', 'Жидкость')


# Create password
password = hospital_models.User.objects.make_random_password()

# Create example project
project = hospital_models.Project.objects.get_or_create(name='Пример', code='ПРМ')[0]

# Create superusers
for username in ('sergey.shishov', 'aleksey.shishov', 'stas.kostenkov'):
    user = hospital_models.User.objects.filter(username=username).first()
    if not user:
        user = hospital_models.User.objects.create_superuser(
            username=username,
            email='{username}@bombinatech.com'.format(username=username),
            password=password,
        )
        hospital_models.UserProfile.objects.get_or_create(
            user=user,
        )
    user.userprofile.projects.add(project)

# Create doctor and superuser
for username in ('doctor', 'supervisor'):
    user = hospital_models.User.objects.filter(username=username).first()
    if not user:
        user = hospital_models.User.objects.create_user(
            username=username,
            password=password,
        )
        hospital_models.UserProfile.objects.get_or_create(
            user=user,
        )
    user.userprofile.projects.add(project)
    user.groups.add(auth_models.Group.objects.get(name=username.capitalize() + 's'))

# Patient
hospital_models.Patient.objects.get_or_create(
    full_name='Иванов Иван Иванович (пример)',
    defaults={
        'birthday': '2001-01-01',
    },
)

# Create example parameters
hospital_models.Parameter.objects.get_or_create(
    name='Целое',
    defaults={
        'description': 'Целое число',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_INTEGER,
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Целое (обязательное)',
    defaults={
        'description': 'Обязательное целочисленное поле',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_INTEGER,
        'extra_params': {'required': True},
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Строка',
    defaults={
        'description': 'Строковое поле',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_STRING,
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Строка (обязательное)',
    defaults={
        'description': 'Обязательное строковое поле',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_STRING,
        'extra_params': {'required': True},
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Дробное',
    defaults={
        'description': 'Поле для числа с плавающей точкой',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_DECIMAL,
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Дробное (обязательное)',
    defaults={
        'description': 'Обязательное поле для числа с плавающей точкой',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_DECIMAL,
        'extra_params': {'required': True},
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Многострочное',
    defaults={
        'description': 'Многострочное поле',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_MULTISTRING,
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Многострочное (обязательное)',
    defaults={
        'description': 'Обязательное многострочное поле',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_MULTISTRING,
        'extra_params': {'required': True},
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Логическое',
    defaults={
        'description': 'Логическое поле',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_BOOLEAN,
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Логическое (обязательное)',
    defaults={
        'description': 'Обязательное логическое поле',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_BOOLEAN,
        'extra_params': {'required': True},
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Дата',
    defaults={
        'description': 'Поле для даты',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_DATE,
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Дата (обязательное)',
    defaults={
        'description': 'Обязательное поле для даты',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_DATE,
        'extra_params': {'required': True},
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Дата и время',
    defaults={
        'description': 'Поле для даты и времени',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_DATETIME,
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Дата и время (обязательное)',
    defaults={
        'description': 'Обязательное поле для даты и времени',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_DATETIME,
        'extra_params': {'required': True},
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Выбор',
    defaults={
        'description': 'Поле для выбора',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_SELECT,
        'extra_params': {
            'choices': [(x, x) for x in EXAMPLE_CHOICES],
        },
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Выбор (обязательное)',
    defaults={
        'description': 'Обязательное поле для выбора',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_SELECT,
        'extra_params': {
            'required': True,
            'choices': [(x, x) for x in EXAMPLE_CHOICES],
        },
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Мульти Выбор',
    defaults={
        'description': 'Поле выбора нескольких значыений',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_SELECT_MULTIPLE,
        'extra_params': {
            'choices': [(x, x) for x in EXAMPLE_CHOICES],
        },
    },
)
hospital_models.Parameter.objects.get_or_create(
    name='Мульти Выбор (обязательное)',
    defaults={
        'description': 'Обязательное поле выбора нескольких значыений',
        'field_type': hospital_models.Parameter.PARAMETER_TYPE_SELECT_MULTIPLE,
        'extra_params': {
            'required': True,
            'choices': [(x, x) for x in EXAMPLE_CHOICES],
        },
    },
)

for parameter in hospital_models.Parameter.objects.all():
    i = 1
    form = hospital_models.Form.objects.get_or_create(
        name='Форма для {parameter_name}'.format(parameter_name=parameter.name),
        code='ФРМ-{number}'.format(number=i),
        project=project,
    )[0]
    i += 1
    form.fields.add(parameter)

# Forms
form = hospital_models.Form.objects.get_or_create(
    name='Пример Формы ВСЕ ПОЛЯ',
    code='ФРМ-ВСЕ',
    project=project,
)[0]
form.fields.set(hospital_models.Parameter.objects.all())

print('!!! New password for users: {}'.format(password))
