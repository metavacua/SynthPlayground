import os


def find_untested_code(source_dir, test_dir):
    untested_files = []
    source_files = set()
    test_files = set()

    for root, _, files in os.walk(source_dir):
        for file in files:
            if (
                file.endswith(".py")
                and not file.startswith("test_")
                and not file.startswith("__init__")
            ):
                source_files.add(os.path.join(root, file))

    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".py") and file.startswith("test_"):
                test_files.add(os.path.join(root, file))

    for source_file in source_files:
        test_file_name = "test_" + os.path.basename(source_file)
        test_file_path = os.path.join(test_dir, test_file_name)
        if test_file_path not in test_files:
            untested_files.append(source_file)

    return untested_files, source_files, test_files


def main():
    source_dir = "tooling"
    test_dir = "tests"
    threshold = 10

    untested_files, source_files, _ = find_untested_code(source_dir, test_dir)

    if untested_files:
        print("Untested files found:")
        for file in untested_files:
            print(f"- {file}")

    coverage = 0
    if source_files:
        coverage = ((len(source_files) - len(untested_files)) / len(source_files)) * 100

    print(f"Test coverage: {coverage:.2f}%")

    if coverage < threshold:
        print(f"Test coverage is below the required threshold of {threshold}%.")
        exit(1)


if __name__ == "__main__":
    main()
