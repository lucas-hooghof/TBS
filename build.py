import tbs

import os

instance = tbs.CreateInstance()
instance.AddDirectory("test")

Parser = tbs.TemplateParser(instance)
Parser.GetAllTemplatesInDirectories()
Parser.ParseTemplates()

ScriptGenerator = tbs.ScriptGen(instance,Parser,os.path.dirname(os.path.abspath(__file__)))





