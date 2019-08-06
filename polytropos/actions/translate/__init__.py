from polytropos.actions.translate.__translator import Translator
from polytropos.actions.translate.__translate import Translate
from polytropos.actions.translate import __type_translators
import polytropos.ontology.variable

Translator.register_type_translator(polytropos.ontology.variable.NamedList, __type_translators.NamedListTranslator)
Translator.register_type_translator(polytropos.ontology.variable.List, __type_translators.ListTranslator)
Translator.register_type_translator(polytropos.ontology.variable.Folder, __type_translators.FolderTranslator)
Translator.register_type_translator(None, __type_translators.GenericTypeTranslator)
