# -*- coding: utf-8 -*-
#
#	Copyright (C) 2012 by Igor E. Novikov
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, base64
import StringIO

from PIL import Image

from uc2 import _, events, msgconst
from uc2.formats.sk2.sk2_presenter import SK2_Presenter
from uc2.formats.sk2 import sk2_model


def png_loader(appdata, filename, translate=True, cnf={}, **kw):
	try:
		fileptr = open(filename, 'rb')
	except:
		errtype, value, traceback = sys.exc_info()
		msg = _('Cannot open %s fileptr for reading') % (filename)
		events.emit(events.MESSAGES, msgconst.ERROR, msg)
		raise IOError(errtype, msg + '\n' + value, traceback)

	content = fileptr.read()
	fileptr.close()
	bitmap = base64.b32encode(content)
	raw_image = Image.open(StringIO.StringIO(content))
	sk2_doc = SK2_Presenter(appdata, cnf)
	page = sk2_doc.methods.get_page()
	layer = sk2_doc.methods.get_layer(page)
	pxm = sk2_model.Pixmap(sk2_doc.config, bitmap=bitmap, size=raw_image.size)
	layer.childs.append(pxm)
	sk2_doc.update()
	return sk2_doc

def png_saver(doc, filename, translate=True, cnf={}, **kw):
	pass

def check_png(path):

	try:
		fileptr = open(path, 'rb')
	except:
		errtype, value, traceback = sys.exc_info()
		msg = _('Cannot open %s fileptr for reading') % (path)
		events.emit(events.MESSAGES, msgconst.ERROR, msg)
		raise IOError(errtype, msg + '\n' + value, traceback)

	mstr = fileptr.read(4)[1:]
	fileptr.close()
	if mstr == 'PNG': return True
	return False
