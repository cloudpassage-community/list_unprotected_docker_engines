import cloudpassage
import requests
import pprint


class Halo(object):
    """Initialize Halo.

    API keys are derived from the HALO_API_KEY and HALO_API_SECRET_KEY
    environment variables.

    Attributes:
        session (cloudpassage.HaloSession): This contains session information
            used for interacting with the ClouddPassage API.
        servers (list): This contains a list of all servers in the account.
    """
    def __init__(self):
        self.key_manager = cloudpassage.ApiKeyManager()
        self.session = cloudpassage.HaloSession(self.key_manager.key_id,
                                                self.key_manager.secret_key)
        self.servers = []
        self.refresh_servers()

    def enable_docker_inspection(self, ids):
        """Enable Docker inspection for list of Halo server IDs."""
        payload = {"ids": ids, "data": {"docker_inspection": True}}
        http_helper = cloudpassage.HttpHelper(self.session)
        response = http_helper.post("/v1/servers/batch", payload)
        pprint.pprint(response)

    def get_servers_running_docker(self):
        """Return a list of IDs for all servers running `dockerd`."""
        h_h = cloudpassage.HttpHelper(self.session)
        url = "/v2/servers?process_name=dockerd"
        retval = [x["id"] for x in h_h.get_paginated(url, "servers", 99)]
        return retval

    def print_total_server_count(self):
        print("Total servers: %s" % len(self.servers))

    def refresh_servers(self):
        """Refresh self.servers with a current list of servers in Halo."""
        server_obj = cloudpassage.Server(self.session)
        self.servers = server_obj.list_all()

    def server_is_running_docker(self, bundle, retry=False):
        """Return server ID if server is running Docker, else None.

        Args:
            bundle (list): Position 0 is occupied by a cloudpassage.HaloSession
                object. Position 1 is occupied by a string containing serverID.
        """
        server_obj = cloudpassage.Server(bundle[0])
        try:
            if [x for x in server_obj.list_processes(bundle[1])
                    if x["process_name"] == "dockerd"]:
                return bundle[1]
            else:
                return None
        except requests.exceptions.ConnectionError as e:
            print(e)
            if retry:
                print("Already retried this server, moving on.")
                return None
        self.server_is_running_docker(bundle, retry=True)
