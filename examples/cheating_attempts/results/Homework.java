Homework Test Results

TestCase                                Result
================================================================
Testenv                                 Crashed due to signal 1:
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by TestEnv (file:/home/ovsyanka/code/autograder/examples/cheating_attempts/temp/Homework.java/) to field java.util.Collections$UnmodifiableMap.m
WARNING: Please consider reporting this to the maintainers of TestEnv
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Exception in thread "main" java.lang.SecurityException: Using environ is not permitted. It could indicate cheating.
	at NoReflectionAndEnvVarsSecurityManager.checkPermission(NoReflectionAndEnvVarsSecurityManager.java:25)
	at java.base/java.lang.System.getenv(System.java:999)
	at Homework.test_env(Homework.java:5)
	at TestEnv.main(TestEnv.java:59)


Testexit                                Crashed due to signal 103:
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by TestExit (file:/home/ovsyanka/code/autograder/examples/cheating_attempts/temp/Homework.java/) to field java.util.Collections$UnmodifiableMap.m
WARNING: Please consider reporting this to the maintainers of TestExit
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release


Testreflection                          Crashed due to signal 103:
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by TestReflection (file:/home/ovsyanka/code/autograder/examples/cheating_attempts/temp/Homework.java/) to field java.util.Collections$UnmodifiableMap.m
WARNING: Please consider reporting this to the maintainers of TestReflection
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release


================================================================
Result: 0/100

Key:
	Failed to Compile: Your submission did not compile due to a syntax or naming error
	Compiled with warnings: Your submission uses unchecked or unsafe operations
	Crashed due to signal SIGNAL_CODE: Your submission threw an uncaught exception.
	All signal error codes are described here: https://man7.org/linux/man-pages/man7/signal.7.html
	Exceeded Time Limit: Your submission took too much time to run (probably an infinite loop)
