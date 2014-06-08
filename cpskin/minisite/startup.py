import ConfigParser
import os.path

from zope.component import provideUtility

from cpskin.minisite.minisite import MinisiteConfig
from cpskin.minisite import logger


def registerMinisites(event):
    CLIENT_HOME = os.environ["CLIENT_HOME"]
    minisites_directory = os.path.join(CLIENT_HOME, 'minisites')
    if os.path.exists(minisites_directory):
        registerMinisitesFromDirectory(minisites_directory)


def registerMinisitesFromDirectory(directory):
    files = os.listdir(directory)
    for filename in files:
        filename = os.path.join(directory, filename)
        if os.path.isfile(filename):
            registerMinisitesFromFile(filename)


def registerMinisitesFromFile(filename):
    config = ConfigParser.RawConfigParser()
    try:
        config.read(filename)
    except ConfigParser.MissingSectionHeaderError:
        return
    logger.debug('Register minisites from file {}'.format(filename))
    for section in config.sections():
        try:
            search_path = config.get(section, 'search_path')
            minisite_url = config.get(section, 'minisite_url')
            minisite = MinisiteConfig(
                main_portal_url=section,
                minisite_url=minisite_url,
                search_path=search_path,
                filename=filename,
            )
            registerMinisite(minisite)
        except KeyError:
            continue


def registerMinisite(config):
    logger.debug('Register minisite at {} for {}'.format(
        config.main_portal_url,
        config.minisite_url,
        )
    )
    provideUtility(
        config,
        name=config.search_path,
    )


def registerMinisitesSetupHandler(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    if context.readDataFile(
            'register_cpskin_minisites.txt') is None:
        return
    from cpskin.minisite import tests

    filename = os.path.join(
        os.path.dirname(tests.__file__),
        'minisites_config.txt',
    )

    registerMinisitesFromFile(filename)
