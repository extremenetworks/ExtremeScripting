class Clean_Config(object):
    def process_config(self):
        self.cfg_modules = []
        print "\nProcessing Configuration...\n\n"
        config = exsh.clicmd('show config', capture=True)
        config = config.splitlines(True)
        print "\n->show configuration\n"
        moduleName = ''
        moduleStr = ''
        configExist = False
        for line in config:
            if '#' not in line and line != '\n':
                moduleStr += line
                configExist = True
            elif configExist is True and '#' in line:
                self.cfg_modules.append(moduleName)
                moduleStr = line
                moduleName = ''
                configExist = False
            elif '#' in line:
                moduleStr += line
                configExist = False
                if '# Module ' in line:
                    moduleName = line.replace('# Module ','')
                    moduleName = moduleName.replace(' configuration.\n','')
                    moduleName = moduleName.lower()
            elif configExist is True and line == '\n':
                moduleStr += line
            else:
                moduleStr = ''

def main():
    cfg = Clean_Config()
    cfg.process_config()
    for module in cfg.cfg_modules:
        cmd = 'show config %s' % module
        print exsh.clicmd(cmd, capture=True)

main()
