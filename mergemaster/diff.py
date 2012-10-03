import re

class Visualizer:
    def parse(self, diff):
        lines = diff.diff.splitlines()
        if len(lines) < 2:
            raise Exception('Too few lines')

        start_hunk_regex = re.compile('^@@ \-([0-9]+),([0-9]+) \+([0-9]+),([0-9]+) @@')
        parsed_lines = []

        line_a = 0
        line_b = 0

        for line in lines[2:]:
            match = start_hunk_regex.match(line)
            if match:
                line_a = int(match.group(1))
                line_b = int(match.group(3))
                continue

            line_class = ''
            str_line_a = ''
            str_line_b = ''
            if line.startswith('-'):
                line_class = 'removed'
                str_line_a = str(line_a)
                line_a += 1
            elif line.startswith('+'):
                line_class = 'added'
                str_line_b = str(line_b)
                line_b += 1
            else:
                str_line_a = str(line_a)
                line_a += 1
                str_line_b = str(line_b)
                line_b += 1

            parsed_lines.append({
                'css_class': line_class,
                'line_a': str_line_a,
                'line_b': str_line_b,
                'text': line[1:]
            })

        if diff.new_file:
            action_icon_class = "icon-plus"
        elif diff.deleted_file:
            action_icon_class = "icon-remove"
        else:
            action_icon_class = "icon-pencil"

        result = {
            'old_file': diff.a_blob.path,
            'new_file': diff.b_blob.path,
            'action_icon_class': action_icon_class,
            'lines': parsed_lines
        }

        return result



