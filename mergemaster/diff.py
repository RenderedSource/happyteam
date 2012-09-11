import re

class Visualizer:
    def parse(self, diff):
        lines = diff.splitlines()
        if len(lines) < 2:
            raise Exception('Too few lines')

        start_hunk_regex = re.compile('^@@ \-([0-9]+),([0-9]+) \+([0-9]+),([0-9]+) @@')
        parsed_lines = []

        for line in lines[2:]:
            match = start_hunk_regex.match(line)
            if match:
                a_from = match.group(1)
                a_to = match.group(2)
                b_from = match.group(3)
                b_to = match.group(4)
                print a_from, a_to, b_from, b_to
                continue

            line_class = ''
            if line.startswith('-'):
                line_class = 'removed'
            elif line.startswith('+'):
                line_class = 'added'
            parsed_lines.append({
                'css_class': line_class,
                'text': line[1:]
            })

        result = {
            'old_file': 'qqq',
            'new_file': 'qqq',
            'lines': parsed_lines
        }

        return result



