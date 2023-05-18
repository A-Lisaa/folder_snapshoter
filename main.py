from src.fs_scaner import scan_folder


def main() -> None:
    folder = scan_folder(".")
    folder.to_brotli_archive("result")


if __name__ == "__main__":
    main()
