import subprocess
import sys
from importlib.metadata import PackageNotFoundError, metadata
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def manage_skydel_package():
    try:
        install_result = subprocess.run(
            [sys.executable, "-m", "pip", "install", Path(__file__).parent.parent],
            capture_output=True,
            text=True,
            check=True,
        )
        print("\n====== 安装本地 skydel 包成功 ======")
        print(install_result.stdout)
    except subprocess.CalledProcessError as e:
        print("\n====== 安装本地 skydel 包失败 ======")
        print("错误输出:", e.stderr)
        pytest.fail("无法安装本地 skydel 包，测试终止")

    yield

    try:
        uninstall_result = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", "skydel"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("\n====== 卸载 skydel 包成功 ======")
        print(uninstall_result.stdout)
    except subprocess.CalledProcessError as e:
        print("\n====== 卸载 skydel 包失败 ======")
        print("错误输出:", e.stderr)
        pytest.warns(UserWarning, lambda: None, "skydel 包卸载失败，可能残留环境中")


def test_skydel_metadata():
    try:
        pkg_metadata = metadata("skydel")
    except PackageNotFoundError:
        pytest.fail("skydel 包安装后仍未找到元数据，可能安装不完整")

    print("\n====== Package Info ======")
    print(pkg_metadata)

    assert pkg_metadata.get("Name") == "skydel", "包名称应为 'skydel'"
    assert "Version" in pkg_metadata, "元数据中必须包含版本信息"
    assert pkg_metadata.get("Version") != "", "版本号不能为空"


def test_skydel_import():
    print("\n====== Package Import ======")

    import skydel
    from skydel.skydelsdx import commands

    print(f"Current Package Version: {skydel.__version__}")
    print(f"Current API Version: {commands.ApiVersion}")

    assert hasattr(skydel, "__version__"), "skydel 模块必须有 __version__ 属性"
    assert skydel.__version__ != "", "包版本号不能为空"
    assert hasattr(commands, "ApiVersion"), "commands 模块必须有 ApiVersion 属性"
    assert commands.ApiVersion is not None, "API版本号不能为 None"


def test_skydel_runtime():
    from skydel.skydelsdx.commandfactory import createCommand

    cmd = createCommand(
        '{"CmdName": "New", "CmdUuid": "uuid", "DiscardCurrentConfig": true, "LoadDefaultConfig": true}'
    )

    print("\n====== Created Command ======")
    print(cmd)

    assert cmd.get(cmd.CmdNameKey) == "New", "命令名称应为 'New'"
    assert cmd.get(cmd.CmdUuidKey) == "uuid", "命令 UUID 应为 'uuid'"
    assert cmd.get("DiscardCurrentConfig") is True, "DiscardCurrentConfig 应为 True"
    assert cmd.get("LoadDefaultConfig") is True, "LoadDefaultConfig 应为 True"
