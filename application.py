"""List servers running Docker, which do not have docker inspection enabled."""
import argparse
import dlib


def main():
    args = get_args()
    halo = dlib.Halo()
    halo.print_total_server_count()
    servers_running_docker = halo.get_servers_running_docker()
    print("Servers running dockerd: %s" % str(len(servers_running_docker)))
    unprotected = [x for x in halo.servers
                   if x["id"] in servers_running_docker and
                   x["docker_inspection"] != "Enabled"]
    protected = [x for x in halo.servers
                 if x["id"] in servers_running_docker and
                 x["docker_inspection"] == "Enabled"]
    print("Protected servers (%s)" % str(len(protected)))
    print("Unprotected servers (%s):" % str(len(unprotected)))
    for x in unprotected:
        print("Server ID: %s\tServer name: %s\tServer group: %s\t" %
              (x["id"], x["hostname"], x["group_path"]))
    if args.fix:
        ids = [x["id"] for x in unprotected]
        halo.enable_docker_inspection(ids)
    return


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", help="Enable Docker inspection for unprotected workloads.")  # NOQA
    args = parser.parse_args()
    if args.fix:
        print("Will enable Docker inspection on available Docker hosts.")
    else:
        print("Will not make changes in account.")
    return args


if __name__ == "__main__":
    main()
