
import re


class ContentProtector:

    def protect_code(self, text: str):
        # Match protected content in priority order:
        # 1. Fenced code blocks
        # 2. Display equations ($$...$$)
        # 3. Inline code (`...`)
        # 4. Inline equations ($...$)

        pattern = re.compile(
            r"```[\s\S]*?```"
            r"|\$\$[\s\S]*?\$\$"
            r"|`[^`\n]+`"
            r"|\$(?!\$)[^\n$]+\$(?!\$)"
        )

        protected = []

        def replace(match):
            placeholder = (
                f"CLIPCRAFT_PROTECTED_{len(protected)}_END"
            )

            protected.append((placeholder, match.group(0)))

            return placeholder

        modified_text = pattern.sub(replace, text)

        return modified_text, protected

    def restore_code(self, text: str, protected):
        for placeholder, original_content in protected:
            if text.count(placeholder) != 1:
                raise RuntimeError(
                    f"Protected content was changed or lost: {placeholder}"
                )

            text = text.replace(
                placeholder,
                original_content
            )

        return text
