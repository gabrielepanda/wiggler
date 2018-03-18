import os

from wiggler.common.resource import Resource
#from wiggler.core.resources.snippets import Snippet

START = 0
END = 1

class CodeSection(object):

    def __init__(self, code, start_offset, **section_options):
        #self.original_offsets = (self.template.section_offset[section_name],)
        self.original_offsets = (start_offset,)
        self.section_options = section_options
        self.yield_inserted_lines = []

    def update_code(self, code):
        self.original_code = code
        self.mangled_code = code
        self.offsets = offsets
        if self.section_options.get('deloopify', True):
            self.yield_inserted_lines = []
            self.deloopify()
        self.mangled_size = len(self.mangled_code.splitlines())
        self.offsets = (
            self.original_offsets[START], self.original_offsets[START] + self.mangled_size)

    def change_start_offset(self, increment):
        def incr(offset):
            return offset + increment
        self.yield_inserted_lines = map(incr, self.yield_inserted_lines)
        self.offsets = tuple(map(incr, self.offsets))

    def get_original_line(self, line):
        nyields = 0
        for yield_line in self.yield_inserted_lines:
            if line > yield_line:
                nyields += 1
        original_line = line - nyields - self.offsets[START] + 1
        return original_line

    @staticmethod
    def find_next_line(index, code_lines):
        if index is None:
            return None, None
        while index < len(code_lines) - 1:
            index = index + 1
            line = code_lines[index]
            if line != '':
                return index, line
        return None, None

    def deloopify(self):
        '''Inject a yield at the end of every loop

        '''
        code_lines = self.original_code.splitlines()
        lines = len(code_lines)
        index = -1
        loops = [None]
        indent = 0
        index, line = self.find_next_line(index, code_lines)
        while line:
            m = re.match("(\s*)(for|while)", line)
            if m:
                # print "match found on line %d" % index
                index, line = self.find_next_line(index, code_lines)
                m = re.match("(\s*)(.+)", line)
                # print "first loop line %d - %s " % (index, line)
                loops.insert(0, len(m.groups()[0]))
                # print "loop block indentation %d" % loops[0]
                index, line = self.find_next_line(index, code_lines)
            if loops[0]:
                if line:
                    m = re.match("(\s*)(.*)", line)
                    indent = len(m.groups()[0])
                    # print "indent %d" % indent
                    if indent < loops[0]:
                        # template = "dedent from %d to %d on line %d"
                        # print template % (loops[0], indent, index)
                        # print "injecting yield in line %d" % index
                        # dedent, end code block
                        code_lines.insert(index, ' ' * loops[0] + "yield")
                        self.yield_inserted_lines.append(
                            index + self.offsets[START])
                        lines += 1
                        loops.pop(0)
                if line is None or index == lines - 1:
                    # print "End of file after loop"
                    # print "injecting yield in line %d" % (lines -1)
                    # dedent, end code block
                    code_lines.insert(lines, ' ' * loops[0] + "yield")
                    self.yield_inserted_lines.append(
                        lines + self.offsets[START])
                    loops.pop(0)
            index, line = self.find_next_line(index, code_lines)
        self.mangled_code = '\n'.join(code_lines)

class Code(Resource):

    def __init__(self, meta, **kwargs):
        super(Code, self).__init__(meta, **kwargs)
        #self.sprite_asset_id = "ciccio"
        #self.module_filename = os.path.join(project_dir, "src", sprite_asset_id + ".py")
        #self.module_name = asset_id
        self.generated_code = ''
        self.sections = {}
        self.compile_error = False
        self.template = None
        self.module = None
        self.traceback_message = None
        self.traceback_line = None
        self.errored_section = None
        self.errored_line = None
        template_id = self._meta['template']
        self.template = self._manager.get_resource('template', template_id)
        #selfsuff_id = self._meta['selfsuff']
        #self.selfsuff = self._manager.get_resource('selfsuff', selfsuff_id)

        sections_code = self._meta['sections']
        # code may contain sections only useful for different self sufficiency levels.
        # itern on existing sections in the template
        for section_name, offsets in self.template.sections.items():
            #section_options = self.selfsuff.sections['options']
            section_options = {}
            start_offset = offsets['start_offset']
            try:
                code = sections_code[section_name]
            except KeyError:
                # Section does not exist in code
                # this should not happen
                continue
            self.sections[section_name] = CodeSection(code, start_offset, **section_options)

        #for section_name, snippet_id in sections:
        #    snippet = Snippet(snippet_id)
        #    snippet_code = snippet.load_data()
        #    self.sections[section_name] = snippet_code

    def generate_module_src(self):
        # adjust offsets for all the successive sections
        for section in self.sections.values():
            start_offset = section.offsets[START]
            section_size = section.mangled_size
            for section in self.sections.values():
                if section.offsets[END] > start_offset:
                    # -1 because the jinjia token is replaced and doesn't count
                    section.change_start_offset(section_size - 1)

        self.generated_code = self.template.render(mangled_user_code)

    def write_module_src(self):
        with open(self.module_filename, "w") as module_file:
            module_file.write(self.generated_code)

