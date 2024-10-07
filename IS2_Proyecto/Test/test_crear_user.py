from django.test import TestCase
from login.models import Rol
from django.contrib.auth.models import User

class UserCreationTest(TestCase):
    fixtures = ['IS2_Proyecto/Test/fixtures/roles_fixture.json','IS2_Proyecto/Test/fixtures/permisos_fixture.json']

    def test_user_creation(self):
        # Crear un usuario
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

        # Verificar que el usuario fue creado correctamente
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword123'))