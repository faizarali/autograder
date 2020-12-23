import re
from pathlib import Path
import shutil

import sh

from autograder.util import AutograderError

from .abstract_base_class import ArgList, TestCase, TEST_HELPERS_DIR

PUBLIC_CLASS_MATCHER = re.compile(r"public.+class")
JNA_FILE_NAME = "jna.jar"
PATH_TO_JNA_FILE = TEST_HELPERS_DIR / "extra" / JNA_FILE_NAME


class JavaTestCase(TestCase):
    """Please, ask students to remove their main as it can theoretically
    generate errors (not sure how though).
    Java doesn't support testcase precompilation because it must always
    link files on compilation.
    """

    source_suffix = ".java"
    executable_suffix = ""
    helper_module_name = "TestHelper.java"
    compiler = sh.Command("javac")
    jar = sh.Command("jar")
    virtual_machine = sh.Command("java")

    @classmethod
    def precompile_submission(cls, submission: Path, student_dir: Path, source_file_name: str, arglist):
        copied_submission = super().precompile_submission(submission, student_dir, submission.name, arglist)
        renamed_submission = copied_submission.parent / source_file_name
        copied_submission.rename(renamed_submission)
        try:
            cls.compiler(renamed_submission, *arglist)
        finally:
            renamed_submission.unlink()

        # What if there are multiple .class files after compilation? What do we do, then?
        return renamed_submission.with_suffix(".class")

    def compile_testcase(self, precompiled_submission: Path):
        new_self_path = precompiled_submission.with_name(self.path.name)
        self.compiler(
            new_self_path,
            "-cp",
            f".:jna.jar",
            *self.argument_lists[ArgList.TESTCASE_COMPILATION],
        )
        return lambda *args, **kwargs: self.virtual_machine("-cp", ".:jna.jar", self.path.stem, *args, **kwargs)

    @classmethod
    def run_additional_testcase_operations_in_student_dir(cls, student_dir: Path):
        shutil.copyfile(PATH_TO_JNA_FILE, student_dir / JNA_FILE_NAME)

    def delete_executable_files(self, precompiled_submission: Path):
        for p in precompiled_submission.parent.iterdir():
            if p.suffix == ".class" and self.path.stem in p.stem:
                p.unlink()

    def prepend_test_helper(self):
        """Puts private TestHelper at the end of testcase class.
        This is quite a crude way to do it but it is the easiest
        I found so far.
        """
        with open(self.path) as f:
            content = f.read()
        final_content = self._add_at_the_end_of_public_class(self.get_formatted_test_helper(), content)
        final_content = (
            f"""import com.sun.jna.Library;
                import com.sun.jna.Native;
            """
            + final_content
        )
        with open(self.path, "w") as f:
            f.write(final_content)

    def _add_at_the_end_of_public_class(self, helper_class: str, java_file: str):
        # TODO: Figure out a better way to do this.
        # This way is rather crude and can be prone to errors,
        # but java does not really leave us any other way to do it.

        match = PUBLIC_CLASS_MATCHER.search(java_file)
        if match is None:
            raise ValueError(f"Public class not found in {self.path}")
        else:
            main_class_index = match.start()

        file_starting_from_main_class = java_file[main_class_index:]
        closing_brace_index = self._find_closing_brace(file_starting_from_main_class)
        return "".join(
            [
                java_file[:main_class_index],
                file_starting_from_main_class[:closing_brace_index],
                "\n" + helper_class + "\n" + "}",
                java_file[closing_brace_index + 1 :],
            ]
        )

    def _find_closing_brace(self, s: str):
        bracecount = 0
        for i in range(len(s)):
            if s[i] == "{":
                bracecount += 1
            elif s[i] == "}":
                bracecount -= 1
                if bracecount == 0:
                    return i
        else:
            raise AutograderError(f"Braces in testcase '{self.path.name}' don't match.")