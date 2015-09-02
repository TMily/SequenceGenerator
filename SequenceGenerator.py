import sublime, sublime_plugin

class SequenceGeneratorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.status_message("You could set the sequence format to: {start:step} or {start}.")
        self.view.window().show_input_panel("Enter Sequence Format:", "1", self.on_done, self.on_change, None)
    def on_done(self, text):
        parameter = self.VerifyFormat(text)
        if not parameter:
            sublime.error_message("Your input is invalid.")
        else:
            self.view.run_command("generate_sequence", {"parameter": parameter})

    def on_change(self, text):
        if not self.VerifyFormat(text):
            sublime.status_message("Your input is invalid.")
        else:
            sublime.status_message("You could set the sequence format to: {start:step:mode:case} only first arg can not be omitted.")
    def VerifyFormat(self, text):
        splits = text.replace(":", " ").split()
        length = len(splits)
        if not 1<=length<=4:
            return False
        for i in range(len(splits)):
            if i < 2:
                try:
                    number = int(splits[i])
                except:
                    return False
            if i >= 2:
                try:
                    txt = str(splits[i])
                except:
                    return False

        parameter = {'start':1, 'step':1, 'mode':"n", 'case':"l"}

        if length==1:
            parameter['start'] = int(splits[0])
        elif length==2:
            parameter['start'] = int(splits[0])
            parameter['step'] = int(splits[1])
        elif length==3:
            parameter['start'] = int(splits[0])
            parameter['step'] = int(splits[1])
            parameter['mode'] = str(splits[2])
        elif length==4:
            parameter['start'] = int(splits[0])
            parameter['step'] = int(splits[1])
            parameter['mode'] = str(splits[2])
            parameter['case'] = str(splits[3])

        return parameter

class GenerateSequenceCommand(sublime_plugin.TextCommand):
    def run(self, edit, parameter):
        new_sel = []
        for region in self.view.sel():
            self.view.erase(edit, region)
            if parameter['mode'] == "n":
                sequence = str(parameter['start'])
            else:
                start = int(parameter['start'])
                sequence = self.int_toletter(start,str(parameter['case']))
            self.view.insert(edit, region.begin(), sequence)

            new_sel.append(sublime.Region(region.begin(), region.begin() + len(sequence)))

            parameter['start'] += parameter['step']

        if len(new_sel) > 0:
            self.view.sel().clear()
            for r in new_sel:
                self.view.sel().add(r)

    def int_toletter(self,number,case):
        result = ""
        alpha = number // 27
        remainder = number - (alpha * 26)
        if case=="l":
            offset = 96
        else:
            offset = 64
        if alpha > 0:
            result = chr(alpha + offset)
        if remainder > 0:
            result += chr(remainder + offset)
        return result