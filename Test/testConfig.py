from Config.ConfigGetter import config


# noinspection PyPep8Naming
def testConfig():
    """
    :return:
    """
    print(config.db_type)
    print(config.db_name)
    print(config.db_host)
    print(config.db_port)
    print(config.db_password)
    assert isinstance(config.proxy_getter_functions, list)
    print(config.proxy_getter_functions)


if __name__ == '__main__':
    testConfig()
