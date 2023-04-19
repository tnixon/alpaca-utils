import configparser

def parse_secrets(secrets_file, config_section='DEFAULT'):
    '''
    Parses the given secrets file and returns the configuration parameters
    :param secrets_file: the secrets file name
    :param config_section: the configuration section to return
    :return: the configuration parameters
    '''
    config = configparser.ConfigParser()
    config.read(secrets_file)
    if config_section in config:
        return config[config_section]
    else:
        raise configparser.NoSectionError(f"Config section {config_section} not found in secrets file {secrets_file}!")