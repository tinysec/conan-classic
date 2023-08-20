import mock
import pytest
import textwrap

from conans.test.utils.mocks import ConanFileMock, MockSettings
from conans.test.utils.test_files import temp_folder
from conan.tools.apple import is_apple_os, to_apple_arch, fix_apple_shared_install_name, XCRun
from conan.tools.apple.apple import _get_dylib_install_name # testing private function

def test_tools_apple_is_apple_os():
    conanfile = ConanFileMock()

    conanfile.settings = MockSettings({"os": "Macos"})
    assert is_apple_os(conanfile) == True

    conanfile.settings = MockSettings({"os": "watchOS"})
    assert is_apple_os(conanfile) == True

    conanfile.settings = MockSettings({"os": "Windows"})
    assert is_apple_os(conanfile) == False


def test_tools_apple_to_apple_arch():
    conanfile = ConanFileMock()

    conanfile.settings = MockSettings({"arch": "armv8"})
    assert to_apple_arch(conanfile) == "arm64"

    conanfile.settings = MockSettings({"arch": "x86_64"})
    assert to_apple_arch(conanfile) == "x86_64"


def test_fix_shared_install_name_no_libraries():
    conanfile = ConanFileMock(
        options="""{"shared": [True, False]}""",
        options_values={"shared": True})
    conanfile.settings = MockSettings({"os": "Macos"})
    conanfile.folders.set_base_package(temp_folder())

    with pytest.raises(Exception) as e:
        fix_apple_shared_install_name(conanfile)
        assert "not found inside package folder" in str(e.value)


def test_xcrun_public_settings():
    # https://github.com/conan-io/conan/issues/12485
    conanfile = ConanFileMock()
    conanfile.settings = MockSettings({"os": "watchOS"})

    xcrun = XCRun(conanfile, use_settings_target=True)
    settings = xcrun.settings

    assert settings.os == "watchOS"

def test_get_dylib_install_name():
    # https://github.com/conan-io/conan/issues/13014
    single_arch = textwrap.dedent("""
    /path/to/libwebp.7.dylib:
    /absolute/path/lib/libwebp.7.dylib
    """)

    universal_binary = textwrap.dedent("""
    /.conan/data/package/lib/libwebp.7.dylib (architecture x86_64):
    /absolute/path/lib/libwebp.7.dylib
    /.conan/data/package/lib/libwebp.7.dylib (architecture arm64):
    /absolute/path/lib/libwebp.7.dylib
    """)

    for mock_output in (single_arch, universal_binary):
        with mock.patch("conan.tools.apple.apple.check_output_runner") as mock_output_runner:
            mock_output_runner.return_value = mock_output
            install_name = _get_dylib_install_name("/path/to/libwebp.7.dylib")
            assert "/absolute/path/lib/libwebp.7.dylib" == install_name
