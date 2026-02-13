import tbs

instance = tbs.CreateInstance()
instance.AddDirectory("test")


Parser = tbs.TemplateParser(instance)
Parser.GetAllTemplatesInDirectories()

Parser.ParseTemplate(Parser.templates[0])

