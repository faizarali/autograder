from pathlib import Path
import sys


from autograder.testcase_utils.abstract_testcase import (
    ArgList,
    ShellCommand,
    TestCase as AbstractTestCase,
)
from autograder.testcase_utils.shell import get_shell_command, EMPTY_COMMAND


INCLUDE_MEMLEAK: str = '\n#include "leak_detector_c.h"\n'


class TestCase(AbstractTestCase):
    source_suffix = ".c"
    executable_suffix = ".out"
    helper_module = "test_helper.c"  # type: ignore
    compiler = get_shell_command("gcc")
    SUBMISSION_COMPILATION_ARGS = ["-Dmain=__student_main__"]
    TESTCASE_COMPILATION_ARGS = []
    if sys.platform.startswith("win32"):
        # Windows cannot load its libraries if linking is dynamic
        TESTCASE_COMPILATION_ARGS += ["-static"]
    else:
        # Windows does not support re-declaring scanf_s even if mingw is used
        SUBMISSION_COMPILATION_ARGS += ["-Dscanf_s=scanf"]

    @classmethod
    def is_installed(cls) -> bool:
        return cls.compiler is not EMPTY_COMMAND

    @classmethod
    def get_template_dir(cls):
        return cls.type_source_file.parent / "c_templates"

    @classmethod
    def precompile_submission(
        cls,
        submission: Path,
        student_dir: Path,
        possible_source_file_stems: str,
        arglist,
        config,
    ) -> Path:
        """Compiles student submission without linking it.
        It is done to speed up total compilation time
        """
        copied_submission = super().precompile_submission(submission, student_dir, [submission.stem], arglist, config)
        precompiled_submission = copied_submission.with_suffix(".o")

        # TODO: Append INCLUDE_MEMLEAK to submission here
        # copied_submission.write_text(copied_submission.read_text())
        try:
            cls.compiler(
                "-c",
                f"{copied_submission}",
                "-o",
                precompiled_submission,
                *arglist,
                *cls.SUBMISSION_COMPILATION_ARGS,
            )
        finally:
            copied_submission.unlink()
        return precompiled_submission

    def precompile_testcase(self):
        self.compiler(
            "-c",
            self.path,
            "-o",
            self.path.with_suffix(".o"),
            *self.argument_lists[ArgList.TESTCASE_PRECOMPILATION],
        )
        self.path.unlink()
        self.path = self.path.with_suffix(".o")

    def compile_testcase(self, precompiled_submission: Path) -> ShellCommand:
        executable_path = self.make_executable_path(precompiled_submission)
        files_to_compile = [
            precompiled_submission.with_name(self.path.name),
            precompiled_submission,
        ]
        # if self.config.file["GCC"].getboolean("MEMORY_LEAK_DETECTION"):
        #     files_to_compile.append(precompiled_submission.with_name("memleak_detector.c"))
        self.compiler(
            "-o",
            executable_path,
            *files_to_compile,
            *self.argument_lists[ArgList.TESTCASE_COMPILATION],
            *self.TESTCASE_COMPILATION_ARGS,
        )
        return ShellCommand(executable_path)

    @property
    def memleak_detector_source_file(self) -> Path:
        return self.type_source_file.parent / "memleak_detector" / "memleak_detector.c"

    @property
    def memleak_detector_header_file(self) -> Path:
        return self.type_source_file.parent / "memleak_detector" / "memleak_detector.h"
