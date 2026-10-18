from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Pregunta, Opcion


class EncuestaViewsTests(TestCase):
    def setUp(self):
        self.pregunta = Pregunta.objects.create(
            pregunta_texto="¿Cuál es tu lenguaje favorito?",
            pub_date=timezone.now()
        )
        self.opcion1 = Opcion.objects.create(pregunta=self.pregunta, opcion_texto="Python", votos=0)
        self.opcion2 = Opcion.objects.create(pregunta=self.pregunta, opcion_texto="JavaScript", votos=0)

    def test_index_view(self):
        response = self.client.get(reverse('encuesta:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Cuál es tu lenguaje favorito?")

    def test_detalle_view(self):
        response = self.client.get(reverse('encuesta:detalle', args=[self.pregunta.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")
        self.assertContains(response, "JavaScript")

    def test_votar_view(self):
        response = self.client.post(
            reverse('encuesta:votar', args=[self.pregunta.id]),
            {'opcion': self.opcion1.id}
        )
        self.assertEqual(response.status_code, 200)
        self.opcion1.refresh_from_db()
        self.assertEqual(self.opcion1.votos, 1)
        self.assertContains(response, "1 voto")
