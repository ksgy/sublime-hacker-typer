import os.path
import sublime, sublime_plugin

hacker_enabled = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False
]

hacker_current = 0
viewid = 0

class HackerTyperCommand(sublime_plugin.TextCommand):
    def run(self, edit, enable=False, content=False, gotonext=False):
        global hacker_enabled
        global hacker_current
        global viewid

        if(viewid == 0):
            viewid = self.view.id()

        if(gotonext and hacker_current < len(hacker_enabled)):
            hacker_current = hacker_current + 1
            sublime.status_message("HackerTyper: Swithced to " + str(hacker_current))


        hacker_enabled[hacker_current] = enable

        if content is False or self.view.id() != viewid:
            return

        # if(self.view.sel()[0].begin() != self.view.sel()[0].end()):
        #     return

        # Replace contents
        self.view.replace(edit, sublime.Region(0, len(content)), 'aaa')


class HackerTyper(sublime_plugin.EventListener):
    solution_exists = False
    hacker_buffer = ""
    global hacker_current

    def on_activated(self, view):
        # Don't check for solution files if the plugin is disabled
        if hacker_enabled[hacker_current] is False:
            return

        # Check if the current file has a solution
        filename = view.file_name()
        if filename is None:
            return

        if(hacker_current == 0):
            hc = ''
        else:
            hc = hacker_current

        solution = filename + ".hackertyper" + str(hc)
        self.solution_exists = os.path.isfile(solution)


        # Give a feedback message if no solution was found
        # Clear the status bar if one was found
        if not self.solution_exists:
            err = "HackerTyper Error: " + os.path.basename(filename)
            err += ".hackertyper not found"
            return sublime.status_message(err)
        else:
            sublime.status_message("hackertyper: switch to: " + str(hc))

        print(solution)

        # Read the entire solution text
        self.hacker_buffer = open(solution).read()

    def on_modified_async(self, view):
        global hacker_enabled
        global hacker_current

        if hacker_enabled[hacker_current] is False or self.solution_exists is False:
            return

        # Fetch correct part of the buffer
        bufSize = view.size()

        # Fall back if we're outrunning the original solution
        if bufSize > len(self.hacker_buffer):
            return

        newBuf  = self.hacker_buffer[:bufSize]

        view.run_command("hacker_typer", { "enable": True, "content": newBuf });
