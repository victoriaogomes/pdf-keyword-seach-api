from kink import inject
from opensearchpy import OpenSearch

from configs.env.env_settings import EnvSettings


@inject
class OpenSearchClient:
    LOG_ERROR_CONNECTING = "Error creating OpenSearch client: {}"

    def __init__(self, env_settings: EnvSettings):
        try:
            self.client = OpenSearch(
                hosts=[{'host': env_settings.open_search_host, 'port': env_settings.open_search_port}],
                # http_auth=('user', 'password'),
                use_ssl=False,
                verify_certs=True,
                ssl_assert_hostname=False,
                ssl_show_warn=False
            )
        except Exception as e:
            print(self.LOG_ERROR_CONNECTING.format(e))
