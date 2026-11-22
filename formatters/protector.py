
import re


class ContentProtector:

    def protect_code(self, text: str):
        pattern = r"```[\s\S]*?```"

        protected = []

        def replace(match):
            placeholder = f"CLIPCRAFT_CODE_{len(protected)}_END"
            protected.append((placeholder, match.group(0)))
            return placeholder

        modified_text = re.sub(pattern, replace, text)

        return modified_text, protected

    def restore_code(self, text: str, protected):
        for placeholder, original_code in protected:
            text = text.replace(placeholder, original_code)

        return text
