<HTML>
<HEAD>
<TITLE>Switch Port Config Conversion Tool</TITLE>
</HEAD>
<BODY>
<H2>Config Convert Tool</H2>
This tool will offer you the possibility to change ports, so you could simulate a config from a BDX8 on an X460 for example.
<FORM enctype="multipart/form-data" NAME="showtechForm" METHOD="POST" ACTION="configconvert.py">
<input type="checkbox" name="use_original_ports">Populate original ports in next page<br>
<input type="file" name="file"><br>
<TEXTAREA NAME="config" COLS="100" ROWS="18" AUTOFOCUS="ON" PLACEHOLDER="Paste your show config here">
</TEXTAREA><br>
<INPUT TYPE="submit" VALUE="Analyze" NAME="submit">
</FORM>
</BODY>
</HTML>
