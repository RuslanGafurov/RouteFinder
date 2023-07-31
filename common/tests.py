from http import HTTPStatus


def common_tests(self, response, template):
    """ Проверка статус кода и шаблона """
    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertTemplateUsed(response, template_name=template)
