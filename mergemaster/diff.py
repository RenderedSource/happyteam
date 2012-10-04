import re

class Visualizer:
    def parse(self, patch):
        file_patches = self.split_patch(patch)

        diffs = []
        for file_patch in file_patches:
            diffs.append(self.parce_file_patch(file_patch))

        return diffs

    def split_patch(self, patch):
        lines = patch.splitlines()
        file_patches = []
        current_file_patch = None

        for line in lines:
            if line.startswith('diff --git '):
                if current_file_patch is not None:
                    file_patches.append(current_file_patch)
                current_file_patch = []
            current_file_patch.append(line)
        if current_file_patch is not None:
            file_patches.append(current_file_patch)

        return file_patches

    def parce_file_patch(self, patch):

        old_file = None
        new_file = None
        binary = False
        created = False
        deleted = False

        hunks = []
        current_hunk = None
        line_a = 0
        line_b = 0

        start_file_regex = re.compile('^diff --git a/(.+) b/(.+)$')
        binary_file_regex = re.compile('^Binary files a?/(.+) and b?/(.+) differ$')
        start_hunk_regex = re.compile('^@@ \-([0-9]+)(?:,[0-9]+)? \+([0-9]+)(?:,[0-9]+)? @@')

        for line in patch:
            match = start_file_regex.match(line)
            if match:
                old_file = match.group(1)
                new_file = match.group(2)
                if old_file == 'dev/null':
                    created = True
                    old_file = new_file
                elif new_file == 'dev/null':
                    deleted = True
                    new_file = old_file
                continue

            match = binary_file_regex.match(line)
            if match:
                old_file = match.group(1)
                if old_file == 'dev/null':
                    created = True
                    old_file = new_file
                new_file = match.group(2)
                if new_file == 'dev/null':
                    deleted = True
                    new_file = old_file
                binary = True
                break

            match = start_hunk_regex.match(line)
            if match:
                line_a = int(match.group(1))
                line_b = int(match.group(2))
                if current_hunk is not None:
                    hunks.append(current_hunk)
                current_hunk = []
                continue

            if line == '\ No newline at end of file':
                continue

            if current_hunk is None:
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

            current_hunk.append({
                'css_class': line_class,
                'line_a': str_line_a,
                'line_b': str_line_b,
                'text': line[1:]
            })

        if current_hunk is not None:
            hunks.append(current_hunk)

        action_icon_class = 'icon-pencil'

        if created:
            action_icon_class = "icon-plus"
        elif deleted:
            action_icon_class = "icon-remove"

        result = {
            'old_file': old_file,
            'new_file': new_file,
            'action_icon_class': action_icon_class,
            'binary': binary,
            'hunks': hunks
        }

        return result



