from Vintageous import local_logger

import sublime

import os


_logger = local_logger(__name__)


class DotFile(object):
    def __init__(self, path):
        self.path = path

    @staticmethod
    def from_user():
        path = os.path.join(sublime.packages_path(), 'User', '.vintageousrc')
        return DotFile(path)

    def run(self):
        try:
            with open(self.path, 'r') as f:
                for line in f:
                    cmd, args = self.parse(line)
                    if cmd:
                        _logger().info('[DotFile] running: {0} {1}'.format(cmd, args))
                        sublime.active_window().run_command(cmd, args)
        except FileNotFoundError:
            pass

    def parse(self, line):
        try:
            _logger().info('[DotFile] parsing line: {0}'.format(line))
            line = line.lstrip(':')
            if line.startswith(('map ')):
                return ('ex_map', {'command_line': line.rstrip()})

            if line.startswith(('omap ')):
                return ('ex_omap', {'command_line': line.rstrip()})

            if line.startswith(('nmap ')):
                return ('ex_nmap', {'command_line': line.rstrip()})
            
            if line.startswith(('vmap ')):
                return ('ex_vmap', {'command_line': line.rstrip()})

            if line.startswith(('let ')):
                return ('ex_let', {'command_line': line.strip()})
        except Exception:
            print('Vintageous: bad config in dotfile: "%s"' % line.rstrip())
            _logger().debug('bad config inf dotfile: "%s"', line.rstrip())

        return None, None
