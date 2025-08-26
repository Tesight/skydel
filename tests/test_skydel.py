from importlib.metadata import metadata


def test_skydel_metadata():
    pkg_metadata = metadata("skydel")

    print("====== Package Info ======")
    print(pkg_metadata)


def test_skydel_import():
    print("====== Package Import ======")
    import skydel

    print("Current Package Version", skydel.__version__)

    from skydel.skydelsdx import commands

    print(f"Current API Version: {commands.ApiVersion}")


def test_skydel_runtime():
    from skydel.skydelsdx.commandfactory import createCommand

    cmd = createCommand(
        '{"CmdName": "New", "CmdUuid": "uuid", "DiscardCurrentConfig": true, "LoadDefaultConfig": true}'
    )
    print(cmd)


if __name__ == "__main__":
    test_skydel_metadata()
    test_skydel_import()
    test_skydel_runtime()