import tbs

instance = tbs.InitilizetbsInstance()
tbs.AddTemplateDirectory(instance,"test")

tbs.replace.StartReplacing(instance)