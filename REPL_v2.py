#!python3

import base64, code, io, keyboard, sys, ui

UiV = base64.b64decode("WwogIHsKICAgICJub2RlcyIgOiBbCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3swLCAwfSwgezU4MCwgNDB9fSIsCiAgICAgICAgImNsYXNzIiA6ICJMYWJlbCIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgImZsZXgiIDogIldIIiwKICAgICAgICAgICJuYW1lIiA6ICJsYWJlbDEiLAogICAgICAgICAgInRleHRfY29sb3IiIDogIlJHQkEoMC43OTQ4MTEsMC43OTQ4MTEsMC43OTQ4MTEsMS4wMDAwMDApIiwKICAgICAgICAgICJmcmFtZSIgOiAie3sxMDUsIDEyM30sIHsxNTAsIDMyfX0iLAogICAgICAgICAgInV1aWQiIDogIkVBNzc4Q0I4LUZEMTEtNDZGQi1COEFBLTkwRkZEQzREQkE1QiIsCiAgICAgICAgICAiY2xhc3MiIDogIkxhYmVsIiwKICAgICAgICAgICJhbGlnbm1lbnQiIDogImxlZnQiLAogICAgICAgICAgInRleHQiIDogIiIsCiAgICAgICAgICAiZm9udF9zaXplIiA6IDEyLAogICAgICAgICAgImZvbnRfbmFtZSIgOiAiTWVubG8tUmVndWxhciIKICAgICAgICB9LAogICAgICAgICJzZWxlY3RlZCIgOiB0cnVlCiAgICAgIH0KICAgIF0sCiAgICAiZnJhbWUiIDogInt7MCwgMH0sIHs1ODAsIDQwfX0iLAogICAgImNsYXNzIiA6ICJWaWV3IiwKICAgICJhdHRyaWJ1dGVzIiA6IHsKICAgICAgImZsZXgiIDogIiIsCiAgICAgICJjdXN0b21fY2xhc3MiIDogIlJFUExWaWV3IiwKICAgICAgImVuYWJsZWQiIDogdHJ1ZSwKICAgICAgInRpbnRfY29sb3IiIDogIlJHQkEoMC4wMDAwMDAsMC40NzgwMDAsMS4wMDAwMDAsMS4wMDAwMDApIiwKICAgICAgImJvcmRlcl9jb2xvciIgOiAiUkdCQSgwLjAwMDAwMCwwLjAwMDAwMCwwLjAwMDAwMCwxLjAwMDAwMCkiLAogICAgICAiYmFja2dyb3VuZF9jb2xvciIgOiAiUkdCQSgxLjAwMDAwMCwxLjAwMDAwMCwxLjAwMDAwMCwxLjAwMDAwMCkiLAogICAgICAibmFtZSIgOiAiIgogICAgfSwKICAgICJzZWxlY3RlZCIgOiBmYWxzZQogIH0KXQ==")

class REPLView (ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		self.input_buffer = ''
	
	def did_load(self):
		self.bg_color = '#580303'
		self.tint_color = 'white'
		self.kb_text_changed()
		
	def kb_text_changed(self):
		line = self.get_eval_line()
		if not line == None:
			if line.startswith('>>>') or line.startswith('...'):
				self['label1'].text = line
				if line[-1] == '\n':
					self.eval_code(line)
			else:
				keyboard.insert_text('>>> ')

	def get_eval_line(self):
		before, _ = keyboard.get_input_context()
		if before and (before.startswith('>>>') or before.startswith('...')):
			return before
		return ''

	def eval_code(self, before):
		Did_run = False
		if before.startswith('>>>'):
			before = before.split('>>> ')[-1]
		if before.startswith('...'):
			before = before.split('... ')[-1]
		prev_stdout = sys.stdout
		if '\n' == before[-1]:
			before = before.replace('\n', '')
			try:
				with io.StringIO() as redirected_out:
					sys.stdout = redirected_out
					c = code.compile_command(before, '<string>', 'single')
					exec(c, globals())
					Did_run = True
					output = redirected_out.getvalue()
					if len(output) > 1000:
						output = '[...]\n' + output[-1000:]
					keyboard.insert_text(output)
			except Exception as E:
				sys.stdout = prev_stdout
				keyboard.insert_text(E)
		sys.stdout = prev_stdout

def main():
	if keyboard.is_keyboard():
		v = ui.load_view_str(UiV)
		keyboard.set_view(v, 'minimized')
	else:
		print('This script is meant to be run in the custom Pythonista Keyboard.')

if __name__ == '__main__':
	main()
