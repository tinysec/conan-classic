from conan.tools._check_build_profile import check_using_build_profile
from conan.tools.files.files import save_toolchain_args


class BazelToolchain(object):

    def __init__(self, conanfile, namespace=None):
        self._conanfile = conanfile
        self._namespace = namespace
        check_using_build_profile(self._conanfile)

    def generate(self):
        content = {}
        configs = ",".join(self._conanfile.conf.get("tools.google.bazel.configs",
                                                    default=[],
                                                    check_type=list))
        if configs:
            content["bazel_configs"] = configs

        bazelrc = self._conanfile.conf.get("tools.google.bazel.bazelrc_path")
        if bazelrc:
            content["bazelrc_path"] = bazelrc

        save_toolchain_args(content, namespace=self._namespace)
