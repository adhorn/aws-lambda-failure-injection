from chaos_lambda import inject_exception
from . import TestBase, ignore_warnings
import unittest


@inject_exception
def handler_with_exception(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }


@inject_exception(exception_type=ValueError)
def handler_with_exception_arg(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }


@inject_exception(exception_type=TypeError, exception_msg='foobar')
def handler_with_exception_arg_2(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }


class TestExceptionMethods(TestBase):

    @ignore_warnings
    def setUp(self):
        self.ssm_client.put_parameter(
            Value="{ \"delay\": 400, \"isEnabled\": true, \"error_code\": 404, \"exception_msg\": \"I FAILED\", \"rate\": 1 }",
            Name='test.config',
            Type='String',
            Overwrite=True
        )

    @ignore_warnings
    def test_get_exception(self):
        with self.assertRaises(Exception):
            handler_with_exception('foo', 'bar')

    @ignore_warnings
    def test_get_exception_arg(self):
        with self.assertRaises(ValueError):
            handler_with_exception_arg('foo', 'bar')

    @ignore_warnings
    def test_handler_with_exception_arg_2(self):
        with self.assertRaises(TypeError):
            handler_with_exception_arg_2('foo', 'bar')


class TestExceptionMethodslowrate(TestBase):

    @ignore_warnings
    def setUp(self):
        self.ssm_client.put_parameter(
            Value="{ \"delay\": 400, \"isEnabled\": true, \"error_code\": 404, \"exception_msg\": \"I FAILED\", \"rate\": 0.0000001 }",
            Name='test.config',
            Type='String',
            Overwrite=True
        )

    @ignore_warnings
    def test_get_statuscode(self):
        handler_with_exception('foo', 'bar')
        self.assert_(True)


class TestExceptionMethodsnotenabled(TestBase):

    @ignore_warnings
    def setUp(self):
        self.ssm_client.put_parameter(
            Value="{ \"delay\": 400, \"isEnabled\": false, \"error_code\": 404, \"exception_msg\": \"I FAILED\", \"rate\": 1 }",
            Name='test.config',
            Type='String',
            Overwrite=True
        )

    @ignore_warnings
    def test_get_statuscode(self):
        handler_with_exception('foo', 'bar')
        self.assert_(True)

    @ignore_warnings
    def test_handler_with_exception_arg_2(self):
        handler_with_exception_arg_2('foo', 'bar')
        self.assert_(True)


if __name__ == '__main__':
    unittest.main()
