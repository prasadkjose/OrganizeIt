from organizeIt.schemaValidation import Validator # Validator.py

def main():
    schema_validator = Validator.YAMLConfigValidator()
    schema_validator.validate_config()

if __name__ == '__main__':
    main() 