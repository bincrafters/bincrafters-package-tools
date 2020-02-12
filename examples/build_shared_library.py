from bincrafters import build_template_default


if __name__ == "__main__":
    # If your project is C++, pass the pure_c=False
    # For more information about: https://github.com/conan-io/conan-package-tools#generating-the-build-configurations-automatically
    pure_c = False
    builder = build_template_default.get_builder(pure_c=pure_c)
    builder.run()
