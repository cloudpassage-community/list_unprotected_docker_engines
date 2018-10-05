import cloudpassage
import pprint


class Halo(object):
    """Initialize Halo.

    API keys are derived from the HALO_API_KEY and HALO_API_SECRET_KEY
    environment variables.

    Attributes:
        session (cloudpassage.HaloSession): This contains session information
            used for interacting with the ClouddPassage API.
        servers (list): This contains a list of all servers in the account.
        servers_running_docker (list): Servers running Docker daemon (list
        of server IDs).
        unprotected (list): Servers running Docker engine and without
            Docker inspection enabled.
        protected (list): Servers running Docker engine and with Docker
            inspection enabled.
    """
    def __init__(self):
        self.key_manager = cloudpassage.ApiKeyManager()
        self.session = cloudpassage.HaloSession(self.key_manager.key_id,
                                                self.key_manager.secret_key)
        self.servers = self.get_servers()
        self.servers_running_docker = self.get_servers_running_docker()
        self.unprotected = [x for x in self.servers
                            if x["id"] in self.servers_running_docker and
                            x["docker_inspection"] != "Enabled"]
        self.protected = [x for x in self.servers
                          if x["id"] in self.servers_running_docker and
                          x["docker_inspection"] == "Enabled"]

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

    def get_servers(self):
        """Return a current list of servers in Halo."""
        server_obj = cloudpassage.Server(self.session)
        return server_obj.list_all()
