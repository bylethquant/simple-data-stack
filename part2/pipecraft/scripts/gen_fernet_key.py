from cryptography.fernet import Fernet


def get_fernet_key():
    """Generates a fernet key."""
    return Fernet.generate_key().decode()


def main():
    print(get_fernet_key())


if __name__ == "__main__":
    main()
